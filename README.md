# JIRA Cloud Data Processing Project

## Overview
This project provides tools for interacting with the JIRA API, processing data, and visualizing results. It includes functionality for fetching JIRA data, processing and cleaning the data, and generating insightful plots.

### Version
1.0.1-dev (Critical Fixes)

## Features
- ✅ Fetch issues from JIRA Cloud by project and version
- ✅ Process issue data including commits, story points, and changelogs
- ✅ Generate summary statistics per assignee
- ✅ Create visualizations of commits per issue
- ✅ Export data to CSV format
- ✅ Support for multiple projects and versions in batch processing
- ✅ Comprehensive error handling and logging
- ✅ Cross-platform compatibility (Windows, Linux, macOS)

## Setup

### Requirements
- **Python 3.6+** (Python 3.8+ recommended)
- See `requirements.txt` for library dependencies

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NARX00/jira_data_processing.git
   cd jira_data_processing
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create credentials directory:**
   ```bash
   mkdir credentials
   ```

4. **Create credential files:**
   Create the following text files in the `credentials/` directory:

   - `credentials/j_url.txt` - Your JIRA base URL (e.g., `https://yourcompany.atlassian.net`)
   - `credentials/email.txt` - Your JIRA email address
   - `credentials/j_api.txt` - Your JIRA API token ([Generate here](https://id.atlassian.com/manage-profile/security/api-tokens))

   **Example:**
   ```bash
   echo "https://yourcompany.atlassian.net" > credentials/j_url.txt
   echo "your.email@company.com" > credentials/email.txt
   echo "your-api-token-here" > credentials/j_api.txt
   ```

   ⚠️ **Security Note:** Never commit credential files to version control! They are already in `.gitignore`.

### Configuration

1. **Edit `jira_python_project/config.py`:**

   Update the following configuration variables:
   ```python
   # Version number (Jira fixVersion)
   VERSION = "23"

   # List of project names
   # Use quotes around names with spaces
   PROJECT_NAMES = ["ProjectA", "Project B", "ProjectC"]

   # List of version names corresponding to each project
   # Must be same length as PROJECT_NAMES
   VERSION_NAMES = [f"Product A v{VERSION}", f"Product B v{VERSION}", f"Product C v{VERSION}"]
   ```

2. **Adjust timeout settings (optional):**
   ```python
   # Request timeout in seconds (default: 30)
   REQUEST_TIMEOUT = 30
   ```

### Usage

Run the application from the project root directory:

```bash
python3 -m jira_python_project.main
```

Or if your Python 3 is the default:
```bash
python -m jira_python_project.main
```

### Output

The application creates the following outputs in the `data/` directory:

```
data/
└── [version_name]/
    ├── [version_name]-detailed.csv    # Detailed issue information
    ├── [version_name]-summary.csv     # Summary statistics per assignee
    ├── [version_name]-stats.csv       # Aggregate statistics
    └── Commits_per_Issue_[project]_[version].png  # Visualization
```

### Logs

Application logs are stored in the `logger/` directory:
- `logger/application.log` - Main log file (rotates at 10MB, keeps 5 backups)
	
## Project Structure

```
jira_data_processing/
├── jira_python_project/          # Main application package
│   ├── __init__.py               # Package initializer
│   ├── config.py                 # Configuration settings
│   ├── main.py                   # Main entry point
│   ├── jira_api.py               # JIRA API interaction functions
│   ├── data_processing.py        # Data extraction and processing
│   ├── data_cleaning.py          # Data cleaning and transformation
│   ├── plotting.py               # Data visualization
│   └── logger_config.py          # Logging configuration
├── credentials/                  # API credentials (gitignored)
│   ├── j_url.txt                 # JIRA base URL
│   ├── email.txt                 # User email
│   └── j_api.txt                 # API token
├── data/                         # Output directory (gitignored)
├── logger/                       # Log files (gitignored)
├── requirements.txt              # Python dependencies
├── CHANGELOG.md                  # Version history
├── REMEDIATION_PLAN.md           # Improvement roadmap
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## Troubleshooting

### Common Issues

**1. FileNotFoundError: credential file not found**
- Ensure you've created the `credentials/` directory
- Verify all three credential files exist and contain valid data
- Check that file names match exactly: `j_url.txt`, `email.txt`, `j_api.txt`

**2. Authentication errors**
- Verify your JIRA URL is correct (include `https://`)
- Ensure your API token is valid and not expired
- Confirm your email address matches your JIRA account

**3. No issues found / empty results**
- Check that PROJECT_NAMES and VERSION_NAMES are configured correctly
- Verify the project names and version names exist in your JIRA instance
- Ensure you have permission to view the projects
- Check that issues exist with the specified fixVersion and are in "Done" status

**4. Timeout errors**
- Increase `REQUEST_TIMEOUT` in config.py if you have slow network
- Check your internet connection
- Verify JIRA instance is accessible

**5. Module import errors**
- Ensure you're running from the project root directory
- Use `python3 -m jira_python_project.main` (not `python main.py`)
- Verify all dependencies are installed: `pip install -r requirements.txt`

### Debug Mode

To enable debug logging, set the `LOG_LEVEL` environment variable:

```bash
# Linux/Mac
export LOG_LEVEL=DEBUG
python3 -m jira_python_project.main

# Windows
set LOG_LEVEL=DEBUG
python -m jira_python_project.main
```

## Limitations

- Custom field IDs are hardcoded (customfield_10029, customfield_10048)
- Only fetches issues with status "Done"
- Excludes Epic and Automation issue types
- Requires Bitbucket integration for commit data
- No retry logic for failed API calls (yet - see REMEDIATION_PLAN.md)

## Roadmap

See [REMEDIATION_PLAN.md](REMEDIATION_PLAN.md) for detailed improvement plans:
- **Phase 1:** ✅ Critical fixes (COMPLETED)
- **Phase 2:** Environment variables, retry logic, rate limiting
- **Phase 3:** Testing, documentation, performance improvements
- **Phase 4:** Web dashboard, automation, advanced features

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository** and create a feature branch
2. **Write tests** for new features (target: 70%+ coverage)
3. **Follow PEP 8** style guide (use `black` for formatting)
4. **Update documentation** (README, docstrings, CHANGELOG)
5. **Submit a pull request** with a clear description

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy

# Run tests
pytest

# Format code
black jira_python_project/

# Lint code
flake8 jira_python_project/
```

## License

[Add your license here]

## Support

- **Issues:** Report bugs via [GitHub Issues](https://github.com/NARX00/jira_data_processing/issues)
- **Documentation:** See inline docstrings and comments
- **Changelog:** See [CHANGELOG.md](CHANGELOG.md)

## Acknowledgments

- Built with [requests](https://requests.readthedocs.io/), [pandas](https://pandas.pydata.org/), and [matplotlib](https://matplotlib.org/)
- Uses [JIRA REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)

---

**Last Updated:** 2025-11-11 | **Version:** 1.0.1-dev
