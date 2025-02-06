"""
config.py

This file contains database connection settings for the SQL report generator.

Modify these values to match your Oracle database credentials.

Usage:
    - Ensure this file is correctly configured before running `main.py`.
    - DO NOT commit this file to version control if it contains sensitive credentials.
"""

# Oracle database credentials
user = "your_username"  # Replace with your Oracle username
dsn = "your_dsn"        # Replace with your Oracle Data Source Name (DSN)
lib_dir = "/path/to/oracle/lib"  # Replace with the path to Oracle Instant Client libraries
