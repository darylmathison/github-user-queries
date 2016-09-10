from ..client import github
from .model import FoundUser
from .model import Repo
from .model import FullUser
from .model import PullRequest
from time import sleep


class GitHubUserService(object):
    @staticmethod
    def search_for_users(name):
        results = github.search_for_user(name)
        if isinstance(results, dict) and "error" in results:
            return results["error"]
        else:
            users = []
            for user in results:
                user = FoundUser(user["avatar_url"],
                                 user["repos_url"],
                                 user["html_url"],
                                 user["login"])
                users.append(user)
            return users

    @staticmethod
    def search_for_user(username):
        """This fills in the repos and relevant pull requests for a user"""
        results = github.search_for_user(username)
        if isinstance(results, dict) and "error" in results:
            return results["error"]
        else:
            user = results[0]
            full_user = FullUser(
                user["avatar_url"],
                user["repos_url"],
                user["html_url"],
                user["login"],
                GitHubUserService.retrieve_repos(user["login"])
            )
            return full_user

    @staticmethod
    def retrieve_repos(username):
        repos = github.retrieve_repos(username)
        if isinstance(repos, dict) and "error" in repos:
            return repos["error"]
        ret = []
        for repo in repos:
            github_repo = github.retrieve_repo(username, repo["name"])
            if "error" in github_repo:
                return github_repo["error"]
            pulls = [PullRequest(p["html_url"], p["title"]) for p in
                     github.retrieve_pulls(github_repo["full_name"], state="all")
                     ]

            if pulls:
                ret.append(Repo(repo["name"], repo["url"], repo["html_url"], pulls, True))
            else:
                ret.append(Repo(repo["name"], repo["url"], repo["html_url"], None, True))

        return ret
