import io
import json
from pathlib import Path

import pandas as pd
import pytest

from ml_api.app import create_app
from ml_api.config import TestingConfig


@pytest.fixture()
def app(tmpdir):
    testing_config = TestingConfig()
    setattr(testing_config, "PREFIX", tmpdir)

    app = create_app(config_object=testing_config)

    with app.app_context():
        yield app


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        yield client


def test_prediction_endpoint(tmpdir, client):
    path = Path(tmpdir)
    upload_folder = path / "batch_raw_files"
    upload_folder.mkdir(mode=511, parents=False, exist_ok=False)

    file_list = []
    folder = Path("ml_api/test_data")
    for file in folder.iterdir():

        if str(file).endswith(".csv"):
            file_list.append(
                (io.BytesIO(bytearray(file.read_bytes())), str(file).split("/")[2])
            )

    data = dict(file=file_list)

    response = client.post(
        "/predict", buffered=True, content_type="multipart/form-data", data=data
    )
    load_res = json.loads(response.data)
    results_df = pd.read_csv(path / "results.csv")

    assert load_res["status_code"] == 200
    assert load_res["message"] == "Prediction is completed"
    assert results_df["results"].values[0] == 0
