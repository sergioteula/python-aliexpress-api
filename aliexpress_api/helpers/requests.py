from types import SimpleNamespace
import json

from ..errors import ApiRequestException, ApiRequestResponseException


def api_request(request, response_name):
    try:
        response = request.getResponse()
    except Exception as error:
        if hasattr(error, 'message'):
            raise ApiRequestException(error.message) from error
        raise ApiRequestException(error) from error

    try:
        response = response[response_name]['resp_result']
        response = json.dumps(response)
        response = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))
    except Exception as error:
        raise ApiRequestResponseException(error) from error

    if response.resp_code == 200:
        return response.result
    else:
        raise ApiRequestResponseException(f'Response code {response.resp_code} - {response.resp_msg}')
