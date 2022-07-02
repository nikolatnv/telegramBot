import json
import os

path_json = os.path.abspath('data.json')
with open(path_json, "r") as f:
    data = json.load(f)


def get_token():
    return data['token']


def get_dir_tmp():
    return data['tmp']


def get_dir_dirs():
    return data['dirs']


def get_users():
    return data['users']


def get_dir_pass():
    return data['pass']


def default_photo_path():
    return data['default_photo_path']

