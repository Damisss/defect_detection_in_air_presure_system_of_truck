import logging
import os
import pickle
import shutil
import sys
import typing as t
from pathlib import Path

from scania_truck_air_presure_fault_detector.db_operations.service import DbOperation
from scania_truck_air_presure_fault_detector.raw_files_validation.validator import (
    FileValidator,
)
from scania_truck_air_presure_fault_detector.transform_data.data_transformer import (
    transformer,
)
from scania_truck_air_presure_fault_detector.config.core import TRAINED_MODEL_DIR
sys.path.insert(0, "")

_logger = logging.getLogger(__name__)


class FileManager:
    @staticmethod
    def raw_file_manager(
        *,
        raw_files_folder: str,
        validated_files_folder: str,
        db_path: str,
        query_path: str,
        data_path: str,
        is_training: bool = True,
    ):
        _logger.info("Raw files preprocessing has started......")
        try:
            file_validator = FileValidator(raw_files_folder)
            file_validator.file_name_validation(validated_files_folder)
            file_validator.number_of_columns_validation(
                validated_files_folder, is_training=is_training
            )
            file_validator.empty_column_validation(validated_files_folder)

            transformer(f"{validated_files_folder}/good_files", is_training=is_training)

            db_operation = DbOperation(db_path)
            db_operation.connect()
            db_operation.create_table(query_path)
            db_operation.insert_good_data(f"{validated_files_folder}/good_files")
            db_operation.fetch_data(data_path)

            if is_training:
                if os.path.isdir(TRAINED_MODEL_DIR):
                    shutil.rmtree(TRAINED_MODEL_DIR)
                    os.mkdir(TRAINED_MODEL_DIR)
                else:
                    os.mkdir(TRAINED_MODEL_DIR)

            _logger.info("Raw files preprocessing has finished!")
            return "done"
        except Exception as e:
            raise e

    @staticmethod
    def save_model(*, model, model_path: t.Union[Path, str]) -> None:
        _logger.info(f"Saving model {model_path}...")
        try:
            with open(model_path, "wb") as f:
                f.write(pickle.dumps(model))
        except Exception as e:
            _logger.info(f"Something went wrong while saving model {e}")
            raise e

    @staticmethod
    def load_model(*, model_path: t.Union[Path, str]):
        with open(model_path, "rb") as f:
            model = pickle.loads(f.read())
            return model
