import requests
import json
import logging
from . import consts as c, utils, exceptions
from bllper.sysHelper import get_windows_proxy_settings


class Client(object):

    def __init__(self, api_key, api_secret_key, passphrase, use_server_time=False, flag='1'):

        self.API_KEY = api_key
        self.API_SECRET_KEY = api_secret_key
        self.PASSPHRASE = passphrase
        self.use_server_time = use_server_time
        self.flag = flag

        
    def _get_proxy(self):
        proxy_settings = get_windows_proxy_settings()
        if proxy_settings['proxy_enabled']:
            logging.info(f'代理服务器地址: {proxy_settings["proxy_server"]}')
            return {
                'http': 'http://' + proxy_settings['proxy_server'],
                'https': 'https://' + proxy_settings['proxy_server']
            }
        else:
            logging.info('未启用代理服务器')
            return {}
            

    def _request(self, method, request_path, params):

        if method == c.GET:
            request_path = request_path + utils.parse_params_to_str(params)
        # url
        url = c.API_URL + request_path

        timestamp = utils.get_timestamp()

        # sign & header
        if self.use_server_time:
            timestamp = self._get_timestamp()

        body = json.dumps(params) if method == c.POST else ""

        sign = utils.sign(utils.pre_hash(timestamp, method, request_path, str(body)), self.API_SECRET_KEY)
        header = utils.get_header(self.API_KEY, sign, timestamp, self.PASSPHRASE, self.flag)

        # send request
        response = None

        logging.debug("url:", url)
        logging.debug("headers:", header)
        logging.debug("body:", body)

        if method == c.GET:
            response = requests.get(url, headers=header, proxies=self._get_proxy())
        elif method == c.POST:
            response = requests.post(url, data=body, headers=header, proxies=self._get_proxy())

        # exception handle
        # print(response.headers)

        if not str(response.status_code).startswith('2'):
            raise exceptions.OkxAPIException(response)

        return response.json()

    def _request_without_params(self, method, request_path):
        return self._request(method, request_path, {})

    def _request_with_params(self, method, request_path, params):
        return self._request(method, request_path, params)

    def _get_timestamp(self):
        url = c.API_URL + c.SERVER_TIMESTAMP_URL
        response = requests.get(url, proxies=self._get_proxy())
        if response.status_code == 200:
            return response.json()['data'][0]['ts']
        else:
            return ""
