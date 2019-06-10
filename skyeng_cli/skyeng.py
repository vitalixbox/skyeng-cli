import requests
import logging


logger = logging.getLogger(__name__)


class SkyengApiError(Exception):
    pass


class SkyengApiAuth:
    def __init__(self, username=None, password=None, token_global=None):
        self._username = username
        self._password = password
        self._token_global = token_global

    def auth(self):
        if self._token_global:
            return self

        elif self._username and self._password:
            api = BaseApi('https://id.skyeng.ru')

            res = api.post(
                path='/api/v1/auth/login-form',
                payload={
                    '_username': self._username,
                    '_password': self._password,
                },
                headers={}
            )
            if not res.json()['success']:
                raise SkyengApiError('Auth failed: {}'.format(res.json()))

            res = api.post(
                path='/user-api/v1/auth/jwt',
                cookies=res.cookies.get_dict()
            )
            self._token_global = res.cookies.get_dict()['token_global']

        else:
            raise NotImplementedError

        return self

    @property
    def token_global(self):
        return self._token_global

    @property
    def auth_cookies(self):
        return {'token_global': self._token_global}

    @classmethod
    def from_userpass(cls, username, password):
        return SkyengApiAuth(username=username, password=password)

    @classmethod
    def from_token_global(cls, token_global):
        return SkyengApiAuth(token_global=token_global)


class SkyengApi:
    def __init__(self, auth):
        self._rooms_api = BaseApi('https://rooms.vimbox.skyeng.ru')
        self._words_api = BaseApi('https://api.words.skyeng.ru')
        self._dictionary_api = BaseApi('https://dictionary.skyeng.ru')
        self._auth = auth

    def get_profile(self):
        res = self._rooms_api.post(
            path='/users/api/v1/auth/config',
            cookies=self._auth.auth().auth_cookies
        )
        return res.json()['user']

    def get_wordsets(self, user_id):
        res = self._words_api.get(
            path='/api/for-vimbox/v1/wordsets.json?studentId={}&pageSize=500&page=1'.format(user_id),
            headers=self._bearer_headers
        )
        return res.json()['data']

    def get_words(self, user_id, wordset_id):
        res = self._words_api.get(
            '/api/v1/wordsets/{}/words.json?studentId={}&wordsetId={}&pageSize=500&page=1'.format(
                wordset_id, user_id, wordset_id
            ),
            headers=self._bearer_headers
        )
        return res.json()['data']

    def get_meanings(self, meaning_ids):
        meaning_ids = [str(mi) for mi in meaning_ids]
        res = self._dictionary_api.get(
            '/api/for-services/v2/meanings?ids={}'.format(','.join(meaning_ids)),
        )
        return res.json()

    @property
    def _bearer_headers(self):
        return {'Authorization': 'Bearer {}'.format(self._auth.auth().token_global)}
