# main.py

"""
The main script for executing the JIRA data processing and visualization pipeline.
This script orchestrates the fetching, processing, cleaning, and plotting of JIRA data.
"""

import sys
import time

from config import Config
from data_cleaning import transform_and_clean_data
from data_processing import generate_stats_for_project_version
from logger_config import logger
from plotting import plot_commits_per_issue


def main():
    logger.info("Application start")

    if not Config.PROJECT_NAMES or not Config.VERSION_NAMES:
        logger.error("PROJECT_NAMES and VERSION_NAMES must be configured in config.py")
        sys.exit(1)

    if len(Config.PROJECT_NAMES) != len(Config.VERSION_NAMES):
        logger.error("PROJECT_NAMES and VERSION_NAMES must have the same length")
        sys.exit(1)

    failed_projects = []
    successful_projects = []

    for project_name, version_name in zip(Config.PROJECT_NAMES, Config.VERSION_NAMES):
        try:
            start_time = time.time()
            logger.info(f"Processing {project_name} - {version_name}")

            summary_df, detailed_df, stats_df = generate_stats_for_project_version(project_name, version_name)
            detailed_df_cleaned = transform_and_clean_data(detailed_df, summary_df, stats_df, version_name)
            plot_commits_per_issue(detailed_df_cleaned, project_name, version_name)

            end_time = time.time()
            logger.info(f"Time taken for {project_name} - {version_name}: {end_time - start_time:.2f} seconds")
            logger.info(f"Successfully processed {project_name} - {version_name}")
            successful_projects.append(f"{project_name} - {version_name}")

        except Exception as e:
            logger.error(f"Error processing {project_name} - {version_name}: {e}", exc_info=True)
            failed_projects.append(f"{project_name} - {version_name}")
            # Continue processing remaining projects instead of exiting

    # Summary report
    logger.info("=" * 50)
    logger.info(f"Application end - Processed {len(Config.PROJECT_NAMES)} project(s)")
    logger.info(f"Successful: {len(successful_projects)}")
    logger.info(f"Failed: {len(failed_projects)}")

    if failed_projects:
        logger.warning(f"Failed projects: {', '.join(failed_projects)}")
        sys.exit(1)  # Exit with error code if any project failed

if __name__ == "__main__":
    main()
