import requests
import logging


logger = logging.getLogger(__name__)


class BaseApi:
    def __init__(self, base_url, keep_session=False):
        self._base_url = base_url
        self._keep_session = keep_session

    def get(self, path, **kwargs):
        return self._call('get', path, **kwargs)

    def post(self, path, **kwargs):
        return self._call('post', path, **kwargs)

    def _call(self, method, path, cookies=None, headers=None, payload=None):
        url = '{}{}'.format(self._base_url, path)

        request_kwargs = {}
        if payload:
            request_kwargs['data'] = payload
        if headers:
            request_kwargs['headers'] = headers
        if cookies:
            request_kwargs['cookies'] = cookies

        logger.debug(
            'API call: {} {} {}'.format(method.upper(), url, request_kwargs)
        )
        res = requests.request(method, url, **request_kwargs) 
        if res.status_code not in [200, 201]:
            raise SkyengApiError('Bad response: {} {}'.format(res.status_code, res.text))

        return res
