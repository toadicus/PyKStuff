__author__ = 'toadicus'

import requests
import sys
from .Constants import Constants
from .Mod import Mod, ModVersion
from .User import User
from StaticClass import staticclass

Constants.RootUri = "https://kerbalstuff.com"
Constants.ApiUri = Constants.RootUri + "/api"
Constants.UserAgent = "PyKStuff by toadicus"

Constants.browse_new = Constants.format_action("/browse/new?page={0:d}")
Constants.browse_featured = Constants.format_action("/browse/featured?page={0:d}")
Constants.browse_top = Constants.format_action("/browse/top?page={0:d}")

Constants.mod_info = Constants.format_action("/mod/{0:d}")
Constants.mod_latest = Constants.format_action("/mod/{0:d}/latest")

Constants.search_mod = Constants.format_action("/search/mod?query={0}&page={1:d}")
Constants.search_user = Constants.format_action("/search/user?query={0}&page={1:d}")

Constants.user_info = Constants.format_action("/user/{0}")

if Constants.headers is None:
    Constants.headers = {}
Constants.headers["User-Agent"] = "PyKStuff by toadicus"


@staticclass
class KerbalStuffReadOnly:
    current_response = None
    """:type : requests.Response"""
    current_json = None
    """:type : dict[str, object]"""

    @classmethod
    def do_get_request(cls, uri: str, *format_args):
        cls.current_response = None
        cls.current_json = None

        if len(format_args) > 0:
            uri = uri.format(*format_args)

        cls.current_response = requests.get(uri, headers=Constants.headers)

        if cls.current_response.status_code >= 400:
            sys.stderr.write("Failed connecting to KerbalStuff with status code {0}: {1}".format(
                cls.current_response.status_code, cls.current_response.reason))
            sys.exit(cls.current_response.status_code)

        try:
            cls.current_json = cls.current_response.json()
        except ValueError:
            sys.stderr.write("Response received was not valid JSON\n")
            sys.exit(1)

    @classmethod
    def browse_featured(cls, page_id: int=1) -> list:
        cls.do_get_request(Constants.browse_featured, page_id)

        mods = []
        """:type : list of [Mod]"""

        if cls.current_json is not None and isinstance(cls.current_json, list):
            for m in cls.current_json:
                mods.append(Mod(m))

        return mods

    @classmethod
    def browse_new(cls, page_id: int=1):
        cls.do_get_request(Constants.browse_new, page_id)

        mods = []
        """:type : list of [Mod]"""

        if cls.current_json is not None and isinstance(cls.current_json, list):
            for m in cls.current_json:
                mods.append(Mod(m))

        return mods

    @classmethod
    def browse_top(cls, page_id: int=1):
        cls.do_get_request(Constants.browse_top, page_id)

        mods = []
        """:type : list of [Mod]"""

        if cls.current_json is not None and isinstance(cls.current_json, list):
            for m in cls.current_json:
                mods.append(Mod(m))

        return mods

    @classmethod
    def mod_info(cls, mod_id: int) -> Mod:
        cls.do_get_request(Constants.mod_info, mod_id)

        if cls.current_json is not None:
            return Mod(cls.current_json)
        return None

    @classmethod
    def mod_latest(cls, mod_id: int) -> ModVersion:
        cls.do_get_request(Constants.mod_latest, mod_id)

        if cls.current_json is not None:
            return ModVersion(cls.current_json)
        return None

    @classmethod
    def search_mod(cls, query: str, page_id: int=1):
        cls.do_get_request(Constants.search_mod, query, page_id)

        mods = []
        """:type : list of [Mod]"""

        if cls.current_json is not None and isinstance(cls.current_json, list):
            for m in cls.current_json:
                mods.append(Mod(m))

        return mods

    @classmethod
    def search_user(cls, query: str, page_id: int=0):
        cls.do_get_request(Constants.search_user, query, page_id)

        users = []

        if cls.current_json is not None and isinstance(cls.current_json, list):
            for u in cls.current_json:
                users.append(User(u))
        return users

    @classmethod
    def user_info(cls, username: str):
        cls.do_get_request(Constants.user_info, username)

        if cls.current_json is not None and isinstance(cls.current_json, dict):
            return User(cls.current_json)
        return None
