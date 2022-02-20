import sys

from sklearn.cluster import KMeans
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from scania_truck_air_presure_fault_detector.config.core import (
    TRAINED_MODEL_DIR,
    config,
)
from scania_truck_air_presure_fault_detector.data_preprocessors.preprocessors import (
    ClusterData,
    DropUnwantedFeatures,
    ImputeMissingData,
)
from scania_truck_air_presure_fault_detector.training.best_model_finder import (
    ModelFinder,
)

sys.path.insert(0, "")

pipeline = Pipeline(
    [
        ("drop_features", DropUnwantedFeatures(config.model_config.unwanted_features)),
        # (
        #     "drop_duplicate",
        #     DropDuplicateRows()
        # ),
        ("imput_missing_data", ImputeMissingData(KNNImputer())),
        (
            "cluster_data",
            ClusterData(
                KMeans, TRAINED_MODEL_DIR / config.app_config.kmeans_model_path
            ),
        ),
        ("find_best_estimator", ModelFinder()),
    ]
)
