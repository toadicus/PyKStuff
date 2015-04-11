__author__ = 'toadicus'


class Namespace():
    _instance = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            obj = super(Namespace, cls).__new__(*args, **kwargs)
            obj._config = {}
            obj._allow_reassignment = True
            obj._initialized = False
            cls._instance = obj
        return cls._instance

    def __init__(self, allow_reassignment=True):
        if self._initialized:
            return
        self._initialized = True
        self._allow_reassignment = allow_reassignment

    def __getattr__(self, key):
        if isinstance(key, str) and key[0] == "_":
            return object.__getattribute__(self, key)
        try:
            return self._config[key]
        except KeyError:
            return None

    def __setattr__(self, key, value):
        if isinstance(key, str) and key[0] == "_":
            object.__setattr__(self, key, value)
            return
        if not self._allow_reassignment and key in self._config.keys():
            raise TypeError("Attempted to reassign Namespace member {0}, but reassignment is not allowed.".format(key))
        self._config[key] = value

    def __contains__(self, key):
        return key in self._config.keys()