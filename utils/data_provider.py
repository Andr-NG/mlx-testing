import json
import os


class DataProvider:

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        with open(file_path, 'r') as file:
            self.data = json.load(file)


if __name__ == '__main__':
    current_dir = os.getcwd()
    # sub_folder = 'data'
    # file_name = 'user_data.json'
    # provider = DataProvider(os.path.join(current_dir, sub_folder, file_name))
    # from models.user_data import UserData as UD
    # print(UD(**provider.data).owner.password)
    print(current_dir)
    for dir in os.listdir(current_dir):
        print(dir)
