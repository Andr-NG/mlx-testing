import configparser
import os


class ConfigProvider:

    def __init__(self, filename: str) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(filename)

    def get_url(self, section: str, key='DEV') -> str:
        session_env = os.getenv('ENV')
        if session_env in ('QA', 'STG', 'PROD'):
            key = session_env
            return self.config[section].get(key)
        else:
            return self.config[section].get(key)

    def get_file_path(self, file: str, section='PATH') -> str:
        return self.config[section].get(file)
