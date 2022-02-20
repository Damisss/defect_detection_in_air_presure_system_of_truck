import os
import shutil
from pathlib import Path, PurePosixPath

import pandas as pd
from flask import Blueprint, current_app, jsonify, request, send_file
from scania_truck_air_presure_fault_detector.config.core import config
from scania_truck_air_presure_fault_detector.predict import make_prediction, model
from scania_truck_air_presure_fault_detector.utils.file_management import FileManager
from werkzeug.utils import secure_filename

app = Blueprint("app", __name__)

ALLOWED_EXTENSIONS = {"csv"}
PREFIX = PurePosixPath(current_app.config["PREFIX"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/predict", methods=["POST"])
def predict():
    try:

        if request.method == "POST":

            if "file" not in request.files:
                return {"response": "No file selected!!!!!"}

            files = request.files.getlist("file")
            if not files:
                return {"message": "No selected file"}

            shutil.rmtree("ml_api/prediction_batch_raw_files")
            os.mkdir("ml_api/prediction_batch_raw_files")

            for file in files:
                if file.filename == "":
                    return {"message": "No file selected"}
                if file and allowed_file(file.filename):

                    filename = secure_filename(file.filename)
                    file.save(
                        os.path.join(
                            current_app.config["PREFIX"],
                            current_app.config["UPLOAD_FOLDER"],
                            filename,
                        )
                    )

            FileManager.raw_file_manager(
                raw_files_folder=PREFIX.joinpath(
                    current_app.config["PRED_RAW_FILES_FOLDER"]
                ),
                validated_files_folder=PREFIX.joinpath(
                    current_app.config["PRED_VALIDATED_FILES_FOLDER"]
                ),
                db_path="ml_api/data/pred.db",
                query_path="ml_api/data/pred.sql",
                data_path=PREFIX.joinpath(current_app.config["PRED_DATA"]),
                is_training=False,
            )

            if Path(PREFIX.joinpath(current_app.config["PRED_DATA"])).is_file:
                _df = pd.read_csv(PREFIX.joinpath(current_app.config["PRED_DATA"]))
                pred = make_prediction(input_data=_df)
                results = pd.DataFrame({"results": pred})

                results.to_csv(
                    PREFIX.joinpath(current_app.config["PREDICTION_RESULTS"]),
                    index=None,
                    header=True,
                )

                return jsonify(
                    {
                        "message": "Prediction is completed",
                        "status_code": 200,
                    }
                )

            return jsonify(
                {"error_message": "Please upload valid batch files", "status_code": 400}
            )

    except Exception as e:
        raise e


@app.route("/downloads/pred/results")
def download_prediction_results():

    try:
        if Path(PREFIX.joinpath(current_app.config["PREDICTION_RESULTS"])).is_file:
            return send_file("prediction_results/results.csv", as_attachment=True)

        return jsonify(
            {
                "error_message": "There no result available. Please run prediction first.",
                "status_code": 400,
            }
        )
    except Exception as e:
        raise e


# https://packaging.python.org/en/latest/tutorials/packaging-projects/
