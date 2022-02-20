import logging
import sys

import pandas as pd
from kneed import KneeLocator
from sklearn.cluster import KMeans

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
