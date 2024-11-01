import os
from backstory import BackstoryClient
from backstory_test import BackstoryClientDummy
from metadata import MetadataService

import metadata
import json
import logging

logger = logging.getLogger(__name__)

BQ_METADATA_TABLE = os.environ['BQ_METADATA_TABLE']

class StatusUpdateService:
    def __init__(self):
        #self.client = BackstoryClient(region_prefix="eu", sa_file_path=SA_FILE)
        self.client = BackstoryClientDummy()
        self.metadata = MetadataService(bq_table_name=BQ_METADATA_TABLE)

    def run(self):
        try:
            job_ids = self.metadata.filter_by_status(status="IN_QUEUE")
            for job_id in job_ids:
                try:
                    result = self.client.get_data_export(job_id)
                    status = result.get("dataExportStatus", {}).get("stage", "UNKNOWN")
                    if status != "IN_QUEUE":
                        raw_data = json.loads(json.dumps(result))
                        self.metadata.insert(id=job_id, status=status, data=raw_data)
                except ValueError:
                    self.metadata.insert(id=job_id, status="NOT_FOUND", data=None)
        except Exception as e:
            print(e)
