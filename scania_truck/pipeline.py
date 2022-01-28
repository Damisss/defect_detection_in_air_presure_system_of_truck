# from db_operations.service import dbOperation
# from raw_files_validation.validator import FileValidator
# from config.core import config
# from transform_data.data_transformer import transformer

from sklearn.cluster import KMeans
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from scania_truck.config.core import config
from scania_truck.data_preprocessors.preprocessors import (
    ClusterData,
    DropUnwantedFeatures,
    ImputeMissingData,
)
from scania_truck.training.best_model_finder import ModelFinder

pipeline = Pipeline(
    [
        ("drop_features", DropUnwantedFeatures(config.model_config.unwanted_features)),
        # (
        #     "drop_duplicate",
        #     DropDuplicateRows()
        # ),
        ("imput_missing_data", ImputeMissingData(KNNImputer())),
        ("cluster_data", ClusterData(KMeans, config.app_config.kmeans_model_path)),
        ("find_best_estimator", ModelFinder()),
    ]
)
