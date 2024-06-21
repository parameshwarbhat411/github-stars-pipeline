from load.extract_load import ExtractLoad
import logging.config
import os

logging.config.fileConfig('temp.conf')

if __name__ == '__main__':
    # Get the data path
    data_path = os.path.join(os.getcwd(), 'data/gharchive_sample')
    logging.info(f"Data Path: {data_path}")

    # Initialize ExtractLoad object
    extract_load_obj = ExtractLoad('file.db')
    extract_load_obj.load_json(data_path)