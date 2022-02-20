import logging

import mlflow
import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler

from scania_truck_air_presure_fault_detector.config.core import (
    TRAINED_MODEL_DIR,
    config,
)
from scania_truck_air_presure_fault_detector.utils.file_management import FileManager
from scania_truck_air_presure_fault_detector.utils.mlflow_helper import (
    log_and_load_production_model,
    mlflow_model_logger,
)

_logger = logging.getLogger(__name__)


class ModelFinder(BaseEstimator, ClassifierMixin):
    def fit(self, X: pd.DataFrame, y: pd.Series):
        _logger.info("Searching best model for each data cluster...")
        try:
            X = X.copy()
            X[config.model_config.target] = y
            clusters = X["Clusters"].unique()

            mlflow.set_tracking_uri(
                config.model_config.mlflow_config["remote_server_uri"]
            )

            for i in sorted(clusters):
                _X = X[X["Clusters"] == i]
                _y = _X[config.model_config.target]
                _X = _X.drop(config.model_config.target, axis=1)
                _X = _X.drop("Clusters", axis=1)
                X_train, X_test, y_train, y_test = train_test_split(
                    _X,
                    _y,
                    test_size=config.model_config.test_size,
                    random_state=config.model_config.random_state,
                )
                # finde best estimator for the cluster
                over_sampler = SMOTE(
                    sampling_strategy="auto",  # samples only the minority class
                    random_state=0,  # for reproducibility
                    k_neighbors=5,
                    n_jobs=4,
                )

                id = i + 1
                mlflow.set_experiment(
                    f"{config.model_config.mlflow_config['experiment_name']}_{str(i)}"
                )
                with mlflow.start_run():

                    model_1 = Pipeline(
                        [
                            ("scaler", StandardScaler()),
                            ("over_sampler", over_sampler),
                            ("logistic", LogisticRegression()),
                        ]
                    )

                    logistic = GridSearchCV(
                        model_1,
                        param_grid=config.model_config.logistic_regression_params,
                        cv=config.model_config.cv,
                    )
                    logistic.fit(X_train, y_train)
                    logistic_f1 = f1_score(y_test, logistic.predict(X_test))

                    mlflow.log_metric("f1_score", logistic_f1)
                    mlflow_model_logger(logistic.best_estimator_, "logistic", i)

                with mlflow.start_run():
                    model_2 = Pipeline(
                        [
                            ("scaler", StandardScaler()),
                            ("over_sampler", over_sampler),
                            ("random_forest", RandomForestClassifier()),
                        ]
                    )

                    random_forest = GridSearchCV(
                        model_2,
                        param_grid=config.model_config.random_forest_params,
                        cv=config.model_config.cv,
                    )
                    random_forest.fit(X_train, y_train)
                    random_forest_f1 = f1_score(y_test, random_forest.predict(X_test))

                    mlflow.log_metric("f1_score", random_forest_f1)
                    mlflow_model_logger(
                        random_forest.best_estimator_, "random_forest", i
                    )
                model_name = (
                    "random_forest" if random_forest_f1 > logistic_f1 else "logistic"
                )

                prod_model = log_and_load_production_model(
                    experiment_ids=id, model_name=model_name, metric="f1_score"
                )
                FileManager.save_model(
                    model=prod_model,
                    model_path=f"scania_truck_air_presure_fault_detector/models/{model_name}_{str(i)}.pickle",
                )
                _logger.info(f"Saving best model for cluster: {i}.")

            return self
        except Exception as e:
            _logger.info(
                f"Something went wrong while finding best model for cluster  {e}"
            )
            raise e

    def predict(self, X: pd.DataFrame, y: pd.Series = None):
        _logger.info("Prediction has started...")
        try:
            X = X.copy()
            kmeans = FileManager.load_model(
                model_path=TRAINED_MODEL_DIR / config.app_config.kmeans_model_path
            )
            preds = kmeans.predict(X)
            X["Clusters"] = preds
            clusters = X["Clusters"].unique()

            results = list()
            for i in clusters:
                _X = X[X["Clusters"] == i]
                _X = _X.drop("Clusters", axis=1)

                for model_path in TRAINED_MODEL_DIR.iterdir():
                    if str(model_path).endswith(f"_{str(i)}.pickle"):
                        model = FileManager.load_model(model_path=model_path)
                        predictions = model.predict(_X)

                        for r in predictions:
                            results.append(r)
            return results

        except Exception as e:
            _logger.info(f"Something went wrong while making predictions {e}")
            raise e
