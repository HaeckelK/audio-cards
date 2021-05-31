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

    def insert_member_stats(self, member_stats: MemberStats) -> int:
        cur = self.conn.cursor()
        added = now()
        try:
            cur.execute(
                """INSERT INTO member_stats (file_id,
    name,
    gamesPlayed,
    winRate,
    goals,
    assists,
    cleanSheetsDef,
    cleanSheetsGK,
    shotSuccessRate,
    passesMade,
    passSuccessRate,
    tacklesMade,
    tackleSuccessRate,
    proName,
    proPos,
    proStyle,
    proHeight,
    proNationality,
    proOverall,
    manOfTheMatch,
    redCards,
    favoritePosition,
    added) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
RETURNING id""",
                (
                    self.file_id,
                    member_stats.name,
                    member_stats.gamesPlayed,
                    member_stats.winRate,
                    member_stats.goals,
                    member_stats.assists,
                    member_stats.cleanSheetsDef,
                    member_stats.cleanSheetsGK,
                    member_stats.shotSuccessRate,
                    member_stats.passesMade,
                    member_stats.passSuccessRate,
                    member_stats.tacklesMade,
                    member_stats.tackleSuccessRate,
                    member_stats.proName,
                    member_stats.proPos,
                    member_stats.proStyle,
                    member_stats.proHeight,
                    member_stats.proNationality,
                    member_stats.proOverall,
                    member_stats.manOfTheMatch,
                    member_stats.redCards,
                    member_stats.favoritePosition,
                    added,
                ),
            )
        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            raise RecordExistsException
        stats_id = int(cur.fetchone()[0])

        # TODO error handling
        cur.execute("""UPDATE files SET import_status = 'imported' WHERE id = %s""", (self.file_id,))

        self.conn.commit()
        cur.close()
        return stats_id
