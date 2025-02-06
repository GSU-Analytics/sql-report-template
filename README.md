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
- Conda for dependency management

## Installation
### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/sql-report-template.git
cd sql-report-template
```

### 2. Set Up the Environment
Using Conda:
```bash
conda env create -f environment.yml
conda activate sql-report-env
```
Using pip (alternative method):
```bash
pip install -r requirements.txt
```

### 3. Configure Database Connection
Edit the `config_example.py` file to include your Oracle database credentials. Save the file as `config.py`.
```python
# config.py
user = "your_username"
dsn = "your_dsn"
lib_dir = "/path/to/oracle/lib"
```
Alternatively, you can store credentials in a `.env` file and modify `config.py` to read from environment variables.

## Usage
### Running the Report Generator
```bash
python main.py --sql_folder_path="./working_queries" --output_file="./report/Program_Report.xlsx"
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

