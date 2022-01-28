# import sys
# sys.path.insert(0, '')

from pathlib import PurePosixPath, Path
from flask import Blueprint, request, jsonify, send_file, current_app
import os
import pandas as pd
import shutil
from werkzeug.utils import secure_filename

from scania_truck.utils.file_management import FileManager
from scania_truck.config.core import config
from scania_truck.pipeline import pipeline

app = Blueprint('app', __name__)

ALLOWED_EXTENSIONS = {'csv'}
PREFIX = PurePosixPath(current_app.config['PREFIX'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/train')
def train():
    if len(os.listdir(config.app_config.train_batch_files)) == 0:
        
        return jsonify(
            {
                'error_message':'Please upload train batch files',
                'status_code': 400,
            }
        )
        
    try:
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

            return  jsonify(
            {
                'message':'Model training is completed',
                'status_code': 200,
            }
        )

        return jsonify(
            {
                'error_message':'Please upload valid batch files',
                'status_code': 400,
            }
        )

    except Exception as e:
        raise e

@app.route('/predict', methods=['POST'])
def predict():
    try:
        
        if request.method == 'POST':
            
            if 'file' not in request.files:
                return {'response': 'No file selected!!!!!'}
            
            files = request.files.getlist('file')
            if not files:
                return{'message': 'No selected file'}

            shutil.rmtree('ml_api/prediction_batch_raw_files')
            os.mkdir('ml_api/prediction_batch_raw_files')

            for file in files:
                if file.filename == '':
                    return {'message': 'No file selected'}
                if file and allowed_file(file.filename):

                    filename = secure_filename(file.filename)
                    file.save(os.path.join(current_app.config['PREFIX'], current_app.config['UPLOAD_FOLDER'], filename))
            

            FileManager.raw_file_manager(
                raw_files_folder =  PREFIX.joinpath( current_app.config['PRED_RAW_FILES_FOLDER']),
                validated_files_folder = PREFIX.joinpath(current_app.config['PRED_VALIDATED_FILES_FOLDER']),
                db_path= PREFIX.joinpath(current_app.config['PRED_DB_PATH']),
                query_path=config.app_config.test_query,
                data_path= PREFIX.joinpath(current_app.config['PRED_DATA']),
                is_training=False
            )
           

            if Path(PREFIX.joinpath(current_app.config['PRED_DATA'])).is_file:
                _df = pd.read_csv(PREFIX.joinpath(current_app.config['PRED_DATA']))
                model = FileManager.load_model(model_path=config.app_config.pipeline_name)
                pred = model.predict(_df)
                
                results = pd.DataFrame({'results': pred})
                results.to_csv(PREFIX.joinpath(current_app.config['PREDICTION_RESULTS']), index=None, header=True)

                return jsonify(
                            {
                                'message':'Prediction is completed',
                                'status_code': 200,
                            }
                        )
            
            return jsonify(
                        {
                            'error_message':'Please upload valid batch files',
                            'status_code': 400
                        }
                    )

    except Exception as e: 
        raise e


@app.route('/downloads/pred/results')
def download_prediction_results():

   try:
        if Path(PREFIX.joinpath(current_app.config['PREDICTION_RESULTS'])).is_file:
            return send_file('prediction_results/results.csv', as_attachment=True) 

        return jsonify(
                    {
                        'error_message':'There no result available. Please run prediction first.',
                        'status_code': 400
                    }
                )
   except Exception as e: 
        raise e
