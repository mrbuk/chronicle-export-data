from datetime import datetime, timezone
from google.cloud import bigquery

class MetadataService:
    IN_QUEUE = "IN_QUEUE"

    def __init__(self, bq_table_name: str):
        self.bq_table_name = bq_table_name

    def insert(self, id: str, state: str, data: str):
        client = bigquery.Client()
        # Perform a query.
        query = (
            f'INSERT INTO `{self.bq_table_name}` '
            '(event_time, id, state, data) '
            'VALUES (@event_time, @id, @state, @data)'
        )

        # create a UTC timestamp
        curent_ts = datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat()

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("event_time", "TIMESTAMP", curent_ts),
                bigquery.ScalarQueryParameter("id", "STRING", id),
                bigquery.ScalarQueryParameter("state", "STRING", state),
                bigquery.ScalarQueryParameter("data", "JSON", data),
            ]
        )

        results = client.query_and_wait(
            query, job_config=job_config
        )

    def fetch(self, state: str):
        # client = bigquery.Client()
        # # Perform a query.
        # query_job = client.query(
        #     f'SELECT name FROM `{self.bq_table_name}` '
        #     'WHERE state = "IN_QUEUE" '
        #     'LIMIT 50')
        # rows = query_job.result()  # Waits for query to finish
        pass
