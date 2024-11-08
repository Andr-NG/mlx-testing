import requests
import utils
import allure
import os
from dotenv import load_dotenv
from models import MLX as mlx_models

load_dotenv()
helper = utils.Helper()


class MLX:

    def __init__(self, url: str) -> None:
        self.url = url
        self.username = os.getenv('USERNAME')
        self.password = os.getenv('DEV_PASS')

    @allure.step('Creating a new account')
    def sign_up(self, login: str, user_pass: str) -> dict:
        """Sign up

        Args:
            login (str): email
            user_pass (str): password

        Returns:
            dict: SignUp response
        """
        URL = self.url + "/user/signup"
        user_creds = mlx_models.UserCreds(email=login, password=user_pass)
        body = mlx_models.ComplexSignup(creds=user_creds)
        data = requests.post(url=URL, data=body.to_json())
        return data.json()

    def verify_email(self, email: str, email_token: str, jwt: str):
        URL = self.url + f'/user/verify_email?email={email}&token={email_token}'
        res = requests.get(url=URL, headers=helper.get_headers(token=jwt))
        return res.json()

    @allure.step('Signing in to get the token and refresh token')
    # adds a step in the allure report test set-up.
    def sign_in(self, login: str, password: str) -> dict:
        """Sign in

        Args:
            login (str): email
            password (str): pass

        Returns:
            dict:
        """
        URL = self.url + "/user/signin"
        credentials = mlx_models.UserCreds(email=login, password=password)
        data = requests.post(url=URL, data=credentials.to_json())
        # response = MLX.SigninResponse(**data.json())
        return data.json()

    @allure.step('Updating the token and refresh token')
    def refresh_token(self, email: str, wid: str, refresh_token: str) -> dict:
        URL = self.url + "/user/refresh_token"
        body = mlx_models.RefreshToken(email=email, refresh_token=refresh_token, workspace_id=wid)
        data = requests.post(url=URL, data=body.to_json())
        return data.json()

    @allure.step("Retrieving the folder id for Owner")
    def get_folder_id(self, token: str) -> dict:
        """Get the folder id

        Args:
            token (str): token from authorisation

        Returns:
            dict: list of available workspaces
        """
        URL = self.url + "/workspace/folders"
        HEADERS = helper.get_headers(token)
        data = requests.get(url=URL, headers=HEADERS)
        # response = MLX.UserFolderArrayResponse(**data.json())
        return data.json()

    @allure.step("Retrieving the workspace id for Owner")
    def get_workspace_id(self, token: str) -> dict:
        """Get the workspace id

        Args:
            token (str): token from authorisation

        Returns:
            dict: list of available workspaces
        """
        URL = self.url + "/user/workspaces"
        HEADERS = helper.get_headers(token)
        data = requests.get(url=URL, headers=HEADERS)
        return data.json()

    @allure.step('Creating profile with the following body: {profile_params}')
    def create_profile(self, token: str, profile_params: dict) -> dict:
        """Create a profile with preset profile params.

        Args:
            token (str): Bearer token
            profile_params (str): Profile metas

        Returns:
            dict (requests.Response)
        """
        URL = self.url + "/profile/create"
        HEADERS = helper.get_headers(token)
        body = mlx_models.CreateProfile.from_dict(profile_params)
        data = requests.post(url=URL, data=body.to_json(), headers=HEADERS)
        # response = MLX.ArrayOfIDsResponse(**data.json())
        return data.json()

    def delete_profile(self, token: str, profile_ids: list, permanently=True) -> requests.Response:
        """Delete a profiles

        Args:
            token (str): Bearer token
            profile_ids (list): list of profiles to delete

        Returns:
            requests.Response
        """
        URL = self.url + "/profile/remove"
        HEADERS = helper.get_headers(token)
        body = mlx_models.RemoveProfiles(ids=profile_ids, permanently=permanently)
        data = requests.post(url=URL, data=body.to_json(), headers=HEADERS)
        # response = MLX.MLXResponse(**data.json())
        return data.json()
