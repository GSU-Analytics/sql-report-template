# SQL Report Template

## Overview
The **SQL Report Template** is a lightweight framework for executing SQL queries against an Oracle database and generating an Excel report with the results. Users can define SQL queries in separate `.sql` files, run them using the script, and receive a structured Excel report with multiple sheets corresponding to the queries.

## Features
- Executes multiple SQL queries from a specified folder.
- Connects to an Oracle database using `lightoracle`.
- Generates an Excel report with separate sheets for each SQL file.
- Automatically formats tables and includes an introduction sheet.
- Supports command-line arguments for input and output customization.

## Prerequisites
- Python 3.10+
- Oracle Instant Client
- Conda environment for dependency management

## Using This Repository as a Template
This repository is available as a GitHub template, allowing users to quickly generate a new project based on its structure.

### **Method 1: Use GitHub's Template Feature**
1. Go to the template repository: [SQL Report Template](https://github.com/GSU-Analytics/sql-report-template)
2. Click **"Use this template"** (green button).
3. Enter a name for your new repository and click **"Create repository from template"**.
4. Clone your new repository and follow the setup instructions.

### **Method 2: Clone the Repository Manually**
If you prefer to start with this template manually:
```bash
git clone https://github.com/GSU-Analytics/sql-report-template.git my-new-report
cd my-new-report
rm -rf .git  # Removes existing Git history
```
Then, initialize your new repository:
```bash
git init
```
Follow the installation steps to set up the environment and configure the database.

## Installation
### 1. Clone the Repository
```bash
git clone https://github.com/GSU-Analytics/sql-report-template.git
cd sql-report-template
```

### 2. Set Up the Environment
Using Conda:
```bash
conda env create -f environment.yml
conda activate sql-report-env
```

### 3. Install the Package
Using pip:
```bash
pip install -e .
```

- Note: This installs the package in "editable" mode. You can make any changes you want to the source code, in `/src/`, and your commandline scripts will reflect those changes.

### 3. Test your Install and Enter Your Credentials
Now, run:
```bash
sql-reporter --help
```

If you see something like the output below, you are ready to go:

```txt
Usage: sql-reporter [OPTIONS] COMMAND [ARGS]...

  A tool for turning SQL queries into standardized Excel files. Powered by
  Python under the hood. Customize the Python code to make your reports
  exactly how you like them.
```

Run the following command to enter your credentials:
```bash
sql-reporter set-user-credentials
```

## Usage
### Running the Report Generator
```bash
sql-reporter execute --sql_folder_path="./working_queries" --output_file="./report/Program_Report.xlsx"
```
#### Command-Line Arguments:
| Argument            | Description                                                   | Default                          |
|---------------------|---------------------------------------------------------------|----------------------------------|
| `--sql_folder_path` | Path to folder containing `.sql` files.                      | `./working_queries`              |
| `--output_file`     | Path to save the output Excel report.                        | `./report/Program_Report.xlsx`   |

### Example SQL Queries
Place SQL files inside `working_queries/`. Each file should contain at least one query and use `--` comments as query titles.
#### Example: `working_queries/sheet1.sql`
```sql
-- Cohort One Year Retention Rate
SELECT term, COUNT(*) AS student_count FROM student_data WHERE cohort_year = 2023 GROUP BY term;
```

## Report Output
The generated Excel report will include:
1. **Introduction Sheet** – Overview of the report.
2. **Query Sheets** – One sheet per SQL file, formatted as tables.

## File Structure
```
sql-report-template/
│── report_generator/
│   ├── __init__.py
│   ├── query_runner.py  # Executes SQL queries
│   ├── excel_report_generator.py  # Generates Excel reports
│── working_queries/
│   ├── sheet1.sql  # Example SQL file
│   ├── sheet2.sql
│── report/  # Output directory (ignored in .gitignore)
│── config.py  # Database configuration
│── main.py  # Script entry point
│── environment.yml  # Conda environment setup
│── README.md  # Documentation
```

## Troubleshooting
- **Oracle client errors?** Ensure that the Oracle Instant Client is installed and `lib_dir` is correctly set in `config.py`.
- **No output file generated?** Check that the SQL files are correctly formatted and contain queries.
- **Permission issues?** Ensure the script has permission to write to the output directory.

For further assistance, consult the `README.md` or submit an issue in the GitHub repository.

