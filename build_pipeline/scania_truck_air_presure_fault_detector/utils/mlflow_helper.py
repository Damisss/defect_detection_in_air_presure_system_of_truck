from pprint import pprint
from urllib.parse import urlparse

import mlflow
from mlflow.tracking import MlflowClient

from scania_truck_air_presure_fault_detector.config.core import config


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
    filter_string = "name='{}_{}'".format(model_name, str(experiment_ids - 1))
    for mv in client.search_model_versions(filter_string):
        mv = dict(mv)

        if mv["run_id"] == df["run_id"][0]:
            version = mv["version"]
            model = mv["source"]
            client.transition_model_version_stage(
                name="{}_{}".format(model_name, str(experiment_ids - 1)),
                version=version,
                stage="Production",
            )
        else:
            version = mv["version"]
            client.transition_model_version_stage(
                name="{}_{}".format(model_name, str(experiment_ids - 1)),
                version=version,
                stage="Staging",
            )
    loaded_model = mlflow.pyfunc.load_model(model)

    return loaded_model
