import unittest
from unittest.mock import patch, call

from datetime import datetime, timedelta
from backstory import BackstoryClient, CreateDataExportRequest

import json
import uuid

def mocked_sa(*args, **kwargs):
    class MockResponse:
        def __init__(self, service_account_email):
            self.service_account_email = service_account_email

    return MockResponse("na@na")

def mocked_request(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def request(self, method, url, json):
            return self

        def json(self):
            return self.json_data

    req = kwargs["json"]
    if args[0] == "POST" and args[1] == 'https://eu-backstory.googleapis.com/v1/tools/dataexport' and req["gcsBucket"] == "some-bucket":
        return MockResponse({ "dataExportId": "d828bcec-21d3-4ecd-910e-0a934f0bd074",
          "startTime": "2024-10-30T00:00:00Z",
          "endTime": "2024-10-30T12:00:00Z",
          "logType": "some_log_type",
          "gcsBucket": "some-bucket",
          "dataExportStatus": {"stage": "IN_QUEUE"}
        }, 200)
    elif args[0] == "POST" and args[1] == 'https://eu-backstory.googleapis.com/v1/tools/dataexport' and req["gcsBucket"] == "error-bucket":
        return MockResponse({ "dataExportId": "d828bcec-21d3-4ecd-910e-0a934f0bd075",
            "startTime": "2024-10-30T00:00:00Z",
            "endTime": "2024-10-30T12:00:00Z",
            "logType": "some_log_type",
            "gcsBucket": "error-bucket",
            "dataExportStatus": {"stage": "ERROR"}
        }, 500)

    return MockResponse(None, 404)

class BackstoryClientDummy:
    def create_data_export(self, request: CreateDataExportRequest) -> dict:
        return {
            "dataExportId": str(uuid.uuid4()),
            "startTime": request.start_time,
            "endTime": request.end_time,
            "logType": request.log_type,
            "gcsBucket": request.gcs_bucket,
            "dataExportStatus": {"stage": "IN_QUEUE"}
        }

    def get_data_export(self, id: str) -> dict:
        if id == "59f938fd-8fa5-4948-8c6a-d3e70d1a9b4e":
            return {
                "dataExportId": id,
                "startTime": "2020-03-01T00:00:00Z",
                "endTime": "2020-03-15T00:00:00Z",
                "logType": "ALL_TYPES",
                "gcsBucket": "projects/chronicle-test/buckets/dataexport-test-bucket",
                "dataExportStatus": {"stage": "COMPLETED"}
            }
        elif id == "59f938fd-8fa5-4948-8c6a-d3e70d1a9b4f":
            return {
                "dataExportId": id,
                "startTime": "2020-03-01T00:00:00Z",
                "endTime": "2020-03-15T00:00:00Z",
                "logType": "ALL_TYPES",
                "gcsBucket": "projects/chronicle-test/buckets/dataexport-test-bucket",
                "dataExportStatus": {"stage": "ERROR"}
            }
        elif id == "59f938fd-8fa5-4948-8c6a-d3e70d1a9b4a":
            return {
                "dataExportId": id,
                "startTime": "2020-03-01T00:00:00Z",
                "endTime": "2020-03-15T00:00:00Z",
                "logType": "ALL_TYPES",
                "gcsBucket": "projects/chronicle-test/buckets/dataexport-test-bucket",
                "dataExportStatus": {"stage": "IN_QUEUE"}
            }
        else:
            raise ValueError("id does not exist")

class TestBackstory(unittest.TestCase):
    def test_simple_date(self):
        r = CreateDataExportRequest(
            start_time=datetime(2024,10,30,0,0,0), end_time=datetime(2024,10,30,12,0,0),
            gcs_bucket="some-bucket", log_type="some_log_type"
        )

        self.assertEqual(r.start_time, "2024-10-30T00:00:00Z")
        self.assertEqual(r.end_time, "2024-10-30T12:00:00Z")
        self.assertEqual(r.gcs_bucket, "some-bucket")
        self.assertEqual(r.log_type, "some_log_type")

    def test_create_data_export_200(self):
        with (
            patch('google.oauth2.service_account.Credentials.from_service_account_file', side_effect=mocked_sa) as sa_mock,
            patch('google.auth.transport.requests.AuthorizedSession.request', side_effect=mocked_request) as request_mock,
        ):
            client = BackstoryClient(region_prefix="eu", sa_file_path="some_sa_file")
            r = CreateDataExportRequest(
                start_time=datetime(2024,10,30,0,0,0), end_time=datetime(2024,10,30,12,0,0),
                gcs_bucket="some-bucket", log_type="some_log_type"
            )
            result = client.create_data_export(r)
            self.assertIn(
                call(
                    'POST', 'https://eu-backstory.googleapis.com/v1/tools/dataexport', json=r.toDict()
                ),
                request_mock.call_args_list)
            self.assertEqual(result["dataExportId"], "d828bcec-21d3-4ecd-910e-0a934f0bd074")

    def test_create_data_export_500(self):
        with (
            patch('google.oauth2.service_account.Credentials.from_service_account_file', side_effect=mocked_sa) as sa_mock,
            patch('google.auth.transport.requests.AuthorizedSession.request', side_effect=mocked_request) as request_mock,
        ):
            client = BackstoryClient(region_prefix="eu", sa_file_path="some_sa_file")
            r = CreateDataExportRequest(
                start_time=datetime(2024,10,30,0,0,0), end_time=datetime(2024,10,30,12,0,0),
                gcs_bucket="error-bucket", log_type="some_log_type"
            )

            with self.assertRaises(Exception):
                id = client.create_data_export(r)

            self.assertIn(
                call(
                    'POST', 'https://eu-backstory.googleapis.com/v1/tools/dataexport', json=r.toDict()
                ),
                request_mock.call_args_list)

if __name__ == '__main__':
    unittest.main()
