import json
import jwt
import utils
import logging
import API
import models
from models.MLX import SigninResponse
from datetime import datetime
from pydantic import ValidationError


config = utils.ConfigProvider("config.ini")
logger = logging.getLogger("my_logger")

FILE_PATH = config.get_file_path("USER_DATA")


class Helper:

    def get_headers(self, token: str) -> dict[str, str]:
        """Composing headers for a request

        Args:
            token (str): token

        Returns:
            dict[str, str]: headers with Bearer Token
        """
        headers = {"Accept": "application/json"}
        headers.setdefault("Authorization", f"Bearer {token}")
        return headers

    def get_user_data(self) -> models.UserData:
        """Creating an instance of the UserData model to validate and access user data

        Returns:
            models.UserData: easy-to-access user data
        """
        path = config.get_file_path(file="USER_DATA")
        data = utils.DataProvider(file_path=path).data
        return models.UserData(**data)

    def decode_token(self, token: str) -> tuple[str, str, str]:
        """Decoding the token to extract user data

        Args:
            token (str): token

        Returns:
            tuple[str, str, str]: user role, workspace id, token expiration date
        """
        decoded = jwt.decode(jwt=token, options={"verify_signature": False})
        default_workspace_id = decoded["workspaceID"]
        role = decoded["workspaceRole"]
        exp_time = decoded["exp"]
        return role, default_workspace_id, exp_time

    def update_user_data_file(
       self, token: str, refresh_token: str, default_folder_id: str | None = None
    ) -> None:
        """Reading and updating the user data file to have the latest data.

        Args:
            token (str): token
            refresh_token (str): refresh token
            default_folder_id (str | None, optional): profile id. Defaults to None.
        """
        role, default_workspace_id, _ = self.decode_token(token)

        if default_folder_id is None:
            with open(FILE_PATH, "r") as file:
                data: dict = json.load(file)
            data[role]["workspace_id"] = default_workspace_id
            data[role]["token"] = token
            data[role]["refresh_token"] = refresh_token
        else:
            with open(FILE_PATH, "r") as file:
                data: dict = json.load(file)
            data[role]["workspace_id"] = default_workspace_id
            data[role]["token"] = token
            data[role]["refresh_token"] = refresh_token
            data[role]["folder_id"] = default_folder_id

        with open(FILE_PATH, "w") as file:
            json.dump(data, file, indent=4)

    def verify_token(self, token: str) -> str | None:
        """Verify the token to either refresh it or simply return it

        Args:
            token (str): token to be validated

        Returns:
            str: updated token
        """
        provide: models.UserData = self.get_user_data()
        logger.info("Decoding the token to verify exp_time")
        role, _, exp_time = self.decode_token(token=token)
        self.mlx_api = API.MLX(url=config.get_url(section="MLX_API"))
        if datetime.fromtimestamp(exp_time) > datetime.now():
            logger.info("Returning the token, because it is still valid.")
            return token
        else:
            try:
                # Verifying the owner's token and updating it if necessary
                if role == "owner":
                    logger.info(f"Token is expired. Fetching a new {role} token.")
                    response = self.mlx_api.refresh_token(
                        email=provide.owner.email,
                        wid=provide.owner.workspace_id,
                        refresh_token=provide.owner.refresh_token,
                    )
                    logger.info('Receiving a new token %s', response)
                    parsed = SigninResponse(**response)
                    logger.info("Updating the owner token in the user data file.")
                    self.update_user_data_file(
                        token=parsed.data.token, refresh_token=parsed.data.refresh_token
                    )
                    logger.info("Returning the updated token.")
                    return parsed.data.token

                # Verifying the manager's token and updating it if necessary
                if role == "manager":
                    logger.info(f"Token is expired. Fetching a new {role} token.")
                    response = self.mlx_api.refresh_token(
                        email=provide.manager.email,
                        wid=provide.manager.workspace_id,
                        refresh_token=provide.manager.refresh_token,
                    )
                    logger.info('Receiving a new token %s', response)
                    parsed = SigninResponse(**response)
                    logger.info("Updating the manager token in the user data file.")
                    self.update_user_data_file(
                        token=parsed.data.token, refresh_token=parsed.data.refresh_token
                    )
                    logger.info("Returning the updated token.")
                    return parsed.data.token

                # Verifying the user's token and updating it if necessary
                if role == "user":
                    logger.info(f"Token is expired. Fetching a new {role} token.")
                    response = self.mlx_api.refresh_token(
                        email=provide.user.email,
                        wid=provide.user.workspace_id,
                        refresh_token=provide.user.refresh_token,
                    )
                    logger.info('Receiving a new token %s', response)
                    parsed = SigninResponse(**response)
                    logger.info("Updating the user token in the user data file.")
                    self.update_user_data_file(
                        token=parsed.data.token, refresh_token=parsed.data.refresh_token
                    )
                    logger.info("Returning the updated token.")
                    return parsed.data.token

                # Verifying the launcher's token and updating it if necessary
                if role == "launcher":
                    logger.info(f"Token is expired. Fetching a new {role} token.")
                    response = self.mlx_api.refresh_token(
                        email=provide.launcher.email,
                        wid=provide.launcher.workspace_id,
                        refresh_token=provide.launcher.refresh_token,
                    )
                    logger.info('Receiving a new token %s', response)
                    parsed = SigninResponse(**response)
                    logger.info("Updating the launcher token in the user data file.")
                    self.update_user_data_file(
                        token=parsed.data.token, refresh_token=parsed.data.refresh_token
                    )
                    logger.info("Returning the updated token.")
                    return parsed.data.token

            except ValidationError as e:
                logger.error("Validation error occurred: %s", e)
                raise
            except Exception as e:
                logger.error("An unexpected error occurred: %s", e)
                raise


# def create_profile(token: str, body: dict) -> List[str]:
#     try:
#         res = mlx_api.create_profile(token=token, profile_params=body)
#         response = ArrayOfIDsResponse(**res)
#         logger.info("Creating profiles: %s", res)
#         profile_list: List[str] = response.data.ids
#         return profile_list

#     except Exception as e:
#         logger.error("An unexpected error occurred: %s", e)
#         raise


# def remove_profile(token: str, profiles: list) -> dict:
#     try:
#         logger.info("Removing profiles %s", profiles)
#         response = mlx_api.delete_profile(
#             token=token, profile_ids=profiles, permanently=True)
#         return response
#     except Exception as e:
#         logger.error("An unexpected error occurred: %s", e)
#         raise
