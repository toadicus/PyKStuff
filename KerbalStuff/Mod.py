__author__ = 'toadicus'


class Mod:
    def __init__(self, *args, **kwargs):
        self.versions = []
        """:type : list[ModVersion]"""
        self.author = None
        """:type : str"""
        self.downloads = None
        """:type : int"""
        self.default_version_id = None
        """:type : int"""
        self.followers = None
        """:type : int"""
        self.id = None
        """:type : int"""
        self.ksp_version = None
        """:type : str"""
        self.name = None
        """:type : str"""
        self.short_description = None
        """:type : str"""
        self.license = None
        """:type : str"""

        error_message = None
        try:
            self._init_from_args(*args, **kwargs)
        except TypeError as x1:
            try:
                self._init_from_dict(*args, **kwargs)
            except TypeError as x2:
                error_message = "Could not build mod object:\n\t{0}\n\t{1}".format(x1.args[0], x2.args[0])

        if error_message is not None:
            raise TypeError(error_message)

    def _init_from_dict(self, json_dict: dict):
        """
        Initalizes a new instance of the Mod class from a dict of json objects.
        :param json_dict: dict containing the deserialized json response from KerbalStuff
        """
        self.author = str(json_dict["author"])
        self.downloads = int(json_dict["downloads"])
        self.default_version_id = int(json_dict["default_version_id"])
        self.followers = int(json_dict["followers"])
        self.id = int(json_dict["id"])
        self.name = str(json_dict["name"])
        self.short_description = str(json_dict["short_description"])

        if "background" in json_dict.keys():
            self.background = json_dict["background"]
        else:
            self.background = None

        if self.background is not None and "bg_offset_y" in json_dict.keys():
                self.bg_offset_y = json_dict["bg_offset_y"]

        if "versions" in json_dict.keys() and isinstance(json_dict["versions"], list):
            for v in json_dict["versions"]:
                self.versions.append(ModVersion(v))

    def _init_from_args(self,
                        name: str,
                        short_description: str,
                        friendly_version: str,
                        ksp_version: str,
                        mod_license: str
                        ):
        """
        Initializes a Mod object from the given arguments.  Used in mod creation.
        :param name: The name of this Mod
        :param short_description: A short (1000 characters or less) description of this Mod
        :param friendly_version: The human-friendly (or not) version name or number used in creating this Mod
        :param ksp_version: The primary version of KSP for which this Mod was developed.
        :param mod_license: The name or title (128 characters or less) of thie License under which this Mod is released.
        """
        self.name = name
        self.short_description = short_description
        self.license = mod_license

        self.versions.append(ModVersion(friendly_version, ksp_version))

    def __str__(self):
        return ("Mod: {1}\n" +
                "id: {6}\n" +
                "author: {3}\n" +
                "downloads: {0}\n" +
                "followers: {2}\n" +
                "short_description: {7}\n" +
                "default_version_id: {4}\n" +
                "versions:\n[\n{5}\n]").format(
                    self.downloads,
                    self.name,
                    self.followers,
                    self.author,
                    self.default_version_id,
                    "\n".join([str(v) for v in self.versions]),
                    self.id,
                    self.short_description)


class ModVersion:
    def __init__(self, *args, **kwargs):
        self.changelog = None
        """:type : string"""
        self.download_path = None
        """:type : string"""
        self.friendly_version = None
        """:type : string"""
        self.id = None
        """:type : int"""
        self.ksp_version = None
        """:type : string"""

        error_message = None
        try:
            self._init_from_args(*args, **kwargs)
        except TypeError as x1:
            try:
                self._init_from_dict(*args, **kwargs)
            except TypeError as x2:
                error_message = "Could not build mod object:\n\t{0}\n\t{1}".format(x1.args[0], x2.args[0])

        if error_message is not None:
            raise TypeError(error_message)

    def _init_from_dict(self, json_dict: dict):
        """
        Initalizes a new instance of the ModVersion class from a dict of json objects.
        :param json_dict: dict containing the deserialized json response from KerbalStuff
        """
        self.changelog = json_dict["changelog"]
        self.download_path = json_dict["download_path"]
        self.id = json_dict["id"]
        self.ksp_version = json_dict["ksp_version"]
        self.friendly_version = json_dict["friendly_version"]

    def _init_from_args(self, friendly_version: str, ksp_version: str, changelog: str=None):
        """

        :param friendly_version: The human-friendly (or not) version name or number used in creating this ModVersion
        :param ksp_version: The primary version of KSP for which this ModVersion was developed.
        :param changelog: An optional log describing the changes made in this ModVersion
        """
        self.friendly_version = friendly_version
        self.ksp_version = ksp_version
        self.changelog = changelog

    def __str__(self):
        return "Version {0}\n\tid: {1}\n\tksp_version: {2}\n\tdownload_path: {3}\n\tchangelog: {4}".format(
            self.friendly_version, self.id, self.ksp_version, self.download_path, self.changelog)