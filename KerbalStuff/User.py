__author__ = 'toadicus'

from .Mod import Mod


class User:
    def __init__(self, json_dict: dict):
        self.description = json_dict["description"]
        """:type : str"""
        self.forum_username = json_dict["forumUsername"]
        """:type : str"""
        self.irc_nick = json_dict["ircNick"]
        """:type : str"""
        self.mods = []
        """:type : list[Mod]"""
        for m in json_dict["mods"]:
            self.mods.append(Mod(m))

        self.username = json_dict["username"]
        """:type : str"""
        self.reddit_username = json_dict["redditUsername"]
        """:type : str"""
        self.twitter_username = json_dict["twitterUsername"]
        """:type : str"""

    def __str__(self):
        return "User: username={0}," \
               "twitterUsername={1}," \
               "redditUsername={3}," \
               "ircNick={4}," \
               "description={5}," \
               "forumUsername={6}" \
               "\nmods:\n{2}".format(
                                self.username,
                                self.twitter_username,
                                "\n".join([str(m) for m in self.mods]),
                                self.reddit_username,
                                self.irc_nick,
                                self.description,
                                self.forum_username)