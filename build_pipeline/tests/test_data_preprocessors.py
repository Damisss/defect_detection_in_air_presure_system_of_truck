import numpy as np
import pandas as pd
import pytest
from sklearn.cluster import KMeans
from sklearn.impute import KNNImputer

from scania_truck_air_presure_fault_detector.config.core import config
from scania_truck_air_presure_fault_detector.data_preprocessors.preprocessors import (
    ClusterData,
    DropUnwantedFeatures,
    ImputeMissingData,
)


@pytest.fixture
def input_data():
    data = dict()
    for col in config.model_config.features:
        data[col] = np.random.randint(300, size=1000)
    data["class"] = np.random.choice(1, size=1000)

    return pd.DataFrame(data=data)


def test_drop_unwanted_feature(input_data):
    data = input_data

    drop_unwanted_features = DropUnwantedFeatures(config.model_config.unwanted_features)
    transformed_data = drop_unwanted_features.fit_transform(data)

    assert config.model_config.unwanted_features[0] in data
    assert not config.model_config.unwanted_features[0] in transformed_data.columns


def test_impute_missing_data(input_data):
    data = input_data
    y = data["class"]
    data = data.drop("class", axis=1)
    data = data.drop(config.model_config.unwanted_features, axis=1)

    for col in range(0, 20, 2):
        data.loc[:5, data.columns[col]] = np.nan

    imputer = ImputeMissingData(KNNImputer())
    imputed_data = imputer.fit_transform(data)
    imputed_data = pd.DataFrame(data=imputed_data, columns=data.columns)
    imputed_data["class"] = y
    assert data.isna().sum().any() > 0
    assert imputed_data.isna().sum().all() == 0


def test_cluster_data(tmpdir, input_data):
    data = input_data
    y = data["class"]
    data = data.drop("class", axis=1)
    data = data.drop(config.model_config.unwanted_features, axis=1)

    cluster = ClusterData(KMeans, f"{tmpdir}/model.pickle")
    cluster.fit(data, y)
    preds = cluster.transform(data)

    assert len(preds["Clusters"].unique()) > 0
