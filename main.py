import functions_framework
import flask
import logging

from status import StatusUpdateService
from export import ExportService

logger = logging.getLogger(__name__)

@functions_framework.http
def export_http(request: flask.Request) -> flask.typing.ResponseReturnValue:
    request_args = request.args

    start_time = ''
    if request_args and "start_time" in request_args:
        start_time = request_args["start_time"]

    end_time = ''
    if request_args and "end_time" in request_args:
        end_time = request_args["end_time"]

    log_type = ''
    if request_args and "log_type" in request_args:
        log_type = request_args["log_type"]

    try:
        ExportService().run(start_time=start_time, end_time=end_time, log_type=log_type)
    except Exception as e:
        logging.error(e)
        return "internal-error", 500

    return "success", 200

@functions_framework.http
def status_update_http(request: flask.Request) -> flask.typing.ResponseReturnValue:
    try:
        StatusUpdateService().run()
    except Exception as e:
        return "internal-error", 500
    return "not-implemented", 501
