from datetime import datetime, timezone
from google.cloud import bigquery

from typing import List

class MetadataService:
    IN_QUEUE = "IN_QUEUE"

    def __init__(self, bq_table_name: str):
        self.bq_table_name = bq_table_name

    def insert(self, id: str, status: str, data: str|None):
        client = bigquery.Client()
        # Perform a query.
        query = (
            f'INSERT INTO `{self.bq_table_name}` '
            '(event_time, id, status, data) '
            'VALUES (@event_time, @id, @status, @data)'
        )

        # create a UTC timestamp
        curent_ts = datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat()

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("event_time", "TIMESTAMP", curent_ts),
                bigquery.ScalarQueryParameter("id", "STRING", id),
                bigquery.ScalarQueryParameter("status", "STRING", status),
                bigquery.ScalarQueryParameter("data", "JSON", data),
            ]
        )

        results = client.query_and_wait(
            query, job_config=job_config
        )

    def get(self, id) -> str:
        client = bigquery.Client()
        # Perform a query.
        query = (
            f'WITH jobs AS'
            f'(SELECT '
            f' ROW_NUMBER() OVER (PARTITION BY id ORDER BY event_time DESC) as rn,'
            f'  * '
            f' FROM `{self.bq_table_name}`'
            f' WHERE id = @id)'
            f'SELECT * FROM jobs WHERE rn = 1;'
        )
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("id", "STRING", id)
            ]
        )

        rows = client.query_and_wait(
            query, job_config=job_config
        )

        if rows.total_rows == 0:
            return ""
        elif rows.total_rows > 1:
            raise ValueError("more than one entry returned by query")

        # return first item
        return next(row.id for row in rows)

    def filter_by_status(self, status: str) -> List[str]:
        client = bigquery.Client()
        # Perform a query.
        query = (
            f'WITH jobs AS'
            f'(SELECT '
            f' ROW_NUMBER() OVER (PARTITION BY id ORDER BY event_time DESC) as rn,'
            f'  * '
            f' FROM `{self.bq_table_name}`'
            f' WHERE status = @status)'
            f'SELECT id, event_time, status FROM jobs WHERE rn = 1;'
        )
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("status", "STRING", status)
            ]
        )

        rows = client.query_and_wait(
            query, job_config=job_config
        )

        ids = []
        for row in rows:
            ids.append(row.id)

        return ids
