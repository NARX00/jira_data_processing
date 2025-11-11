# Changelog

All notable changes to the JIRA Data Processing project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed in Critical Fixes Branch (2025-11-11)

#### Security & Reliability
- **CRITICAL:** Fixed path separator issues in config.py using `os.path.join()` for cross-platform compatibility
- **CRITICAL:** Moved credential file reading from class definition time to class methods for proper resource management
- **CRITICAL:** Added timeout parameter (30s) to all HTTP requests to prevent infinite hangs
- **CRITICAL:** Fixed null assignee handling to prevent crashes on unassigned JIRA issues

#### Bug Fixes
- Fixed syntax error in plotting.py where `if 'Total_Commits' in detailed_df` should check `detailed_df.columns`
- Fixed error handling in main.py to continue processing remaining projects instead of exiting on first failure
- Fixed potential IndexError in data_processing.py by validating API response structure before access
- Fixed typo in logger_config.py header comment (looger → logger)

#### Improvements
- Removed accidental `data_processing.pyt` file
- Removed duplicate directory creation code in plotting.py
- Removed commented-out dead code in plotting.py
- Added better error messages with full exception info using `exc_info=True`
- Added configuration validation on startup (PROJECT_NAMES and VERSION_NAMES length check)
- Added summary report at end of execution showing successful and failed projects
- Config methods now return stripped strings (remove trailing whitespace/newlines)

#### Added
- Created `requirements.txt` with pinned dependency versions
  - requests >= 2.31.0
  - pandas >= 2.0.0
  - matplotlib >= 3.7.0
- Created comprehensive `REMEDIATION_PLAN.md` with phased improvement roadmap
- Added `REQUEST_TIMEOUT` configuration option (default: 30 seconds)
- Added TODO comments in config.py for required configuration
- Added helpful logging message when plot is saved

### Changed
- `Config.BASE_URL`, `Config.EMAIL`, `Config.API_KEY` changed from class attributes to class methods
  - Now called as `Config.get_base_url()`, `Config.get_email()`, `Config.get_api_key()`
- `Config.PROJECT_NAMES` and `Config.VERSION_NAMES` changed to empty lists with TODO comments
  - Prevents ellipsis syntax error
  - Requires explicit user configuration
- Error handling strategy changed to fail-late instead of fail-fast
  - All projects processed even if some fail
  - Exit code 1 returned only if any project failed

### Files Modified
- jira_python_project/config.py
- jira_python_project/jira_api.py
- jira_python_project/data_processing.py
- jira_python_project/main.py
- jira_python_project/plotting.py
- jira_python_project/logger_config.py

### Files Added
- requirements.txt
- REMEDIATION_PLAN.md
- CHANGELOG.md

### Files Removed
- jira_python_project/data_processing.pyt (accidental file)

---

## [1.0.0] - Initial Release

### Added
- Initial project structure
- JIRA API integration for fetching issues
- Data processing pipeline for JIRA data
- Data cleaning and transformation utilities
- Visualization plotting for commits per issue
- Logging infrastructure with file rotation
- Basic configuration management
- README with setup instructions

### Features
- Fetch issues from JIRA Cloud by project and version
- Process issue data including commits, story points, and changelogs
- Generate summary statistics per assignee
- Create visualizations of commits per issue
- Export data to CSV format
- Support for multiple projects and versions in batch

---

## Migration Guide

### Upgrading to Critical Fixes Branch

If you're using the original version of this code, follow these steps to upgrade:

1. **Update config.py usage:**
   ```python
   # OLD (will not work):
   url = f"{Config.BASE_URL}/rest/api/3/search"

   # NEW:
   url = f"{Config.get_base_url()}/rest/api/3/search"
   ```

2. **Configure PROJECT_NAMES and VERSION_NAMES:**
   ```python
   # In config.py, replace:
   PROJECT_NAMES = []  # TODO: Configure
   VERSION_NAMES = []  # TODO: Configure

   # With your actual values:
   PROJECT_NAMES = ["MyProject", "OtherProject"]
   VERSION_NAMES = ["v1.23", "v1.23"]
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Update credential file paths (if needed):**
   - The code now uses forward slashes and `os.path.join()`
   - Credential files should be in `credentials/` directory:
     - `credentials/j_url.txt`
     - `credentials/email.txt`
     - `credentials/j_api.txt`

5. **Test your configuration:**
   ```bash
   python3 -m jira_python_project.main
   ```

---

## Breaking Changes

### Critical Fixes Branch
- `Config.BASE_URL`, `Config.EMAIL`, `Config.API_KEY` are now methods, not attributes
- `Config.PROJECT_NAMES` and `Config.VERSION_NAMES` are now empty by default (must be configured)
- Application now continues on errors instead of exiting immediately

---

## Known Issues

### Current Limitations
- No rate limiting on API calls (see REMEDIATION_PLAN.md Phase 2.2)
- No retry logic for transient failures (see REMEDIATION_PLAN.md Phase 2.2)
- Credentials stored in plain text files (see REMEDIATION_PLAN.md Phase 2.1)
- No test coverage (see REMEDIATION_PLAN.md Phase 3.1)
- Custom field IDs hardcoded (customfield_10029, customfield_10048)

---

## Contributors
- Initial development team
- Claude (AI assistant) - Critical fixes and remediation plan

---

[Unreleased]: https://github.com/NARX00/jira_data_processing/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/NARX00/jira_data_processing/releases/tag/v1.0.0
