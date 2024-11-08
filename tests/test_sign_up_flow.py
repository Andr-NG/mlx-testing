import API
import logging
import pytest
import data
import time
from pytest import FixtureRequest
from models import MLX as mlx_models
from typing import Any, Generator, List
from models.user_data import UserData
from pydantic import ValidationError
from models import EMP as emp_models
from models import launcher as launcher_models

logger = logging.getLogger("my_logger")


@pytest.fixture()
def sign_up(mlx_api: API.MLX, provide: UserData, generate_owner_email: Generator) -> dict:
    """Sign up

    Args:
        mlx_api (API.MLX): MLX API instance.
        provide (UserData): Fixture to provide data.
        generate_owner_email (Fixture): Fixture to generate email.

    Returns:
        dict: sign-up response
    """
    # Step 1: Sign up
    try:
        sign_up_data = mlx_api.sign_up(
            login=generate_owner_email, user_pass=provide.owner.password
        )
        return sign_up_data
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        raise


@pytest.fixture()
def get_email_token(emp_api: API.EMP, generate_owner_email: Generator) -> emp_models.TokenResponse:
    """Get email token for verification

    Args:
        emp_api (API.EMP): EMP API instance.
        generate_owner_email (Fixture): Fixture to generate email.

    Returns:
        dict: Email verification token.
    """
    # Step 2: Get Email Token
    try:
        email_token_data = emp_api.get_email_token(email=generate_owner_email)
        response = emp_models.TokenResponse(**email_token_data)
        return response
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        raise


@pytest.fixture(scope="session")
def sign_in(
    mlx_api: API.MLX, provide: UserData, generate_owner_email
) -> tuple[str, str]:
    """Sign in to get token

    Args:
        mlx_api (API.MLX): MLX API instance.
        provide (UserData): Fixture to provide data.
        generate_owner_email (Fixture): Fixture to generate email.

    Returns:
        tuple[str, str]: tuple with token and refresh token.
    """
    # Step 3: Sign in
    try:
        logger.info("Signing in with %s", generate_owner_email)
        sign_in_data = mlx_api.sign_in(
            login=generate_owner_email, password=provide.owner.password
        )
        sign_in_response = mlx_models.SigninResponse(**sign_in_data)
        token = sign_in_response.data.token
        refresh_token = sign_in_response.data.refresh_token
        return token, refresh_token
    except ValidationError as e:
        logger.error("Validation or Assertion error occurred: %s", e)
        raise
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        raise


@pytest.fixture()
def sign_in_to_verify(
    mlx_api: API.MLX, provide: UserData, generate_owner_email: Generator
) -> mlx_models.SigninResponse:
    """Sign in to verify only

    Args:
        mlx_api (API.MLX): MLX API instance.
        provide (UserData): Fixture to provide data.
        generate_owner_email (Fixture): Fixture to generate email.

    Returns:
        mlx_models.SigninResponse: mlx_models.SigninResponse
    """
    # Step 3: Sign in
    try:
        sign_in_data = mlx_api.sign_in(
            login=generate_owner_email, password=provide.owner.password
        )
        sign_in_response = mlx_models.SigninResponse(**sign_in_data)
        return sign_in_response
    except ValidationError as e:
        logger.error("Validation or Assertion error occurred: %s", e)
        raise
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        raise


@pytest.fixture()
def verify_email(
    mlx_api: API.MLX,
    generate_owner_email: Generator,
    get_email_token: emp_models.TokenResponse,
    sign_in_to_verify: mlx_models.SigninResponse,
) -> dict:
    """Verify email.

    Args:
        mlx_api (API.MLX): MLX API instance.
        generate_owner_email (Fixture): Fixture to generate email.
        get_email_token (Fixture): Fixture to get email token.
        sign_in_to_verify (Fixture): Fixture to sign in verify account.

    Returns:
        dict: Verification email response.
    """
    # Step 4: Verify Email
    token = sign_in_to_verify.data.token
    email_token = get_email_token.data.token
    try:
        verify_data = mlx_api.verify_email(
            email=generate_owner_email, email_token=email_token, jwt=token
        )
        logger.info(f"Verification response: {verify_data}")
        return verify_data
    except (ValidationError, AssertionError) as e:
        logger.error("Validation or Assertion error occurred: %s", e)
        raise
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        raise


