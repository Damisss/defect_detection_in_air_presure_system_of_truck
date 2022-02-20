import typing as t
from pathlib import Path

from pydantic import BaseModel
from strictyaml import YAML, Float, Int, Map, Seq, Str, load

ROOT_PATH = Path(__file__).resolve().parent
ROOT = ROOT_PATH.parent
CONFIG_FILE_PATH = ROOT / "config.yml"
TRAIN_BATCH_FILES = ROOT / "train_batch_raw_files"
TRAINED_MODEL_DIR = ROOT / "models"

SCHEMA = Map(
    {
        "pipeline_name": Str(),
        "train_batch_files": Str(),
        "validated_files": Str(),
        "train_data": Str(),
        "train_db_path": Str(),
        "test_batch_files": Str(),
        "test_validated_files": Str(),
        "test_data": Str(),
        "test_db_path": Str(),
        "test_query": Str(),
        "train_query": Str(),
        "kmeans_model_path": Str(),
        "sample_file_name": Str(),
        "length_0f_date_stamp_in_file": Int(),
        "length_0f_time_stamp_in_file": Int(),
        "number_of_columns": Int(),
        "unwanted_features": Seq(Str()),
        "target": Str(),
        "features": Seq(Str()),
        "random_state": Int(),
        "test_size": Float(),
        "logistic_regression_params": Map(
            {
                "logistic__solver": Seq(Str()),
                "logistic__penalty": Seq(Str()),
                "logistic__C": Seq(Float()),
            }
        ),
        "random_forest_params": Map(
            {
                "random_forest__criterion": Seq(Str()),
                "random_forest__n_estimators": Seq(Int()),
                "random_forest__min_samples_leaf": Seq(Int()),
                "random_forest__min_samples_split": Seq(Int()),
                "random_forest__max_features": Seq(Float()),
            }
        ),
        "cv": Int(),
        "mlflow_config": Map(
            {
                "artifacts_dir": Str(),
                "experiment_name": Str(),
                "run_name": Str(),
                "registered_model_name": Str(),
                "remote_server_uri": Str(),
            }
        ),
    }
)


class AppConfig(BaseModel):
    pipeline_name: str
    train_batch_files: str
    validated_files: str
    train_db_path: str
    train_data: str
    test_data: str
    test_batch_files: str
    test_validated_files: str
    test_db_path: str
    test_query: str
    train_query: str
    kmeans_model_path: str


class ModelConfig(BaseModel):
    sample_file_name: str
    length_0f_date_stamp_in_file: int
    length_0f_time_stamp_in_file: int
    number_of_columns: int
    unwanted_features: t.Sequence[str]
    target: str
    features: t.Sequence[str]
    random_state: int
    test_size: float
    logistic_regression_params: t.Dict[str, list]
    random_forest_params: t.Dict[str, t.Sequence]
    cv: int
    mlflow_config: t.Dict[str, str]


class Config(BaseModel):
    app_config: AppConfig
    model_config: ModelConfig


def get_config_path() -> Path:
    if CONFIG_FILE_PATH.is_file:
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH!r}")


def parse_config_file(cfg_path: Path = None, schema=None) -> YAML:
    if cfg_path is None:
        cfg_path = get_config_path()
        schema = SCHEMA

    if cfg_path:
        with open(cfg_path, "r") as cfg_file:
            data = load(cfg_file.read(), schema)
            return data
    raise OSError(f"Did not find config file at path: {cfg_path}")


def create_and_valid_config(cfg: YAML = None) -> Config:
    if cfg is None:
        cfg = parse_config_file(cfg)

    _config = Config(
        app_config=AppConfig(**cfg.data), model_config=ModelConfig(**cfg.data)
    )

    return _config


config = create_and_valid_config()
