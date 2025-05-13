"""
main.py

This script executes SQL queries from `.sql` files in a specified folder and generates 
an Excel report containing the query results.

The script connects to an Oracle database using credentials provided in the `config.py` file.
It retrieves queries from SQL files, executes them, and organizes the results into 
separate sheets in an Excel workbook. An introduction sheet is also included.

- The introduction sheet is generated from the `report_config/intro_text.txt` file. You may change
its contents, and the report text will updated.

Command-line arguments allow users to specify:
- The folder containing SQL files (`--sql_folder_path`, default: `./working_queries`)
- The output Excel file path (`--output_file`, default: `./report/Program_Report.xlsx`)

Usage:
    View the help screen
        sql-reporter
        sql-reporter --help

    Set your credentials
        sql-reporter set-user-credentials

    Generate the report
        sql-reporter execute

    Specify a different SQL folder:
        sql-reporter execute -p="./custom_queries"

    Specify a custom output file:
        sql-reporter execute -o="./output/custom_report.xlsx"

    Specify both SQL folder and output file:
        sql-reporter execute -p="./custom_queries" -o="./output/custom_report.xlsx"
"""


import click
import os
import argparse
import yaml
from pathlib import Path
from excel_report_maker import ExcelReportGenerator
from .report_generator import QueryRunner
from .config_utils import set_user_credentials, load_user_credentials, load_intro_text

# Introduction text lines.
INTRO_TEXT = load_intro_text('report_config/intro_text.txt')


@click.group()
def sql_reporter():
    """A tool for turning SQL queries into standardized Excel files.
    Powered by Python under the hood. Customize the Python code to make your reports
    exactly how you like them.
    """
    click.echo('Starting SQL-reporter...')


@sql_reporter.command('execute', short_help='Generate report from queries in SQL_FOLDER_PATH')
@click.option('-p', '--sql_folder_path', type=str, default='./working_queries', help="Path to the folder containing SQL files (default: ./working_queries)")
@click.option('-o', '--output_file',     type=str, default='./report/Program_Report.xlsx', help="Path to save the output Excel report (default: ./report/Program_Report.xlsx)")
def execute(sql_folder_path: str, output_file: str):
    '''Execute all of the SQL queries in --sql_folder_path and use the results to generate a report.
    The report will be saved to --output_file.
    '''
    # Set user credentials, if they haven't been set
    if not Path('report_config/user_config.yaml').exists():
        click.echo('You have not entered your configuration information yet.')
        user = click.prompt('Please enter your Oracle username', type=str)
        dsn = click.prompt('Please enter your Oracle Data Source Name (DSN)', type=str)
        lib_dir = click.prompt('Please enter your path to Oracle Instant Client libraries e.g. /path/to/oracle/lib', type=str)
        click.echo('Got your config')
        set_user_credentials(user, dsn, lib_dir)

    # Load user credentials
    user_credentials = load_user_credentials()

    # Ensure the output location exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Create an instance of QueryRunner
    runner = QueryRunner(**user_credentials)
    
    # Run the queries from all SQL files in the specified folder
    results = runner.run_queries_from_folder(sql_folder_path)

    # Create and generate the workbook
    report_generator = ExcelReportGenerator(results, INTRO_TEXT)
    report_generator.generate_workbook(output_file)


@sql_reporter.command('set-user-credentials')
@click.option('--user',
              prompt='Please enter your Oracle username',
              help='Your Oracle username')
@click.option('--dsn',
              prompt='Please enter your Oracle Data Source Name (DSN)',
              help='Your Oracle Data Source Name')
@click.option('--lib_dir',
              prompt='Please enter your path to Oracle Instant Client libraries e.g. /path/to/oracle/lib',
              help='Your path to Oracle Instance Client libraries')
def set_user_credentials_cli(user, dsn, lib_dir):
    '''Save or change your SQL credentials.'''
    click.echo('Updating your credentials...')
    set_user_credentials(user, dsn, lib_dir)
    click.echo('Credentials updated!')