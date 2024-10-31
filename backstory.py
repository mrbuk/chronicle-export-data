# Imports required for the sample - Google Auth and API Client Library Imports.
# Get these packages from https://pypi.org/project/google-api-python-client/ or run $ pip
# install google-api-python-client from your terminal
from google.auth.transport import requests
from google.oauth2 import service_account

from datetime import datetime

import json
import logging

logger = logging.getLogger(__name__)

class BackstoryClientError(Exception):
    pass

class CreateDataExportRequest:
    def __init__(self, start_time: datetime, end_time: datetime, log_type: str, gcs_bucket: str):
        self.start_time = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.end_time = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.log_type = log_type
        self.gcs_bucket = gcs_bucket

    def toJson(self):
        return json.dumps({
            "startTime": self.start_time,
            "endTime": self.end_time,
            "logType": self.log_type,
            "gcsBucket": self.gcs_bucket
        })

class BackstoryClient:
    SCOPES = ['https://www.googleapis.com/auth/chronicle-backstory']
    BACKSTORY_API_BASE = "backstory.googleapis.com"

    def __init__(self, region_prefix: str, sa_file_path: str):
        self.base_url = f"https://{self.BACKSTORY_API_BASE}"
        if region_prefix:
            self.base_url = f"https://{region_prefix}-{self.BACKSTORY_API_BASE}"

        self.credentials = service_account.Credentials.from_service_account_file(sa_file_path, scopes=self.SCOPES)

    def create_data_export(self, request: CreateDataExportRequest) -> dict:
        http_session = requests.AuthorizedSession(self.credentials)
        url = f"{self.base_url}/v1/tools/dataexport"
        resp = http_session.request("POST", url, json=request.toJson())
        # check status
        if not(resp.status_code >= 200 and resp.status_code <= 299):
            msg = f"received status code {resp.status_code} from backstory api"
            logger.error(msg)
            raise Exception(msg)

        o = resp.json()
        logger.info(f"received {o}")

        if o.get("dataExportId") is None:
            msg = f"dataExportId does not exist"
            logger.error(msg)
            raise BackstoryClientError(msg)

        if o.get("dataExportStatus") is None or o["dataExportStatus"].get("stage") != "IN_QUEUE":
            msg = f"unexpected state of export job: dataExportStatus={o["dataExportStatus"]}"
            logger.error(msg)
            raise BackstoryClientError(msg)

        return o

    def get_data_export(self, id) -> str:
        url = "{}/v1/tools/dataexport".format(self.base_url)
        return "not-implemented"
