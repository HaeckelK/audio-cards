import os
import datetime
from datetime import timezone

import psycopg2


def now() -> int:
    dt = datetime.datetime.now(timezone.utc)

    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    return int(utc_timestamp)


class RecordExistsException(Exception):
    pass


class PostgresDatabase:
    def __init__(self) -> None:
        dbname = os.environ["POSTGRES_DB"]
        user = os.environ["POSTGRES_USER"]
        password = os.environ["POSTGRES_PASSWORD"]
        host = os.environ["POSTGRES_HOST"]
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        return

    def close(self) -> None:
        self.conn.close()
        return

    def add_word(self, word: str) -> int:
        cur = self.conn.cursor()
        language = "NOT IMPLEMENTED"
        known = False
        date_known = -1
        added = now()
        try:
            cur.execute(
                "INSERT INTO words (language, word, known, date_known, added) \
VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (language, word, known, date_known, added),
            )
        except psycopg2.errors.UniqueViolation:
            cur.close()
            self.conn.rollback()
            raise RecordExistsException
        row_id = int(cur.fetchone()[0])
        self.conn.commit()
        cur.close()
        return row_id

    def get_words(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM words;")
        result = cur.fetchall()
        cur.close()
        return result
