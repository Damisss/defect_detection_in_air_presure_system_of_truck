from pathlib import Path

import pytest
from pydantic import ValidationError

from scania_truck.config.core import create_and_valid_config, parse_config_file

CONFIG_TEXT = """
pipeline_name: scania_truck
train_batch_files: scania_truck/train_batch_raw_files
test_batch_files: ml_api/prediction_batch_raw_files
validated_files: scania_truck/validated_files
test_validated_files: ml_api/validated_files
train_db_path: scania_truck/train_data/data.db
test_db_path: ml_api/data/data.db
train_data: scania_truck/train_data/data.csv
test_data: ml_api/data/data.csv
train_query: scania_truck/db_operations/train.sql
test_query: scania_truck/db_operations/prediction.sql
kmeans_model_path: scania_truck/models/kmeans.pickle
prod_model_path: scania_truck/models/

random_state: 42
test_size: 0.33
cv: 2
sample_file_name: ApsFailure_08012020_120000.csv
length_0f_date_stamp_in_file: 8
length_0f_time_stamp_in_file: 6
number_of_columns : 171
logistic_regression_params:
  logistic__solver:
    - newton-cg
  logistic__penalty:
    - l2
  logistic__C:
    - 100.0
random_forest_params:
  random_forest__n_estimators:
    - 150
  random_forest__min_samples_leaf:
    - 2
  random_forest__min_samples_split:
    - 14
  random_forest__max_features:
    - 0.7
  random_forest__criterion:
    - entropy

mlflow_config:
  artifacts_dir: artifacts
  experiment_name: Scania Truck
  run_name: scania_truck
  registered_model_name: model_
  remote_server_uri: http://127.0.0.1:1234
unwanted_features:
  - br_000
target: class
features:
  - aa_000
  - ab_000
  - ac_000
"""

INVALID_CONFIG_TEXT = """
package_name: scania_truck

target: class
features:
  - aa_000
  - ab_000
  - ac_000

"""


def test_config_validation(tmpdir):
    cfg_tmpdir = Path(tmpdir)
    cfg_path = cfg_tmpdir / "config.yml"
    cfg_path.write_text(CONFIG_TEXT)

    parsed_data = parse_config_file(cfg_path=cfg_path)
    config = create_and_valid_config(cfg=parsed_data)

    assert config.app_config
    assert config.model_config


def test_raise_error_for_invalid_cfg(tmpdir):
    cfg_tmpdir = Path(tmpdir)
    cfg_path = cfg_tmpdir / "config.yml"
    cfg_path.write_text(INVALID_CONFIG_TEXT)

    parsed_data = parse_config_file(cfg_path=cfg_path)

    with pytest.raises(ValidationError) as exec_info:
        create_and_valid_config(cfg=parsed_data)
        print(exec_info)

    assert "train_data" in str(exec_info.value)
    assert "field required" in str(exec_info.value)
