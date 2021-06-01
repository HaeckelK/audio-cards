import os
import datetime
from datetime import timezone

import psycopg2

from structures import MemberStats


def now() -> int:
    dt = datetime.datetime.now(timezone.utc)

    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    return int(utc_timestamp)


class RecordExistsException(Exception):
    pass


class PostgresDatabase(Database):
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

    def register_download_file(self, section: str, filename: str, download_timestamp: int) -> int:
        cur = self.conn.cursor()
        added = now()
        try:
            cur.execute(
                "INSERT INTO files (section, filename, download_timestamp, import_status, added) \
VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (section, filename, download_timestamp, "not_imported", added),
            )
        except psycopg2.errors.UniqueViolation:
            cur.close()
            self.conn.rollback()
            raise RecordExistsException
        file_id = int(cur.fetchone()[0])
        self.conn.commit()
        cur.close()
        return file_id
