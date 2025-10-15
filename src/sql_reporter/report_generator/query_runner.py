# query_runner.py

import os
import glob
from pathlib import Path
from lightoracle import LightOracleConnection

class QueryRunner:
    def __init__(self, user, dsn, lib_dir):
        """
        Initialize the QueryRunner with the necessary Oracle connection parameters.
        """
        self.oracle_conn = LightOracleConnection(user, dsn, lib_dir)
        # This attribute will temporarily store query results per file.
        self.results = {}

    def parse_sql_file(self, file_path):
        """
        Parse a SQL file containing multiple queries.
        
        The file should have query titles provided as comment lines that start with '--'
        immediately preceding the query block. Each query block should be terminated by a
        semicolon. The semicolon is stripped out before executing the query.
        
        Args:
            file_path (str): Path to the SQL file.
            
        Returns:
            dict: A dictionary where keys are query titles and values are query strings.
        """
        queries = {}
        current_title = None
        current_query_lines = []
        
        with open(file_path, 'r') as file:
            for line in file:
                stripped_line = line.strip()
                # Skip empty lines.
                if not stripped_line:
                    continue

                # If the line is a comment, treat it as the title for the next query.
                if stripped_line.startswith('--'):
                    # If we already have collected query lines for a previous query,
                    # finish that query and store it.
                    if current_query_lines and current_title:
                        query = '\n'.join(current_query_lines).strip()
                        # Remove trailing semicolon if it exists.
                        if query.endswith(';'):
                            query = query[:-1].strip()
                        queries[current_title] = query
                        current_query_lines = []
                    # Set the new title (remove the '--' marker).
                    current_title = stripped_line.lstrip('-').strip()
                else:
                    # This line is part of a query.
                    # Check if the line (or a portion of it) ends with a semicolon.
                    if ';' in stripped_line:
                        # Handle two cases:
                        # 1. The semicolon is the only token on the line.
                        if stripped_line == ';':
                            # End-of-query marker; do nothing else.
                            continue
                        # 2. The semicolon is at the end of the line.
                        if stripped_line.endswith(';'):
                            # Append the line without the trailing semicolon.
                            current_query_lines.append(stripped_line[:-1].strip())
                            # Join the collected lines to form the full query.
                            query = '\n'.join(current_query_lines).strip()
                            queries[current_title] = query
                            current_query_lines = []
                        else:
                            # If a semicolon appears mid-line, split on the semicolon.
                            parts = stripped_line.split(';')
                            # Use the part before the semicolon.
                            current_query_lines.append(parts[0].strip())
                            query = '\n'.join(current_query_lines).strip()
                            queries[current_title] = query
                            current_query_lines = []
                            # If there is any text after the semicolon, treat it as the start
                            # of a new query (or continuation); add it to current_query_lines.
                            if len(parts) > 1 and parts[1].strip():
                                current_query_lines.append(parts[1].strip())
                    else:
                        # No semicolon in the line; simply add it to the current query.
                        current_query_lines.append(stripped_line)
            # After processing all lines, check if there’s any unfinished query.
            if current_query_lines and current_title:
                query = '\n'.join(current_query_lines).strip()
                if query.endswith(';'):
                    query = query[:-1].strip()
                queries[current_title] = query
                
        return queries

    def run_queries_from_file(self, file_path):
        """
        Parse the provided SQL file, execute each query against the Oracle database,
        and store the resulting dataframes.
        
        Args:
            file_path (str): Path to the SQL file.
            
        Returns:
            dict: A dictionary where the keys are query titles and the values are
                  the resulting Pandas dataframes.
        """
        # Reset the results for this file.
        self.results = {}
        queries = self.parse_sql_file(file_path)
        for title, query in queries.items():
            print(f"Running query: {title} (from file {os.path.basename(file_path)})")
            # Execute the query. (The semicolon has been removed already.)
            df = self.oracle_conn.execute_query(query)
            self.results[title] = df
        return self.results

    def run_queries_from_folder(self, folder_path):
        """
        Iterates over all SQL files in the given folder, runs the queries for each file,
        and stores the results in a nested dictionary. The keys of the outer dictionary
        are the file names (without extension) and the values are dictionaries mapping query
        titles to dataframes.
        
        Args:
            folder_path (str): Path to the folder containing SQL files.
            
        Returns:
            dict: A dictionary where each key is a sheet name (derived from the file name)
                  and each value is a dictionary of query results.
        """
        all_results = {}
        # Use glob to find all .sql files in the folder.
        sql_files = sorted(Path(folder_path).glob('*.sql'))
        for file_path in sql_files:
            # Use the file name (without extension) as the sheet name.
            sheet_name = file_path.stem
            file_results = self.run_queries_from_file(file_path)
            # Make a copy of the results for this file.
            all_results[sheet_name] = file_results.copy()
        return all_results
