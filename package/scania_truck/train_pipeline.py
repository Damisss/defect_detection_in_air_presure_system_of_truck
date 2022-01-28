import os 
import logging
import pandas as pd

from utils.file_management import FileManager
from config.core import config
from pipeline import pipeline

_logger = logging.getLogger(__name__)

def train():
    if len(os.listdir(config.app_config.train_batch_files)) == 0:
        raise Exception('Please upload train batch files')
        
    try:
        _logger.info('Pipeline training has started.')
    
        FileManager.raw_file_manager(
            raw_files_folder = config.app_config.train_batch_files,
            validated_files_folder = config.app_config.validated_files,
            db_path= config.app_config.train_db_path,
            query_path=config.app_config.train_query,
            data_path=config.app_config.train_data
            )
        #if is_raw_data_preprocessed == 'done':
        if os.path.isfile(config.app_config.train_data):
            _df = pd.read_csv(config.app_config.train_data)

            X = _df.drop(config.model_config.target, axis=1)
            y = _df[config.model_config.target]
            pipeline.fit(X, y)
            FileManager.save_model(model=pipeline, model_path=config.app_config.pipeline_name)
            _logger.info('Pipeline training is completed.')
            return 'Done!'
    
    except Exception as e: 
        raise e

if __name__=='__main__':
    train()