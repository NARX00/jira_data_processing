# jira_api.py

"""
This module handles interactions with the JIRA API, including
authentication and making API requests.
"""

import json
import requests
from requests.exceptions import RequestException
from urllib.parse import urlparse

from config import Config
from logger_config import logger
from typing import List


def is_valid_url(url: str) -> bool:
    """
    Validates whether a given string is a valid URL.

    Parameters:
    url (str): The URL string to validate.

    Returns:
    bool: True if the URL is valid, False otherwise.
    """
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    
    except ValueError:
        return False
    
    
def get_jira_auth():
    """
    Retrieves JIRA authentication credentials.

    Returns:
        HTTPBasicAuth: A requests.auth.HTTPBasicAuth object for JIRA authentication.

    Raises:
        Exception: If there is an error in fetching decrypted email or token.
    """
    try:
        return requests.auth.HTTPBasicAuth(Config.get_email(), Config.get_api_key())

    except Exception as e:
        logger.error(f"Error getting JIRA auth: {e}")
        raise  # Re-raising the exception to be handled by the caller


def make_api_request(url: str, auth: tuple) -> dict:
    """
    Makes a GET request to a specified URL with provided authentication.

    Parameters:
        url (str): The URL for the API request.
        auth (tuple): The authentication tuple.

    Returns:
        dict: The JSON response from the API.

    Raises:
        ValueError: If the URL is invalid.
        RequestException: For issues related to the HTTP request.
        JSONDecodeError: If the response is not in JSON format.
    """
    try:
        if not is_valid_url(url):
            raise ValueError("Invalid URL provided")

        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers, auth=auth, timeout=Config.REQUEST_TIMEOUT)
        response.raise_for_status()

        return response.json()
    except RequestException as e:
        logger.error(f"HTTP request error: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from response: {e}")
        raise


def get_issues_by_project_version(project_name: str, version_name: str) -> List[dict]:
    auth = get_jira_auth()

    if not project_name or not version_name:
        logger.error("Invalid project or version name")
        return []

    jql_query = f"project={project_name} AND fixversion='{version_name}' AND status=done AND issuetype NOT IN (Epic, Automation)"
    jql_query_encoded = requests.utils.quote(jql_query)

    start_at = 0
    max_results = 100 # hard Jira limit for number of issue per on API call
    all_issues = []

    while True:
        url = f"{Config.get_base_url()}/rest/api/3/search?jql={jql_query_encoded}&startAt={start_at}&maxResults={max_results}"
        logger.debug(f"Making API request to URL: {url}")

        try:
            response = make_api_request(url, auth)
            issues = response.get('issues', [])
            
            if not issues:
                break  # Break the loop if no more issues are returned

            all_issues.extend(issues)
            start_at += len(issues)

        except RequestException as e:
            logger.error(f"Error making API request: {e}")
            break  # Exit the loop on error
        
        except KeyError as e:
            logger.error(f"Key error in parsing response: {e}")
            break  # Exit the loop on error

    return all_issues
