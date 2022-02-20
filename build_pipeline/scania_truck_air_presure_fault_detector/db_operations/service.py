import logging
import os
import sqlite3

import pandas as pd

_logger = logging.getLogger(__name__)


class DbOperation:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        _logger.info("Connecting sqlite database.")
        return sqlite3.connect(self.db_path)

    def create_table(self, query_path):
        _logger.info("Table creation has started.")
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute("DROP TABLE IF EXISTS scania_truck")

            with open(query_path, "r") as f:
                cur.execute(f.read())
            conn.commit()
            conn.close()

            _logger.info("Table has been successfully created.")

        except sqlite3.OperationalError as e:
            _logger.info("Something went wrong while creating table.")
            raise e

    def insert_good_data(self, good_files_dir):
        _logger.info("Inserting good data into table scania_truck.")
        try:
            conn = self.connect()
            cur = conn.cursor()
            files = [f for f in os.listdir(good_files_dir)]

            for file in files:
                file_path = os.path.join(good_files_dir, file)
                _df = pd.read_csv(file_path)

                for _, content in _df.iterrows():
                    place_holder = ",".join(["?" for i in range(len(content))])
                    columns = ",".join(_df.columns)

                    cur.execute(
                        "INSERT INTO scania_truck ({}) VALUES({})".format(
                            columns, place_holder
                        ),
                        list(content),
                    )
                    conn.commit()
            conn.close()
            _logger.info(
                "The data has been successfully inserted into table scania_truck."
            )

        except sqlite3.OperationalError as e:
            _logger.info(
                "Something went wrong while inserting data into table scania_truck."
            )
            raise e

    def fetch_data(self, csv_path):
        _logger.info("Feteching data from table scania_truck.")
        try:
            conn = self.connect()
            cur = conn.cursor()
            query = "SELECT * FROM scania_truck"
            cur.execute(query)
            data = cur.fetchall()
            columns = [col[0] for col in cur.description]
            _df = pd.DataFrame(data, columns=columns)
            _df.to_csv(csv_path, index=None, header=True)
            _logger.info(f"The data has been successfully save into {csv_path}.")

            conn.commit()
            conn.close()
        except sqlite3.OperationalError as e:
            _logger.info(
                "Something went wrong while inserting data into table scania_truck."
            )
            raise e
