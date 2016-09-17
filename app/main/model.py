import collections

FoundGitHubUser = collections.namedtuple("FoundUser", ("avatar_url", "repos_url", "url", "login"))

FullGitHubUser = collections.namedtuple("FullUser", ("avatar_url", "repos_url", "url", "login", "repos"))

Repo = collections.namedtuple("Repo", ("name", "url", "html_url", "pull_requests", "is_fork"))

PullRequest = collections.namedtuple("PullRequest", ("url", "title"))


class User(object):

    users = dict()

    def __new__(cls, username, *args, **kwargs):
        obj = super().__new__(cls)
        cls.users[username] = obj
        return obj

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_anonymous = False
        self.is_authenticated = True
        self.is_active = True

    def get_id(self):
        return self.username

    @classmethod
    def get(cls, user_id):
        return cls.users[user_id]
