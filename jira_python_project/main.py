# main.py

"""
The main script for executing the JIRA data processing and visualization pipeline.
This script orchestrates the fetching, processing, cleaning, and plotting of JIRA data.
"""

import time

from config import Config
from data_cleaning import transform_and_clean_data
from data_processing import generate_stats_for_project_version
from logger_config import logger
from plotting import plot_commits_per_issue


def main():
    logger.info("Application start")
    
    for project_name, version_name in zip(Config.PROJECT_NAMES, Config.VERSION_NAMES):
        try:
            start_time = time.time()
            logger.info(f"Processing {project_name} - {version_name}")

            summary_df, detailed_df, stats_df = generate_stats_for_project_version(project_name, version_name)
            detailed_df_cleaned = transform_and_clean_data(detailed_df, summary_df, stats_df, version_name)
            plot_commits_per_issue(detailed_df_cleaned, project_name, version_name)
            
            end_time = time.time()
            logger.info(f"Time taken for {project_name} - {version_name}: {end_time - start_time} seconds")
            logger.info(f"Successfully processed {project_name} - {version_name}")
       
        except Exception as e:
            logger.error(f"Error processing {project_name} - {version_name}: {e}")
            # Continue to the next project/version if an error occurs
            continue
    logger.info("Application end")

if __name__ == "__main__":
    main()
