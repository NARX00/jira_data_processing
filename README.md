# JIRA Data Processing Project

## Overview
This project provides tools for interacting with the JIRA API, processing data, and visualizing results. It includes functionality for fetching JIRA data, processing and cleaning the data, and generating insightful plots.

### Version
1.0.0

## Setup

### Requirements
- Python 3.6+
- Libraries: requests, pandas, matplotlib

### Installation
1. Clone the repository:
	- git clone [repository-url]

2. Navigate to the project directory:
	- cd [project-directory]

3. Install required libraries:
	- pip install requests pandas matplotlib
	
### Configuration
Update config.py with the necessary JIRA API configurations:

* JIRA Base URL (text file in credentials folder)
* API credentials (text file in credentials folder)

### Usage
Run the main.py script to execute the application:

* python3 -m main.py
	
### Project Structure
* `config.py` - Contains configuration settings.
* `data/` - Directory for storing output data files and plots.
* `data_cleaning.py` - Module for cleaning and transforming data.
* `data_processing.py` - Handles data extraction and processing.
* `jira_api.py` - Functions for JIRA API requests.
* `logger/` - Log files directory.
* `logger_config.py` - Logging configuration.
* `main.py` - Main script for running the application.
* `plotting.py` - Module for data visualization.
* `__init__.py` - Initializes the application as a package.

### Contributing
Contributions to this project are welcome. Please adhere to the following guidelines:

* Write tests for new features.
* Follow Python's PEP 8 style guide.
* Submit pull requests for review.