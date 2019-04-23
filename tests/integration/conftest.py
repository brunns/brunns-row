# encoding=utf-8
import logging
import sqlite3
from contextlib import closing
from io import StringIO

import pytest

logger = logging.getLogger(__name__)


@pytest.fixture(scope="package")
def db():
    with closing(sqlite3.connect(":memory:")) as conn:
        cursor = conn.cursor()

        cursor.execute(
            "CREATE TABLE sausages (kind VARCHAR NOT NULL PRIMARY KEY, rating INT NOT NULL);"
        )
        cursor.execute("INSERT INTO sausages VALUES (?, ?);", ("cumberland", 10))
        cursor.execute("INSERT INTO sausages VALUES (?, ?);", ("vegetarian", 0))
        cursor.execute("INSERT INTO sausages VALUES (?, ?);", ("lincolnshire", 9))
        conn.commit()

        yield conn


@pytest.fixture(scope="function")
def csv_file():
    data = "kind,rating\n" "cumberland,10\n" "lincolnshire,9\n" "vegetarian,0\n"
    return StringIO(data)
