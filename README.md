# chronicle-export-data

Python code that call the Chronicle Data Export API to initiate data export to Google Cloud Storage.

Invoking `export_http()` without any parameters will lead to an export triggered for:
 - 270d in past
 - 4 export jobs (0-6, 6-12, 12-18, 18-24) to avoid hitting the 10TB per request limit

Invoking `export_http()` and providing HTTP request parameter `start_time` and `end_time` will only run a single export for the specified timeframe

As the Chronicle Data Export API is asynchronous all `export_http()` operations log the status to a BigQuery table.
Running `status_update_http()` will fetch all non completed job from the BigQuery table, query the their status via Chronicle Data Export API and update the BigQuery table if the status has changed.

It is recommended to schedule both Cloud Functions daily via Cloud Scheduler. `status_update_http()` should run a few hours after the `export_http()` so that exports for that day have finished.

## Deployment
It is recommended to deploy `export_http()` and `status_update_http()` as two independent Cloud Function instances with the entry points:
1. `export_http()`
2. `status_update_http()`

For that use the same directory but provide only different entry points for the Cloud Function.

The Cloud Function will require the following environment variables to be set:
- `EXPORT_GCS_BUCKET` -
- `SA_FILE` - path to the service account key file that has permissions to access the Chronicle Data Export API
- `BQ_METADATA_TABLE` - BigQuery table name in the `projectid.dataset.tablename` to store the job status

**Ensure that the service account used to run the Cloud Function has `roles/bigquery.jobUser` permission on the BigQuery dataset/table**

You can deploy it using `gcloud`:

```
gcloud functions deploy chronicle_export \
  --entry-point export_http \
  --runtime=python312 \
  --no-allow-unauthenticated \
  --ingress-settings=internal-and-gclb \
  --set-secrets=/secrets/sa-key.json=SECRET_NAME:latest \
  --set-env-vars=EXPORT_GCS_BUCKET=my-bucket,SA_FILE=/secrets/sa-key.json,BQ_METADATA_TABLE=projectid.dataset.tablename
```

## BigQuery Table
As the Chronicle Data Export API is asynchronous job status is tracked in BigQuery. For that purpose a table needs to be created
```
# create dataset
bq --project_id GCP_PROJECT mk chronicle_export

# create table
bq --project_id GCP_PROJECT mk -t --description "Status tracking for Chronicle Data Export jobs" \
  chronicle_export.job_status \
  id:STRING,event_time:TIMESTAMP,status:STRING,data:JSON
```
