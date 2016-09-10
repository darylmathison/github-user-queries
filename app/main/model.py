import collections

FoundUser = collections.namedtuple("FoundUser", ("avatar_url", "repos_url", "url", "login"))

FullUser = collections.namedtuple("FullUser", ("avatar_url", "repos_url", "url", "login", "repos"))

Repo = collections.namedtuple("Repo", ("name", "url", "html_url", "pull_requests", "is_fork"))

PullRequest = collections.namedtuple("PullRequest", ("url", "title"))
