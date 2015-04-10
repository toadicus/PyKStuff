__author__ = 'toadicus'

__all__ = ["Constants"]

from Namespace import Namespace


class _Constants(Namespace):
    def __init__(self):
        if self._initialized:
            return
        super().__init__()

    def format_action(self, uri_path_fmt):
        return "{0}{1}".format(self.ApiUri, uri_path_fmt)

Constants = _Constants()