# flake8: noqa
import pytest
import logging
import API
import utils
from pytest import FixtureRequest
from typing import Any, Generator, List
from models.user_data import UserData
from models import MLX as models
from data.profile_data import PROFILE_GENERIC
from pydantic import ValidationError

helper = utils.Helper()

# Create a logger with a name specific to your project
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)

# Create a handler and a formatter (console/file handler as needed)
handler = logging.FileHandler(filename="my_logs.log", mode="w")
formatter = logging.Formatter(
    fmt="%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]",
    datefmt="%d/%m/%Y %H:%M:%S",
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Avoid duplicating logs
logger.propagate = False


@pytest.fixture(scope="session")
def generate_owner_email() -> Generator[str, Any, None]:
    name_owner = 'andrey.nguyenmain'
    domain = '@multilogin.com'

    with open('index.txt', 'r') as f:
        data = f.read()

    ind = int(data) + 1
    email = name_owner + str(ind) + domain
    yield email

    with open('index.txt', 'w') as f:
        f.write(str(ind))


@pytest.fixture(scope="session")
def config() -> utils.ConfigProvider:
    """Setting up a config provider

    Returns:
        utils.ConfigProvider: ConfigProvider class
    """
    return utils.ConfigProvider("config.ini")


@pytest.fixture(scope="session", autouse=True)
def mlx_api(config: utils.ConfigProvider) -> API.MLX:
    logger.info("MLX API instantiated")
    URL = config.get_url(section="MLX_API")
    return API.MLX(url=URL)


@pytest.fixture(scope="session", autouse=True)
def emp_api(config: utils.ConfigProvider) -> API.EMP:
    logger.info("EMP API instantiated")
    URL = config.get_url(section="MLX_API")
    return API.EMP(url=URL)


@pytest.fixture(scope="session", autouse=True)
def launcher_api(config: utils.ConfigProvider) -> API.Launcher:
    logger.info("Launcher API instantiated")
    URL = config.get_url(section="LAUNCHER_API", key='LAUNCHER_URL_v2')
    return API.Launcher(url=URL)


@pytest.fixture(scope="session")
def provide(config: utils.ConfigProvider) -> dict:
    path = config.get_file_path(file="USER_DATA")
    user_data = utils.DataProvider(file_path=path).data
    return UserData(**user_data)


# @pytest.fixture(scope="session")
# def get_owner_token(provide: UserData) -> str:
#     return helper.verify_token(token=provide.owner.token)


# @pytest.fixture(scope="session")
# def get_manager_token(provide: UserData) -> str:
#     return helper.verify_token(provide.manager.token)


# @pytest.fixture(scope="session")
# def get_launcher_token(provide: UserData) -> str:
#     return helper.verify_token(provide.launcher.token)


# @pytest.fixture(scope="session")
# def get_user_token(provide: UserData) -> str:
#     return helper.verify_token(provide.user.token)


# @pytest.fixture(scope="session")
# def get_owner_folder_id(provide: UserData) -> str:
#     return provide.owner.folder_id


# @pytest.fixture(scope="session")
# def get_manager_folder_id(provide: UserData) -> str:
#     return provide.manager.folder_id


# @pytest.fixture(scope="session")
# def get_user_folder_id(provide: UserData) -> str:
#     return provide.user.folder_id


# @pytest.fixture(scope="session")
# def get_launcher_folder_id(provide: UserData) -> str:
#     return provide.launcher.folder_id


# @pytest.fixture()
# def create_profile(
#     mlx_api: API.MLX, request: FixtureRequest, get_owner_token, get_owner_folder_id
# ) -> Generator[str, Any, None]:
#     """Creating a profile

#     Args:
#         mlx_api (API.MLX): MLX API
#         get_owner_token (str): reading token from user_data.json.
#         get_owner_folder_id (str): reading folder_id from user_data.json.
#         remove (boolean): flag to remove a created profile

#     Yields:
#         Generator[str, Any, None]: returning a list with profiles created.
#     """
#     # if remove is provided via pytest.mark.parametrize, it will be used via request.param.
#     remove = request.param if hasattr(request, "param") else True
#     try:
#         body = PROFILE_GENERIC
#         body.update({"folder_id": get_owner_folder_id})
#         res = mlx_api.create_profile(token=get_owner_token, profile_params=body)
#         response = models.ArrayOfIDsResponse(**res)
#         profile_list: List[str] = response.data.ids
#         logger.info("Creating profile: %s", res)

#         yield profile_list

#         if remove:
#             delete = mlx_api.delete_profile(
#                 token=get_owner_token, profile_ids=profile_list
#             )
#             logger.info("Removing profile %s", delete)

#     except (ValidationError, KeyError) as e:
#         logger.error("Validation or Key error occurred: %s", e)
#         raise

#     except Exception as e:
#         logger.error("An unexpected error occurred: %s", e)
#         raise
