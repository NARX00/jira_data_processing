# config.py

"""
This module contains the configuration settings for the application.
"""

import os


class Config:
    """
    Configuration constants for the application.
    """
    # Base credentials directory
    CREDENTIALS_DIR = "credentials"

    # Atlassian URL "https://xxx.atlassian.net"
    @classmethod
    def _read_credential_file(cls, filename):
        """Helper method to safely read credential files."""
        filepath = os.path.join(cls.CREDENTIALS_DIR, filename)
        try:
            with open(filepath, 'r') as reader:
                return reader.readline().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Credential file not found: {filepath}")
        except Exception as e:
            raise Exception(f"Error reading credential file {filepath}: {e}")

    @classmethod
    def get_base_url(cls):
        """Get the JIRA base URL from credentials."""
        return cls._read_credential_file("j_url.txt")

    @classmethod
    def get_email(cls):
        """Get the user email from credentials."""
        return cls._read_credential_file("email.txt")

    @classmethod
    def get_api_key(cls):
        """Get the API key from credentials."""
        return cls._read_credential_file("j_api.txt")

    # Version and Project Configuration - for main.py
    VERSION = "23"  # Jira fixVersion number only

    # if project name has space then use quotes in the list
    # Example: PROJECT_NAMES = ["ProjectA", "Project B", "ProjectC"]
    PROJECT_NAMES = []  # TODO: Configure your project names here

    # for example: product v{VERSION}
    # Example: VERSION_NAMES = [f"ProductA v{VERSION}", f"ProductB v{VERSION}"]
    VERSION_NAMES = []  # TODO: Configure your version names here

    # Results storing folder
    DATA_DIRECTORY = "data"

    # Request timeout in seconds (default: 30)
    REQUEST_TIMEOUT = 30