@pytest.fixture(scope="session")
def get_workspace_id(mlx_api: API.MLX, sign_in: tuple) -> str:
    """Get workspace id

    Args:
        mlx_api (API.MLX): MLX API instance.
        sign_in (Fixture): Fixture to sign in to get token.

    Returns:
        str: Workspace ID.
    """
    # Step 4: Get workspace_id
    token, _ = sign_in
    try:
        logger.info("Requesting workspace_id")
        wid_data = mlx_api.get_workspace_id(token=token)
        workspace_id = mlx_models.UserWorkspaceArrayResponse(**wid_data)
        logger.info("Workspace ID response: %s", workspace_id)
        return workspace_id.data.workspaces[0].workspace_id
    except ValidationError as e:
        logger.error("Validation or Assertion error occurred: %s", e)
        raise
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        raise


@pytest.fixture()
def enable_plan(emp_api: API.EMP, get_workspace_id: str) -> dict:
    """Set restrictions.

    Args:
        emp_api (API.EMP): EMP API instance.
        get_workspace_id (Fixture): Fixture to get workspace id.

    Returns:
        dict: Set restriction response.
    """
    # Step 5: Assign plan
    try:
        data = emp_api.set_restrictions(workspace_id=get_workspace_id)
        return data
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        raise


@pytest.fixture(scope="session")
def get_folder_id(mlx_api: API.MLX, sign_in: tuple) -> str:
    """Get folder id.

    Args:
        mlx_api (API.MLX): MLX API instance.
        sign_in (Fixture): Fixture to sign in to get token.

    Returns:
        str: Folder ID.
    """
    # Step 4: Get folder_id
    token, _ = sign_in
    try:
        fid_data = mlx_api.get_folder_id(token=token)
        folders = mlx_models.UserFolderArrayResponse(**fid_data)
        for folder in folders.data.folders:
            if folder.name == "Default folder":
                return folder.folder_id
    except ValidationError as e:
        logger.error("Validation or Assertion error occurred: %s", e)
        raise
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        raise


@pytest.fixture(scope="session")
def create_profile(
    mlx_api: API.MLX, request: FixtureRequest, sign_in: tuple, get_folder_id: str
) -> Generator[str, Any, None]:
    """Create profile.

    Args:
        mlx_api (API.MLX): MLX API instance.
        request (FixtureRequest): Fixture request.
        sign_in (Fixture): Fixture to sign in to get token.
        get_folder_id (Fixture): Fixture to get folder id.

    Yields:
        Generator[str, Any, None]: list of profiles.
    """

    # if remove is provided via pytest.mark.parametrize, it will be used via request.param.
    remove = request.param if hasattr(request, "param") else True
    try:
        body = data.PROFILE_GENERIC
        body.update({"folder_id": get_folder_id})
        token, _ = sign_in
        res = mlx_api.create_profile(token=token, profile_params=body)
        response = mlx_models.ArrayOfIDsResponse(**res)
        profile_list: List[str] = response.data.ids

        yield profile_list

        if remove:
            delete = mlx_api.delete_profile(token=token, profile_ids=profile_list)
            logger.info("Removing profile %s", delete)

    except (ValidationError, KeyError) as e:
        logger.error("Validation or Key error occurred: %s", e)
        raise

    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        raise


