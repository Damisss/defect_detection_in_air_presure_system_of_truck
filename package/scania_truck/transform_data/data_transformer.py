import logging
import os

import pandas as pd

_logger = logging.getLogger(__name__)


def transformer(good_files, is_training=True):
    _logger.info("Data transformation has started.")
    try:
        files = [os.path.join(good_files, f) for f in os.listdir(good_files)]
        for file in files:
            _df = pd.read_csv(file)
            if is_training:
                _df["class"] = _df["class"].map({"neg": 0, "pos": 1})

            _df = _df.replace("na", "NULL")
            _df.to_csv(file, index=None, header=True)
            _logger.info("Saving transformed data.")

    except Exception as e:
        raise e
