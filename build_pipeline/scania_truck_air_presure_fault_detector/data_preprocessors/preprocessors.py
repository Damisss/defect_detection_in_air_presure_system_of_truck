import logging

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from scania_truck_air_presure_fault_detector.utils.file_management import FileManager

# from scania_truck.utils.helper import find_number_of_cluster

_logger = logging.getLogger(__name__)


class DropUnwantedFeatures(BaseEstimator, TransformerMixin):
    def __init__(self, unwanted_feature) -> None:

        # if not isinstance(unwanted_feature, list):
        #     self.unwanted_feature = [unwanted_feature]
        # else:
        self.unwanted_feature = unwanted_feature

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    def transform(self, X: pd.DataFrame, y: pd.Series = None):
        X = X.copy()
        X = X.drop(self.unwanted_feature, axis=1)

        return X


class DropDuplicateRows(BaseEstimator, TransformerMixin):
    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    def transform(self, X: pd.DataFrame, y: pd.Series = None):
        _logger.info("Droping duplicate data.")

        X = X.copy()
        X = X.drop_duplicates()

        _logger.info("Done!")
        return X


class ImputeMissingData(BaseEstimator, TransformerMixin):
    def __init__(self, transformer) -> None:
        self.transformer = transformer

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # X=X.copy()
        # self.transformer.fit(X)
        return self

    def transform(self, X: pd.DataFrame, y: pd.Series = None):
        _logger.info("Missing data imputation has started.")
        try:
            X = X.copy()
            col = X.columns
            self.transformer.fit(X)
            X = self.transformer.transform(X)
            X = pd.DataFrame(data=X, columns=col)

            _logger.info("Missing data imputation has completed.")

            return X
        except Exception as e:
            _logger.info(f"Something went wrong while imputating missing data {e}")
            raise e


class ClusterData(BaseEstimator, TransformerMixin):
    def __init__(self, transformer, kmeans_model_path) -> None:
        self.transformer = transformer
        self.kmeans_model_path = kmeans_model_path

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        _logger.info("Data clustering has started.")
        try:
            X = X.copy()

            if isinstance(y, pd.Series):
                scaler = StandardScaler()
                X = scaler.fit_transform(X)
                # n_clusters = find_number_of_cluster(X, 11)
                self.transformer = self.transformer(n_clusters=2)
                self.transformer.fit(X)
                FileManager.save_model(
                    model=self.transformer, model_path=self.kmeans_model_path
                )
            return self

        except Exception as e:
            _logger.info(f"Something went wrong while clustering data {e}")
            raise e

    def transform(self, X: pd.DataFrame, y: pd.Series = None):
        try:
            X = X.copy()

            if isinstance(self.transformer, KMeans):
                scaler = StandardScaler()
                data = scaler.fit_transform(X)
                preds = self.transformer.predict(data)
                X["Clusters"] = preds
                self.transformer = None

            _logger.info("Data clustering has completed.")
            return X
        except Exception as e:
            _logger.info(f"Something went wrong while clustering data {e}")
            raise e
