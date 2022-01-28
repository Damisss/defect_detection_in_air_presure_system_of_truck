# import sys
# sys.path.insert(0, '')

from scania_truck.config.core import config

class Config:
    DEBUG = False
    TESTING = False
    SERVER_PORT = 3000
    UPLOAD_FOLDER = 'ml_api/prediction_batch_raw_files'
    PREFIX = ''
    PRED_RAW_FILES_FOLDER = config.app_config.test_batch_files
    PRED_VALIDATED_FILES_FOLDER = config.app_config.test_validated_files
    PRED_DB_PATH = config.app_config.test_db_path
    PRED_DATA = config.app_config.test_data
    PREDICTION_RESULTS='ml_api/prediction_results/results.csv'


# class ProductionConfig(Config):
#     DEBUG = False
#     SERVER_ADDRESS: os.environ.get('SERVER_ADDRESS', '0.0.0.0')
#     SERVER_PORT: os.environ.get('SERVER_PORT', '5000')


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):     
    TESTING = True
    PRED_RAW_FILES_FOLDER = 'batch_raw_files'
    PRED_VALIDATED_FILES_FOLDER = 'test_validated_files' 
    PRED_DB_PATH = 'test_data.db' 
    PRED_DATA = 'test_data.csv' 
    UPLOAD_FOLDER = 'batch_raw_files'
    PREDICTION_RESULTS ='results.csv'