# data_processing.py

"""
This module handles processing of data fetched from the JIRA API,
including processing individual issues and generating statistics for project versions.
"""

import pandas as pd
import requests


from typing import List, Tuple
from config import Config
from jira_api import get_jira_auth, get_issues_by_project_version
from logger_config import logger


def process_issues(issues: List[dict], auth: Tuple[str, str]) -> Tuple[List[dict], pd.DataFrame]:
    """
    Processes a list of issues from JIRA and compiles them into structured data.

    Parameters:
    issues (List[dict]): A list of issue data in dictionary format.
    auth (Tuple[str, str]): Authentication credentials for JIRA API.

    Returns:
    Tuple[List[dict], pd.DataFrame]: A tuple containing a list of processed issues and a DataFrame of the processed data.
    """
    
    headers = {"Accept": "application/json"}
    result = []

    for issue in issues:
        try:
            processed_issue = process_single_issue(issue, auth, headers)
            result.append(processed_issue)
        except KeyError as e:
            logger.error(f"Missing key in issue data {issue['id'] if 'id' in issue else 'unknown'}: {e}")
        except requests.RequestException as e:
            logger.error(f"HTTP request failed while processing issue {issue['id'] if 'id' in issue else 'unknown'}: {e}")

    result = sorted(result, key=lambda d: d['ID'], reverse=True) 
    df_result = pd.DataFrame(result)
    
    return result, df_result


def process_single_issue(issue: dict, auth: Tuple[str, str], headers: dict) -> dict:
    """
    Processes a single JIRA issue and extracts relevant data. 

    Parameters:
    issue (dict): The issue data in dictionary format.
    auth (Tuple[str, str]): Authentication credentials for JIRA API.
    headers (dict): HTTP headers for API requests.

    Returns:
    dict: A dictionary containing processed data of the issue.
    """
    
    # Extracting basic issue data
    id_list = issue['id']
    key_list = issue['key']
    assignee_name = issue['fields']['assignee']['displayName']
    issue_type = issue['fields']['issuetype']['name']

    # Story points extraction
    story_points = issue['fields'].get('customfield_10029') or issue['fields'].get('customfield_10048')

    # Prepare URLs for additional data retrieval
    url_commits = f"{Config.BASE_URL}/rest/dev-status/latest/issue/detail?issueId={id_list}&applicationType=bitbucket&dataType=repository"
    url_changelog = f"{Config.BASE_URL}/rest/api/3/issue/{key_list}/changelog"
    issue_url = f"{Config.BASE_URL}/rest/api/3/issue/{key_list}"
    
    # Retrieve commits by issue ID
    commit_response = requests.get(url_commits, headers=headers, auth=auth)
    commit_response.raise_for_status()  # Handle HTTP errors
    dict_commits = commit_response.json()

    # Retrieve changelog by issue key
    changelog_response = requests.get(url_changelog, headers=headers, auth=auth)
    changelog_response.raise_for_status()  # Handle HTTP errors
    changelog = changelog_response.json()

    # Extract status changes from changelog
    status_changes = [
        item for item in changelog["values"]
        if any(change["field"] == "status" for change in item["items"])
    ]

    total_changelog = []
    for status_change in status_changes:
        created = status_change["created"]
        status_item = [item for item in status_change["items"] if item["field"] == "status"][0]
        to_status = status_item["toString"]
        total_changelog.append([created, to_status])

    # Retrieve creation date by issue key
    issue_response = requests.get(issue_url, headers=headers, auth=auth)
    issue_response.raise_for_status()  # Handle HTTP errors
    creation_date = issue_response.json()["fields"]["created"]

    # Count total commits
    total_commits = [len(repo["commits"]) for repo in dict_commits["detail"][0]["repositories"]]

    # Combine collected data into a result dict
    processed_issue_data = {
        "ID": id_list,
        "Key": key_list,
        "Display_Name": assignee_name,
        "Issue_Type": issue_type,
        "Story_Points": story_points,
        "Total_Commits": sum(total_commits),
        "Total_Repos": len(total_commits),
        "Commits_in_each_repo": total_commits,
        "Changelog_and_Time": total_changelog,
        "Create_Date": creation_date
    }

    return processed_issue_data


def generate_stats_for_project_version(project_name: str, version_name: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Generate statistics for a given project version in JIRA.

    Parameters:
    project_name (str): The name of the project.
    version_name (str): The name of the version.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: A tuple of three DataFrames, the first being the combined summary,
    the second being the original processed data, and the third being the summary statistics.
    """
    if not project_name or not version_name:
        raise ValueError("Invalid project name or version name")

    auth = get_jira_auth()

    try:
        issues = get_issues_by_project_version(project_name, version_name)

        if not issues:
            logger.warning(f"No issues found for {project_name} - {version_name}")
            # Return empty DataFrames or handle as needed
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

        df = pd.DataFrame(issues)
        processed_data, df = process_issues(issues, auth)

        # Check if DataFrame is empty after processing
        if df.empty:
            logger.warning(f"No data to process for {project_name} - {version_name}")
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

        # Group by 'Display_Name' and aggregate data
        summary = df.groupby('Display_Name').agg({
            'Issue_Type': 'count',
            'Story_Points': 'sum',
            'Total_Commits': 'sum',
        }).reset_index()

        # Pivot table for issue type counts
        issue_type_count = df.pivot_table(index='Display_Name', columns='Issue_Type', values='ID', aggfunc='count', fill_value=0)
        issue_type_count.columns = [f"{col}_Count" for col in issue_type_count.columns]
        
        combined_summary = pd.concat([summary.set_index('Display_Name'), issue_type_count], axis=1).reset_index()

        # Summary statistics
        summary_stats = combined_summary.describe().T
        summary_stats['Summary'] = combined_summary.sum(numeric_only=True)
        summary_stats = summary_stats[['mean', 'std', 'Summary']].rename(columns={'mean': 'Average', 'std': 'Standard Deviation'})

        # Rename 'index' column to 'Statistic'
        summary_stats.reset_index(inplace=True)
        summary_stats.rename(columns={'index': 'Statistic'}, inplace=True)

        return combined_summary, df, summary_stats

    except KeyError as e:
        logger.error(f"KeyError in processing {project_name} - {version_name}: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    except Exception as e:
        logger.error(f"Error in processing {project_name} - {version_name}: {e}")
        raise


















