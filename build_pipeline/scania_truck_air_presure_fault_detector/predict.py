import typing as t

import pandas as pd

from scania_truck_air_presure_fault_detector.config.core import (
    TRAINED_MODEL_DIR,
    config,
)
from scania_truck_air_presure_fault_detector.utils.file_management import FileManager

model = FileManager.load_model(
    model_path=TRAINED_MODEL_DIR / config.app_config.pipeline_name
)


def make_prediction(*, input_data: pd.DataFrame) -> list:
    """Make a prediction using a saved model pipeline."""
    results = model.predict(input_data)

    return results
