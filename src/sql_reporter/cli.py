"""
cli.py

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
        sql-reporter set-user-credentials .my_special_credentials.yaml

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
from pathlib import Path
from sql_reporter.main import main as make_report
from sql_reporter.config_utils import set_user_credentials, load_intro_text


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
@click.option('--intro_path',            type=str, default='./report_config/intro_text.txt', help="Path to file containing text for the introduction sheet.")
@click.option('--config_file',           type=str, default='.user_config.yaml', help='Path to your configuration file. Will be created if it does not exist.')
def execute(sql_folder_path: str, output_file: str, intro_path: str, config_file: str):
    '''Execute all of the SQL queries in --sql_folder_path and use the results to generate a report.
    The report will be saved to --output_file.
    '''
    # Set user credentials, if they haven't been set
    if not Path(config_file).exists():
        click.echo('You have not entered your configuration information yet.')
        user = click.prompt('Please enter your Oracle username', type=str)
        dsn = click.prompt('Please enter your Oracle Data Source Name (DSN)', type=str)
        lib_dir = click.prompt('Please enter your path to Oracle Instant Client libraries e.g. /path/to/oracle/lib', type=str)
        set_user_credentials(user, dsn, lib_dir, config_file)
        click.echo(f'Configuration information saved to {config_file}.')
    # Introduction text lines.
    intro_path = Path(intro_path) 
    try:
        intro_text = load_intro_text(intro_path)
    except Exception as e:
        click.echo(f'Could not load your file: {str(intro_path)}')
        intro_text = 'Here is some sample text. \n\n Create an introductory text file and load it with --intro_path to replace this.'

    # Run the report generator
    make_report(sql_folder_path, output_file, intro_text)
    click.echo('Your report has been generated!')


@sql_reporter.command('set-user-credentials')
@click.argument('config_file')
@click.option('--user',
              prompt='Please enter your Oracle username',
              help='Your Oracle username')
@click.option('--dsn',
              prompt='Please enter your Oracle Data Source Name (DSN)',
              help='Your Oracle Data Source Name')
@click.option('--lib_dir',
              prompt='Please enter your path to Oracle Instant Client libraries e.g. /path/to/oracle/lib',
              help='Your path to Oracle Instance Client libraries')
def set_user_credentials_cli(user, dsn, lib_dir, config_file='.user_config.yaml'):
    '''Save or change your SQL credentials for a given config_file.
    '''
    click.echo('Updating your credentials...')
    set_user_credentials(user, dsn, lib_dir, config_path=config_file)
    click.echo('Credentials updated!')


if __name__ == '__main__':
    sql_reporter()