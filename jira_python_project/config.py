# config.py

"""
This module contains the configuration settings for the application.
"""

class Config:
    """
    Configuration constants for the application.
    """
    # Atlassian URL "https://xxx.atlassian.net" 
    with open("credentials\j_url.txt") as reader:
        BASE_URL = reader.readline() # organization url 
    
    # JIRA credentials - jira_api.py
    with open("credentials\email.txt") as reader:
        EMAIL = reader.readline() # organization user email
    
    with open("credentials\j_api.txt") as reader:
        API_KEY = reader.readline() # user API token
    
    # Version and Project Configuration - for main.py
    VERSION = "23" # # Jira fixVersion number only
    
    # if project name has space then use "''" 
    PROJECT_NAMES = [" ", " ", " "]
    
    # for example: product v{VERSION} 
    VERSION_NAMES = [f"xxx{VERSION}", ...]
    
    # Results storing folder
    DATA_DIRECTORY = "data"