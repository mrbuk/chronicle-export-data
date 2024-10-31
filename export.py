import os
import json
import logging
import uuid

from backstory import BackstoryClient, BackstoryClientError, CreateDataExportRequest
from date_calculator import DateCalculator
from metadata import MetadataService
from datetime import datetime

from backstory_test import BackstoryClientDummy

GCS_BUCKET = os.environ['EXPORT_GCS_BUCKET']
SA_FILE = os.environ['SA_FILE']
BQ_METADATA_TABLE = os.environ['BQ_METADATA_TABLE']

logger = logging.getLogger(__name__)

class ExportService:
    def __init__(self):
        #self.client = BackstoryClient(region_prefix="eu", sa_file_path=SA_FILE)
        self.client = BackstoryClientDummy()
        self.metadata = MetadataService(bq_table_name=BQ_METADATA_TABLE)

    def run(self, start_time: str, end_time: str, log_type = "ALL_TYPES"):
        # if dates have been provided execute this export without calcuation
        # this is meant to be used for manual invocation e.g. export led to error
        if start_time and end_time:
            r = json.dumps({
                "startTime": start_time,
                "endTime": end_time,
                "logType": log_type,
                "gcsBucket": GCS_BUCKET
            })
            self.export_request(r)

        # use DateCalculator() to calculate the date in the past and split
        # into multiple ranges to avoid running into 10TB per request limit
        else:
            calculator = DateCalculator()
            for d in calculator.ranges:
                r = CreateDataExportRequest(
                    start_time=d[0], end_time=d[1],
                    gcs_bucket=GCS_BUCKET, log_type = log_type)
                self.export_request(r)

    def export_request(self, r):
        raw_data = json.loads(r.toJson())
        try:
            result = self.client.create_data_export(r)
            id = result.get("dataExportId", "UNKNOWN")
            state = result.get("dataExportStatus", {}).get("stage", "UNKNOWN")
            self.metadata.insert(id=id, state=state, data=raw_data)
            # log success to bq
        except BackstoryClientError as e:
            logger.error(f"exporting data '{r}' resulted in an error: {e}")
            self.metadata.insert(id="UNKNOWN", state="INTERNAL_ERROR", data=raw_data)