class TestE2ESignUp:

    def test_sign_up(
            self, sign_up: dict, request: FixtureRequest, generate_owner_email: Generator
    ) -> None:
        logger.info(f"Executing {request.node.name}")
        logger.info("Attempting sign-up with %s", generate_owner_email)
        try:
            data = sign_up
            logger.info(f"Sign up response: {data}")
            logger.info("Doing validations and assertions ...")
            sign_up_response = mlx_models.MLXResponse(**data)
            assert sign_up_response.status.http_code == 201, "Failed at sign up step"
            assert sign_up_response.status.message == "Successful signup"
        except (ValidationError, AssertionError) as e:
            logger.error("Validation or Assertion error occurred: %s", e)
            raise
        finally:
            logger.info(f"Finishing {request.node.name}")

    def test_get_email_token(
        self, get_email_token: emp_models.TokenResponse,
        request: FixtureRequest
    ) -> None:
        logger.info(f"Executing {request.node.name}")
        logger.info("Receiving email token")
        logger.info(f"Email token response: {get_email_token}")
        try:
            logger.info("Doing assertions")
            assert get_email_token.data.token, "No token returned"
        except (AssertionError, ValidationError) as e:
            logger.error("Validation or Assertion error occurred: %s", e)
            raise
        finally:
            logger.info(f"Finishing {request.node.name}")

    def test_sign_in_to_verify(
            self, sign_in_to_verify: mlx_models.SigninResponse, request: FixtureRequest
    ) -> None:
        logger.info(f"Executing {request.node.name}")
        logger.info("Signing in to verify")
        sign_in_response: mlx_models.SigninResponse = sign_in_to_verify
        logger.info("Sign-in response: %s", sign_in_response.status)
        token = sign_in_response.data.token
        refresh_token = sign_in_response.data.refresh_token

        try:
            logger.info("Doing assertions")
            assert token, "No token returned"
            assert refresh_token, "No refresh token returned"
        except (AssertionError, ValidationError) as e:
            logger.error("Validation or Assertion error occurred: %s", e)
            raise
        finally:
            logger.info(f"Finishing {request.node.name}")

    def test_verify_email(self, verify_email: dict, request: FixtureRequest) -> None:
        logger.info(f"Executing {request.node.name}")
        logger.info("Verifying email...")
        data = verify_email
        verify_response = mlx_models.MLXResponse(**data)
        logger.info("Verify email response: %s", verify_response)

        try:
            logger.info("Doing assertions")
            assert (
                verify_response.status.http_code == 200
            ), "Failed at email verification step"
            assert verify_response.status.message == "Email successfully verified"
        except (ValidationError, AssertionError) as e:
            logger.error("Validation or Assertion error occurred: %s", e)
            raise
        finally:
            logger.info(f"Finishing {request.node.name}")

    def test_set_restrictions(self, request: FixtureRequest, enable_plan: dict) -> None:
        logger.info(f"Executing {request.node.name}")
        logger.info("Assigning plan")
        data = enable_plan
        logger.info("Set resrtictions response %s", data)
        response = mlx_models.MLXResponse(**data)

        try:
            logger.info("Doing assertions")
            assert response.status.http_code == 200, "Failed at setting restricions"
        except (ValidationError, AssertionError) as e:
            logger.error("Validation or Assertion error occurred: %s", e)
            raise
        finally:
            logger.info(f"Finishing {request.node.name}")

    def test_get_folder_id(self, request: FixtureRequest, get_folder_id: str) -> None:
        logger.info(f"Executing {request.node.name}")
        logger.info("Requesting folder_id")
        folder_id = get_folder_id
        logger.info("Folder ID %s", folder_id)

        try:
            logger.info("Doing assertions")
            assert folder_id, "Folder ID not correct"
        except AssertionError as e:
            logger.error("Validation or Assertion error occurred: %s", e)
            raise
        finally:
            logger.info(f"Finishing {request.node.name}")

    def test_create_profile(
            self, create_profile: Generator, request: FixtureRequest
    ) -> None:
        logger.info(f"Executing {request.node.name}")
        logger.info("Creating profile...")
        profile_list = create_profile
        logger.info("Profiles created: %s", profile_list)

        try:
            logger.info("Doing assertions")
            assert len(profile_list) >= 1, "Wrong number of profiles created"
        except AssertionError as e:
            logger.error("Validation or Assertion error occurred: %s", e)
            raise
        finally:
            logger.info(f"Finishing {request.node.name}")

    def test_launcher_profile(
        self, create_profile: Generator, get_folder_id: str, sign_in: tuple,
        request: FixtureRequest, launcher_api: API.Launcher
    ) -> None:
        logger.info(f"Executing {request.node.name}")
        pid = create_profile[0]
        token, _ = sign_in
        data = launcher_api.start_profile(
            profile_id=pid, folder_id=get_folder_id, token=token
        )
        response = launcher_models.Response(**data)
        logger.info(f"Launching profile {pid}: {response}")

        try:
            logger.info("Doing assertions")
            assert response.status.http_code == 200, "Failed to launch profile"
        except (AssertionError, ValidationError) as e:
            logger.error("Validation or Assertion error occurred: %s", e)
            raise
        finally:
            logger.info(f"Finishing {request.node.name}")

    def test_close_profile(
        self, create_profile: Generator,
        request: FixtureRequest, launcher_api: API.Launcher,
        sign_in: tuple
    ) -> None:
        logger.info(f"Executing {request.node.name}")
        pid = create_profile[0]
        token, _ = sign_in
        time.sleep(3)
        data = launcher_api.stop_profile(profile_id=pid, token=token)
        logger.info(f"Stoping profile {pid}: {data}")
        response = launcher_models.Response(**data)

        try:
            logger.info("Doing assertions")
            assert response.status.http_code == 200, "Failed to stop profile"
        except (AssertionError, ValidationError) as e:
            logger.error("Validation or Assertion error occurred: %s", e)
            raise
        finally:
            logger.info(f"Finishing {request.node.name}")
