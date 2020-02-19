import requests
import json
import argparse
import config
from bs4 import BeautifulSoup
from datetime import datetime

JINS_BASE_URL = config.JINS_API_BASE_URL
payload_login = config.LOGIN_INFO
payload_token = config.TOKEN
code_headers = config.GET_CODE_HEADERS
token_headers =  config.GET_TOKEN_HEADERS
info_headers = config.GET_INFO_HEADERS
# proxies = config.PROXY


class GetAllowCode():
    def __init__(self, client_id, client_secret, date):
        self.client_id = client_id
        self.client_secret = client_secret
        self.date = date

    def login_url(self):
        get_url_info = 'https://accounts.jins.com/jp/ja/oauth/authorize?response_type=' \
                'code&client_id={}&redirect_uri={}&state=hoge&scope=office%20run%20drive&service_id=meme'.format(self.client_id, JINS_BASE_URL)
        with requests.Session() as session:
            url = session.get(
                get_url_info,
                # proxies=proxies
                )
            soup = BeautifulSoup(url.text, "lxml")
            auth_token = soup.find(attrs={'name': 'authenticity_token'}).get('value')
            payload_login['authenticity_token'] = auth_token
            response_cookie = url.cookies
            res = session.post('https://accounts.jins.com/jp/ja/login?service_id=meme',
                                data=payload_login,
                                headers=code_headers,
                                # proxies=proxies
                                )
            res.raise_for_status()
            code = res.url.split('=')[1].split('&')[0]
        return code

    def get_access_token(self, code, time_count):
        oath_url = 'https://apis.jins.com/meme/v1/oauth/token'
        payload_token['client_id'] = self.client_id
        payload_token['client_secret'] = self.client_secret
        payload_token['code'] = code
        r = requests.post(oath_url, payload_token, headers=token_headers)
        r.raise_for_status()
        office_info = GetAllowCode._get_office_info(self, json.loads(r.text)['access_token'], self.date, time_count)
        return office_info

    def _get_office_info(self, access_token, date, time_count):
        day = datetime.strptime(date, '%Y%m%d')
        time = time_count
        office_url = 'https://apis.jins.com/meme/v1/users/me/office2/' \
                'computed_data?type=computed_data2&date_from=' \
                '{0}-{1}-{2}T00%3A00%3A00%2B09%3A00&date_to={0}-{1}-{2}' \
                'T{3}%3A{4}%3A{5}%2B09%3A00'.format(
                                                day.strftime('%Y'),
                                                day.strftime('%m'),
                                                day.strftime('%d'),
                                                time.strftime('%H'),
                                                time.strftime('%M'),
                                                time.strftime('%S')
                                                )
        info_headers['authorization'] = 'bearer' + ' ' + access_token
        res_office = requests.get(office_url,
            headers=info_headers,
            # proxies=proxies
            )
        res_office.raise_for_status()
        return res_office.text