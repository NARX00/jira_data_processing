# plotting.py

"""
This module provides functionalities for plotting data, particularly focusing on visualizing 
the number of commits per issue in a given project version.
"""

import matplotlib.pyplot as plt
import pandas as pd
import os

from config import Config
from logger_config import logger

def plot_commits_per_issue(detailed_df: pd.DataFrame, project_name: str, version_name: str):
    """
    Creates a horizontal bar plot showing the number of commits per issue for a specified project and version.

    Parameters:
    detailed_df (pd.DataFrame): DataFrame containing issue details with commit counts.
    project_name (str): The name of the project.
    version_name (str): The name of the version.

    Returns:
    None: The function saves the plot as an image file and displays it.
    """
    try:
        if 'Total_Commits' in detailed_df.columns:
            # Sort the DataFrame based on 'Total_Commits' in ascending order
            sorted_df = detailed_df.sort_values(by='Total_Commits', ascending=True)

            x = sorted_df['Key']
            y = sorted_df['Total_Commits']
            titles = sorted_df['Key']

            # Dynamically adjust the figure height
            fig_height = max(8, 0.25 * len(titles))
            fig, ax = plt.subplots(figsize=(12, fig_height))
            bars = ax.barh(x, y, align='center')

            ax.set_yticks(range(len(titles)))
            ax.set_yticklabels(titles)
            ax.set_xlabel('Number of Commits')
            ax.set_ylabel('Issues')
            plt.title(f'Commits per Issue in {project_name}-{version_name}')

            total_keys = len(sorted_df)
            pl_total_commits = sum(sorted_df['Total_Commits'])
            ax.text(0.99, 0.01, f"Total Issues: {total_keys}", transform=ax.transAxes, ha="right", va="bottom", fontsize=12)
            ax.text(0.01, 0.01, f"Total Commits: {pl_total_commits}", transform=ax.transAxes, ha="left", va="bottom", fontsize=12)

            for bar, value in zip(bars, y):
                text_x_pos = bar.get_width()
                ax.text(text_x_pos, bar.get_y() + bar.get_height() / 2, f"{value}", va='center', ha='left')

            # Create a version-specific directory
            version_directory = os.path.join(Config.DATA_DIRECTORY, version_name)
            os.makedirs(version_directory, exist_ok=True)

            plt.tight_layout()

            # Save the plot in the version-specific directory
            plot_filename = os.path.join(version_directory, f'Commits_per_Issue_{project_name}_{version_name}.png')
            plt.savefig(plot_filename)

            logger.info(f"Plot saved to {plot_filename}")

        else:
            logger.warning(f"No data available to plot for {project_name} - {version_name}.")

    except Exception as e:
        logger.error(f"Error plotting commits per issue: {e}")
        raise
            