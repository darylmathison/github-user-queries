import collections

FoundGitHubUser = collections.namedtuple("FoundUser", ("avatar_url", "repos_url", "url", "login"))

FullGitHubUser = collections.namedtuple("FullUser", ("avatar_url", "repos_url", "url", "login", "repos"))

Repo = collections.namedtuple("Repo", ("name", "url", "html_url", "pull_requests", "is_fork"))

PullRequest = collections.namedtuple("PullRequest", ("url", "title"))


class User:

    class Factory:
        users = dict()

        @classmethod
        def get(cls, user_id):
            try:
                return cls.users[user_id]
            except KeyError as ke:
                return None

        @classmethod
        def create(cls, username, password):
            user = User(username, password)
            cls.users[user.get_id()] = user
            return user

    keeper = Factory()

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_anonymous = False
        self.is_authenticated = True
        self.is_active = True

    def get_id(self):
        return self.username


