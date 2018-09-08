import logging

import requests

from inegi.exceptions import *

logger = logging.getLogger('walmart')
logger.setLevel(level=logging.DEBUG)


def printx(data):
    logger.info(data)


class Client(object):

    def __init__(self):
        self.session = requests.session()
        self.api_url = "http://www.beta.inegi.org.mx/app/api/denue/v1/consulta/"
        self.token = '0ff1fcf6-6a0c-4655-8dce-6672c043bd89'

    def get_data_from_inegi(self, id_pyme):
        return self._get('/ficha/{}'.format(id_pyme))

    def _get(self, endpoint, **kwargs):
        return self._request('GET', endpoint, **kwargs)

    def _delete(self, endpoint, **kwargs):
        return self._request('DELETE', endpoint, **kwargs)

    def _post(self, endpoint, **kwargs):
        return self._request('POST', endpoint, **kwargs)

    def _put(self, endpoint, **kwargs):
        return self._request('PUT', endpoint, **kwargs)

    def _request(self, method, endpoint, headers=None, params=None, data=None, files=None, **kwargs):
        _headers = {'Cache-Control': 'no-cache',
                    'Accept': 'application/json'}
        if headers:
            _headers.update(headers)

        _params = {
        }
        if params:
            _params.update(params)
        import datetime
        time1 = datetime.datetime.now()
        petition = '{}{}/{}'.format(self.api_url, endpoint, self.token)
        response = self.session.request(method, petition, files=files,
                                        headers=_headers, params=params, data=data, **kwargs)
        time2 = datetime.datetime.now()
        elapsed_time = time2 - time1
        printx(method + " " + response.url[0:100] + " time: " + str(elapsed_time.total_seconds()) + " sec.")
        return self._parse(response)

    @staticmethod
    def _parse(response):
        status_code = response.status_code
        if 'application/json' in response.headers['Content-Type']:
            r = response.json()
        else:
            r = response.text
        if status_code in (200, 201, 202):
            return r
        elif status_code == 204:
            return None
        elif 400 <= status_code < 500:
            offset = 1
            message = r
            import json
            logger.info(json.dumps(r))
            params = r.get('parameters', False)
            if params:
                for param in params:
                    message = message.replace('%' + str(offset), param)
                    offset = offset + 1
            message = "CLIENT_ERROR: " + message
            raise GeneralError(message)

        elif 500 <= status_code:
            raise GeneralError(str(r))
