# config.py

"""
This module contains the configuration settings for the application.
"""
import os

class Config:
    """
    Configuration constants for the application.
    """
    # Construct path to credentials directory relative to this config file
    # __file__ is the path to the current file (jira_python_project/config.py)
    # os.path.dirname(__file__) is jira_python_project/
    # os.path.join(os.path.dirname(__file__), '..', 'credentials') is ../credentials/
    CREDENTIALS_DIR = os.path.join(os.path.dirname(__file__), '..', 'credentials')

    JIRA_URL_FILE = os.path.join(CREDENTIALS_DIR, 'j_url.txt')
    EMAIL_FILE = os.path.join(CREDENTIALS_DIR, 'email.txt')
    API_TOKEN_FILE = os.path.join(CREDENTIALS_DIR, 'j_api.txt')

    # Atlassian URL "https://xxx.atlassian.net"
    try:
        with open(JIRA_URL_FILE) as reader:
            BASE_URL = reader.readline().strip() # organization url
    except FileNotFoundError:
        BASE_URL = "YOUR_JIRA_BASE_URL" # Default or placeholder
        print(f"Warning: {JIRA_URL_FILE} not found. Using placeholder BASE_URL.")

    # JIRA credentials - jira_api.py
    try:
        with open(EMAIL_FILE) as reader:
            EMAIL = reader.readline().strip() # organization user email
    except FileNotFoundError:
        EMAIL = "YOUR_EMAIL" # Default or placeholder
        print(f"Warning: {EMAIL_FILE} not found. Using placeholder EMAIL.")

    try:
        with open(API_TOKEN_FILE) as reader:
            API_KEY = reader.readline().strip() # user API token
    except FileNotFoundError:
        API_KEY = "YOUR_API_KEY" # Default or placeholder
        print(f"Warning: {API_TOKEN_FILE} not found. Using placeholder API_KEY.")
    
    # Version and Project Configuration - for main.py
    VERSION = "23" # # Jira fixVersion number only
    
    # User-specific configuration: Populate these lists before execution.
    # if project name has space then use "''" 
    PROJECT_NAMES = []
    
    # for example: product v{VERSION} 
    VERSION_NAMES = []
    
    # Results storing folder
    DATA_DIRECTORY = "data"