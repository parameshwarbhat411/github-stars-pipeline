import gzip
import shutil
import tempfile
import os
import duckdb
from datetime import datetime
import logging as logger
import glob

class ExtractLoad:
    def __init__(self, db_path):
        self.db_path = db_path

    def initial_load(self, source_dir, tmp_dir_name):

        # Unzip .json.gz files to the temporary directory
        for filename in os.listdir(source_dir):
            if filename.endswith('.json.gz'):
                source_file = os.path.join(source_dir, filename)
                dest_file = os.path.join(tmp_dir_name, filename[:-3])  # Remove .gz extension
                with gzip.open(source_file, 'rb') as f_in:
                    with open(dest_file, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)

        json_files = glob.glob(f"{tmp_dir_name}/*.json")

        # Count the number of JSON files
        num_json_files = len(json_files)

        logger.info(f"Number of JSON files: {num_json_files} in {tmp_dir_name}")

        con = duckdb.connect(self.db_path)
        con.execute("CREATE SCHEMA IF NOT EXISTS source")
        logger.info("Performing initial load...")
        # Initial load: load all JSON files
        con.execute(f"""
        CREATE TABLE source.src_gharchive AS
        SELECT *, NOW() AS loaded_at FROM read_json_auto('{tmp_dir_name}/*.json')
        """)
        con.close()

    def incremental_load(self, source_dir, tmp_dir_name):
        con = duckdb.connect(self.db_path)
        con.execute("CREATE SCHEMA IF NOT EXISTS source")
        logger.info("Performing incremental load...")

        # Incremental load: load only new JSON files
        result = con.execute("SELECT MAX(loaded_at) FROM source.src_gharchive").fetchone()
        max_loaded_at = result[0].replace(tzinfo=None) if result[0] is not None else datetime.min

        for filename in os.listdir(source_dir):
            if filename.endswith('.json.gz'):
                try:
                    # Extract the timestamp from the filename
                    file_timestamp_str = filename.split('.')[0]
                    file_timestamp = datetime.strptime(file_timestamp_str, '%Y-%m-%d')

                    # Only process files newer than the last load time
                    if file_timestamp > max_loaded_at:
                        source_file = os.path.join(source_dir, filename)
                        dest_file = os.path.join(tmp_dir_name, filename[:-3])  # Remove .gz extension

                        with gzip.open(source_file, 'rb') as f_in, open(dest_file, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                            logger.info(f'Unzipped {filename} to {dest_file}')

                        # Insert new data into the table
                        con.execute(f"""
                        INSERT INTO source.src_gharchive 
                        SELECT *, NOW() AS loaded_at FROM read_json_auto('{dest_file}')
                        """)
                except Exception as e:
                    logger.error(f"Error processing file {filename}: {e}")
        con.close()

    def load_json(self, source_dir):
        try:
            if not os.path.exists(source_dir):
                raise FileNotFoundError(f"Source directory not found: {source_dir}")

            with tempfile.TemporaryDirectory() as tmp_dir_name:
                logger.info(f'Created temporary directory: {tmp_dir_name}')

                con = duckdb.connect(self.db_path)

                # Check if the table exists by attempting to select from it
                table_exists = True
                try:
                    con.execute("SELECT 1 FROM source.src_gharchive LIMIT 1")
                except duckdb.Error:
                    table_exists = False

                con.close()

                if not table_exists:
                    self.initial_load(source_dir, tmp_dir_name)
                else:
                    self.incremental_load(source_dir, tmp_dir_name)

        except duckdb.FatalException as e:
            logger.error(e)
