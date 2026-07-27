# Copyright 2018-2026 Simon Brunning
import logging
import sqlite3
from collections.abc import Generator
from contextlib import closing
from io import StringIO
from sqlite3 import Connection

import pytest

logger = logging.getLogger(__name__)


@pytest.fixture(scope="package")
def db() -> Generator[Connection]:
    with closing(sqlite3.connect(":memory:")) as conn:
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE sausages (kind VARCHAR NOT NULL PRIMARY KEY, rating INT NOT NULL);")
        sausages = [("cumberland", 10), ("vegetarian", 0), ("lincolnshire", 9)]
        cursor.executemany("INSERT INTO sausages VALUES (?, ?);", sausages)
        conn.commit()

        yield conn


@pytest.fixture(scope="function")
def csv_file() -> StringIO:
    data = "kind,rating\ncumberland,10\nlincolnshire,9\nvegetarian,0\n"
    return StringIO(data)
