import os
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from scania_truck_air_presure_fault_detector.config.core import config
from scania_truck_air_presure_fault_detector.raw_files_validation.validator import (
    FileValidator,
)


@pytest.fixture
def generate_data():
    data = dict()

    for col in config.model_config.features:
        data[col] = np.random.choice(100, size=100)

    df = pd.DataFrame(data, columns=config.model_config.features)
    df["class"] = np.random.choice(1, size=100)
    return df


INVALID_FILE_NAME = "ApsFailure_152000_120218.csv"
VALID_FILE_NAME_2 = "ApsFailure_11052021_120219.csv"
VALID_FILE_NAME_1 = "ApsFailure_11052020_140550.csv"


def test_file_name_validation(tmpdir, generate_data):
    path = Path(tmpdir)
    batch_files_path = path / "batch_files"
    batch_files_path.mkdir(mode=511, parents=False, exist_ok=False)
    validated_file_path = path / "validated_files"

    for file_name in (VALID_FILE_NAME_1, VALID_FILE_NAME_2, INVALID_FILE_NAME):
        generate_data.to_csv(batch_files_path / f"{file_name}", header=True, index=None)

    validator = FileValidator(batch_files_path=batch_files_path)
    validator.file_name_validation(validated_file_path)

    good_files = os.listdir(validated_file_path / "good_files")
    bad_files = os.listdir(validated_file_path / "bad_files")

    assert len(good_files) == 2
    assert len(bad_files) == 1
    assert VALID_FILE_NAME_1 in good_files
    assert VALID_FILE_NAME_2 in good_files
    assert INVALID_FILE_NAME in bad_files


def test_number_of_columns_validation(tmpdir, generate_data):
    path = Path(tmpdir)
    good_files = path / "good_files"
    bad_files = path / "bad_files"
    good_files.mkdir(mode=511, parents=False, exist_ok=False)
    bad_files.mkdir(mode=511, parents=False, exist_ok=False)

    df = generate_data
    count = 1
    for file_name in (VALID_FILE_NAME_1, VALID_FILE_NAME_2):

        if count == 2:
            df = df.drop("ag_003", axis=1)
        df.to_csv(good_files / f"{file_name}", header=True, index=None)
        count += 1

    validator = FileValidator(batch_files_path="")
    validator.number_of_columns_validation(path)

    assert len(os.listdir(good_files)) == 1
    assert len(os.listdir(bad_files)) == 1


def test_empty_column_validation(tmpdir, generate_data):
    path = Path(tmpdir)
    good_files = path / "good_files"
    bad_files = path / "bad_files"
    good_files.mkdir(mode=511, parents=False, exist_ok=False)
    bad_files.mkdir(mode=511, parents=False, exist_ok=False)

    df = generate_data
    count = 1
    for file_name in (VALID_FILE_NAME_1, VALID_FILE_NAME_2):

        if count == 2:
            df["ag_003"] = np.nan
        df.to_csv(good_files / f"{file_name}", header=True, index=None)
        count += 1

    validator = FileValidator(batch_files_path="")
    validator.empty_column_validation(path)

    assert len(os.listdir(good_files)) == 1
    assert len(os.listdir(bad_files)) == 1
