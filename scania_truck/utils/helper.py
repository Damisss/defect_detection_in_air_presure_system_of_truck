import logging
import sys
from pprint import pprint
from urllib.parse import urlparse

import mlflow
import pandas as pd
from kneed import KneeLocator
from mlflow.tracking import MlflowClient
from sklearn.cluster import KMeans

from scania_truck.config.core import config

_logger = logging.getLogger(__name__)


def regex() -> str:
    return "['ApsFailure']+['\_'']+[\d_]+[\d]+\.csv"


def find_number_of_cluster(data: pd.DataFrame, number_of_trial: int) -> int:
    inertia = []
    for i in range(1, number_of_trial):
        cluster = KMeans(n_clusters=i).fit(data)
        inertia.append(cluster.inertia_)

    kneedle = KneeLocator(
        range(1, number_of_trial),
        inertia,
        S=1.0,
        curve="convex",
        direction="decreasing",
    )
    _logger.info(f"Number of cluster is {kneedle.knee}.")
    return kneedle.knee


def mlflow_model_logger(model, model_name, i):
    tracking_url_type_store = urlparse(mlflow.get_artifact_uri()).scheme

    if tracking_url_type_store != "file":
        mlflow.sklearn.log_model(
            model, "model", registered_model_name=f"{model_name}_" + str(i)
        )
    else:
        mlflow.sklearn.load_model(model, "model")


def log_and_load_production_model(*, experiment_ids: int, model_name: str, metric: str):
    # if experiment_ids == 1:
    mlflow.set_tracking_uri(config.model_config.mlflow_config["remote_server_uri"])
    # runs = mlflow.search_runs(experiment_ids=str(experiment_ids))
    # lowest = runs[f'metrics.{metric}'].sort_values(ascending=True)[0]
    # runs_id = runs[runs[f'metrics.{metric}']==lowest]['run_id'][0]

    df = mlflow.search_runs([experiment_ids], order_by=[f"metrics.{metric} DESC"])

    client = MlflowClient()
    filter_string = "name='{}_{}'".format(model_name, str(experiment_ids))
    print("registerrr", model_name)
    for mv in client.search_model_versions(filter_string):
        mv = dict(mv)

        if mv["run_id"] == df["run_id"][0]:
            pprint(mv, indent=4)
            version = mv["version"]
            model = mv["source"]
            client.transition_model_version_stage(
                name="{}_{}".format(model_name, str(experiment_ids)),
                version=version,
                stage="Production",
            )
        else:
            version = mv["version"]
            client.transition_model_version_stage(
                name="{}_{}".format(model_name, str(experiment_ids)),
                version=version,
                stage="Staging",
            )

    loaded_model = mlflow.pyfunc.load_model(model)

    return loaded_model


# Multiple calls to logging.getLogger('someLogger') return a
# reference to the same logger object.  This is true not only
# within the same module, but also across modules as long as
# it is in the same Python interpreter process.

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s —" "%(funcName)s:%(lineno)d — %(message)s"
)


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler
