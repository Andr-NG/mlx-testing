import requests
import allure
import data
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os


load_dotenv()


class EMP:

    def __init__(self, url: str) -> None:
        self.url = url
        self.env = os.getenv('ENV', 'DEV')
        if self.env not in ('QA', 'STG', 'PROD', 'DEV'):
            raise ValueError(f"Unsupported environment: {self.env}")
        self.basic_auth = HTTPBasicAuth(username='admin', password=os.getenv(self.env))

    @allure.step('Retrieving email token')
    def get_email_token(self, email: str) -> dict:
        params = {'email': email}
        URL = self.url + '/emp/verification_token'
        res = requests.get(url=URL, params=params, auth=self.basic_auth)
        return res.json()

    @allure.step('Setting restrictions')
    def set_restrictions(self, workspace_id: str):
        body = data.RESTRICTIONS
        body['workspace_id'] = workspace_id
        URL = self.url + '/emp/restrictions'
        res = requests.post(url=URL, json=body, auth=self.basic_auth)
        return res.json()