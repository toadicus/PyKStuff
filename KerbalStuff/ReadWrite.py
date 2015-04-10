__author__ = 'toadicus'

import os
import requests
import zipfile

from requests.cookies import RequestsCookieJar
from .ReadOnly import KerbalStuffReadOnly
from .Constants import Constants
from .Mod import Mod, ModVersion

Constants.login = Constants.format_action("/login")
Constants.mod_create = Constants.format_action("/mod/create")
Constants.mod_update = Constants.format_action("/mod/{0:d}/update")


class KerbalStuff(KerbalStuffReadOnly):
    current_cookies = None
    """:type : RequestsCookieJar"""
    @classmethod
    def do_post_request(cls,
                        uri: str,
                        *format_args,
                        data: dict=None,
                        files: dict=None,
                        cookies: RequestsCookieJar=None
                        ):
        cls.current_response = None
        cls.current_json = None
        cls.current_cookies = None

        if len(format_args) > 0:
            uri = uri.format(*format_args)

        cls.current_response = requests.post(uri, headers=Constants.headers, data=data, files=files, cookies=cookies)

        try:
            cls.current_json = cls.current_response.json()
        except ValueError:
            sys.stderr.write("Response received was not valid JSON\n")
            sys.exit(1)

    @classmethod
    def login(cls, username: str, password: str):
        data = {'username': username, 'password': password}

        cls.do_post_request(Constants.login, data=data)

        if cls.current_json is not None and not cls.current_json["error"]:
            cls.current_cookies = cls.current_response.cookies

    @classmethod
    def mod_create(cls, mod: Mod, file_name: str, file_path: str):
        if not Mod or not isinstance(mod, Mod):
            raise TypeError("mod argument must be a valid Mod object")

        if mod.name is None or len(mod.name) == 0:
            raise TypeError("mod.name cannot be empty")
        if mod.license is None or len(mod.license) == 0:
            raise TypeError("mod.license cannot be empty")
        if mod.short_description is None or len(mod.short_description) == 0:
            raise TypeError("mod.short_description cannot be empty")
        if len(mod.versions) != 1:
            raise TypeError("mod must have a single version to create")
        if mod.versions[0] is None:
            raise TypeError("First mod version must be a valid ModVersion object")
        if mod.versions[0].friendly_version is None or len(mod.versions[0].friendly_version) == 0:
            raise TypeError("First mod version friendly_version cannot be empty")
        if mod.versions[0].ksp_version is None or len(mod.versions[0].ksp_version) == 0:
            raise TypeError("First mod version ksp_version cannot be empty")

        if cls.current_cookies is None or "session" not in cls.current_cookies.keys():
            raise Exception("Must log in first!")

        if not os.path.exists(file_path):
            raise IOError("File '{0}' does not exist".format(file_path))

        data = {
            'name': mod.name,
            'short-description': mod.short_description,
            'license': mod.license,
            'version': mod.versions[0].friendly_version,
            'ksp-version': mod.versions[0].ksp_version
        }

        files = {}

        with open(file_path, 'rb') as zip_file:
            if not zipfile.is_zipfile(zip_file):
                raise IOError("File at path '{0}' is not a valid zip file.".format(file_path))
            files['zipball'] = (file_name, zip_file.readall(), 'application/zip')

        cls.do_post_request(Constants.mod_create, data=data, files=files, cookies=cls.current_cookies)

        if cls.current_json is not None:
            return cls.current_json

        return None

    @classmethod
    def mod_update(cls, mod_id: int, mod_version: ModVersion, notify_followers: bool, file_name: str, file_path: str):
        if mod_version is None or not isinstance(mod_version, ModVersion):
            raise TypeError("mod_version must be a valid ModVersion object")
        if mod_version.friendly_version is None or len(mod_version.friendly_version) == 0:
            raise TypeError("mod_version.friendly_version must not be empty")
        if mod_version.ksp_version is None or len(mod_version.ksp_version) == 0:
            raise TypeError("mod_version.ksp_version must not be empty")

        if cls.current_cookies is None or "session" not in cls.current_cookies.keys():
            raise Exception("Must log in first!")

        if not os.path.exists(file_path):
            raise IOError("File '{0}' does not exist".format(file_path))

        data = {
            'version': mod_version.friendly_version,
            'ksp-version': mod_version.ksp_version,
            'notify-followers': "yes" if notify_followers else "no"
        }

        if mod_version.changelog is not None and len(mod_version.changelog) > 0:
            data['changelog'] = mod_version.changelog

        files = {}

        with open(file_path, 'rb') as zip_file:
            if not zipfile.is_zipfile(zip_file):
                raise IOError("File at path '{0}' is not a valid zip file.".format(file_path))
            files['zipball'] = (file_name, zip_file.readall(), 'application/zip')

        cls.do_post_request(Constants.mod_update, mod_id, data=data, files=file, cookies=cls.current_cookies)

        if cls.current_json is not None:
            return cls.current_json

        return None
