import os
from pathlib import Path
from excel_report_maker import ExcelReportGenerator
from sql_reporter.report_generator import QueryRunner
from sql_reporter.config_utils import load_user_credentials


def main(sql_folder_path: str, output_file: str, intro_text: None):
    '''Execute all of the SQL queries in sql_folder_path and use the results to generate a report.
    The report will be saved to output_file.
    '''
    # Load user credentials
    user_credentials = load_user_credentials()

    # Ensure the output location exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Create an instance of QueryRunner
    runner = QueryRunner(**user_credentials)
    
    # Run the queries from all SQL files in the specified folder
    results = runner.run_queries_from_folder(sql_folder_path)

    # Create and generate the workbook
    report_generator = ExcelReportGenerator(results, intro_text)
    report_generator.generate_workbook(output_file)