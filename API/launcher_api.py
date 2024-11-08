import requests
import utils
from models import launcher


utils = utils.Helper()


class Launcher:

    def __init__(self, url: str) -> None:
        self.url = url

    def start_profile(self, token, profile_id, folder_id) -> dict:
        URL = self.url + f"/profile/f/{folder_id}/p/{profile_id}/start"
        HEADERS = utils.get_headers(token)
        data = requests.get(url=URL, headers=HEADERS)
        # response = API.ResponseStatus(**data.json())
        return data.json()

    def stop_profile(self, token, profile_id) -> dict:
        # URL is hardcoded because the stop-profile endpoint is available only in v1
        URL = f"https://launcher.mlx.yt:45001/api/v1/profile/stop/p/{profile_id}"
        HEADERS = utils.get_headers(token)
        data = requests.get(url=URL, headers=HEADERS)
        # response = API.ResponseStatus(**data.json())
        return data.json()

    def import_cookies(self, token, pid, fid, cookies, xpass_load=False) -> dict:
        URL = self.url + "/cookie_import"
        HEADERS = utils.get_headers(token)
        body = launcher.CookieImport(
            profile_id=pid,
            folder_id=fid,
            cookies=cookies,
            import_advanced_cookies=xpass_load,
        )
        data = requests.post(
            url=URL, data=body.to_json(), headers=HEADERS
        )
        # response = MLX.MLXResponse(**data.json())
        return data.json()
