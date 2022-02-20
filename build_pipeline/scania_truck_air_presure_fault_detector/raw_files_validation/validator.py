import logging
import os
import re
import shutil

import pandas as pd

from scania_truck_air_presure_fault_detector.config.core import config
from scania_truck_air_presure_fault_detector.utils.helper import regex

_logger = logging.getLogger(__name__)


class FileValidator:
    def __init__(self, batch_files_path):
        self.batch_files_path = batch_files_path

    def _make_dir(self, *args) -> None:
        for arg in args:
            os.makedirs(arg)

    def _generated_path(self, parent_dir):
        good_files_path = os.path.join(parent_dir, "good_files")
        bad_files_path = os.path.join(parent_dir, "bad_files")
        return good_files_path, bad_files_path

    def _delete_dir(self, validated_files_path: str) -> None:
        shutil.rmtree(validated_files_path)

    def file_name_validation(self, validated_files_path):
        _logger.info("File name validation has started.")
        try:
            good_files_path, bad_files_path = self._generated_path(validated_files_path)
            if os.path.isdir(validated_files_path):
                self._delete_dir(validated_files_path)
            self._make_dir(good_files_path, bad_files_path)

            files = [f for f in os.listdir(self.batch_files_path)]

            for file in files:
                file_path = os.path.join(f"{self.batch_files_path}/{file}")
                if re.match(regex(), file):
                    length_0f_date_stamp_in_file = file.split("_")[1]
                    length_0f_time_stamp_in_file = file.split("_")[2].split(".")[0]
                    is_date_and_time_stampe_valid = (
                        len(length_0f_date_stamp_in_file)
                        == config.model_config.length_0f_date_stamp_in_file
                        and len(length_0f_time_stamp_in_file)
                        == config.model_config.length_0f_time_stamp_in_file
                    )

                    if is_date_and_time_stampe_valid:
                        shutil.copy2(file_path, good_files_path)
                        _logger.info(f"Saving {file} to good files folder.")
                        continue

                    shutil.copy2(file_path, bad_files_path)
                    _logger.info(f"Saving {file} to bad files folder.")
                else:
                    shutil.copy2(file_path, bad_files_path)
                    _logger.info(f"Saving {file} to bad files folder.")

            _logger.info("File name validation has finished.")

        except Exception as e:
            _logger.info(f"Something went wrong while validating file name {e}")
            raise e

    def number_of_columns_validation(self, validated_files_path, is_training=True):
        _logger.info("Columns validation has started.")
        try:
            good_files_path, bad_files_path = self._generated_path(validated_files_path)

            files = [f for f in os.listdir(good_files_path)]

            for file in files:
                file_path = os.path.join(f"{good_files_path}/{file}")
                _df = pd.read_csv(file_path)
                colnum = (
                    config.model_config.number_of_columns
                    if is_training
                    else config.model_config.number_of_columns - 1
                )

                if len(_df.columns) == colnum:
                    continue

                shutil.move(file_path, bad_files_path)
                _logger.info(f"Saving {file} to bad files folder.")

            _logger.info("Columns validation has finished.")

        except Exception as e:
            _logger.info(f"Something went wrong while validating the columns {e}")
            raise e

    def empty_column_validation(self, validated_files_path):
        _logger.info("Empty columns validation has started.")
        try:
            good_files_path, bad_files_path = self._generated_path(validated_files_path)

            files = [f for f in os.listdir(good_files_path)]
            for file in files:
                file_path = os.path.join(f"{good_files_path}/{file}")
                _df = pd.read_csv(file_path)
                for col in _df.columns:
                    if (len(_df[col]) - _df[col].count()) == len(_df[col]):
                        shutil.move(file_path, bad_files_path)
                        _logger.info(f"Saving {file} to bad files folder.")
                        break

            _logger.info("Empty columns validation has finished.")
        except Exception as e:
            _logger.info(f"Something went wrong while validating the empty columns {e}")
            raise e
