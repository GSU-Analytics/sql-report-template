"""
main.py

This script executes SQL queries from `.sql` files in a specified folder and generates 
an Excel report containing the query results.

The script connects to an Oracle database using credentials provided in the `config.py` file.
It retrieves queries from SQL files, executes them, and organizes the results into 
separate sheets in an Excel workbook. An introduction sheet is also included.

Command-line arguments allow users to specify:
- The folder containing SQL files (`--sql_folder_path`, default: `./working_queries`)
- The output Excel file path (`--output_file`, default: `./report/Program_Report.xlsx`)

Usage:
    Run with default settings:
        python main.py

    Specify a different SQL folder:
        python main.py --sql_folder_path="./custom_queries"

    Specify a custom output file:
        python main.py --output_file="./output/custom_report.xlsx"

    Specify both SQL folder and output file:
        python main.py --sql_folder_path="./custom_queries" --output_file="./output/custom_report.xlsx"

Dependencies:
    - Python 3.10+
    - pandas
    - openpyxl
    - lightoracle (custom package for Oracle database connections)

Modules:
    - argparse: Parses command-line arguments.
    - os: Handles file and directory operations.
    - config: Contains database connection details.
    - report_generator.QueryRunner: Executes SQL queries and retrieves results.
    - report_generator.ExcelReportGenerator: Creates the Excel report.
"""


import os
import argparse
from config import user, dsn, lib_dir
from report_generator import QueryRunner, ExcelReportGenerator

# Introduction text lines.
intro_text = [
    "This workbook contains detailed enrollment and retention reports for the program.",
    "Report generated on: 02-04-2025",
    "",
    "Contents:",
    "Each SQL file in the specified folder has been processed into its own sheet."
]

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Run SQL queries and generate an Excel report.")
    parser.add_argument(
        "--sql_folder_path", 
        type=str, 
        default="./working_queries", 
        help="Path to the folder containing SQL files (default: ./working_queries)"
    )
    parser.add_argument(
        "--output_file", 
        type=str, 
        default="./report/Program_Report.xlsx", 
        help="Path to save the output Excel report (default: ./report/Program_Report.xlsx)"
    )
    
    args = parser.parse_args()
    
    # Ensure the report directory exists
    os.makedirs(os.path.dirname(args.output_file), exist_ok=True)

    # Create an instance of QueryRunner
    runner = QueryRunner(user, dsn, lib_dir)
    
    # Run the queries from all SQL files in the specified folder
    results = runner.run_queries_from_folder(args.sql_folder_path)

    # Create and generate the workbook
    report_generator = ExcelReportGenerator(results, intro_text)
    report_generator.generate_workbook(args.output_file)

if __name__ == '__main__':
    main()
