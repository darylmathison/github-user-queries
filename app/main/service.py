import base64

from .model import FoundGitHubUser
from .model import FullGitHubUser
from .model import PullRequest
from .model import Repo
from ..client import github


class GitHubUserService(object):
    @staticmethod
    def search_for_users(name):
        results = github.search_for_user(name)
        if isinstance(results, dict) and "error" in results:
            return results["error"]
        else:
            users = []
            for user in results:
                user = FoundGitHubUser(user["avatar_url"],
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
            full_user = FullGitHubUser(
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
            if repo["fork"]:
                github_repo = github.retrieve_repo(repo["url"])
                if "error" in github_repo:
                    return github_repo["error"]
                else:
                    # get the parent repo since children don't have PRs
                    github_repo = github.retrieve_repo(
                        github_repo["parent"]["url"]
                    )
            else:
                github_repo = github.retrieve_repo(repo["url"])
                if "error" in github_repo:
                    return github_repo["error"]

            pulls = [PullRequest(p["html_url"], p["title"]) for p in
                     github.retrieve_pulls(github_repo["full_name"],
                                           state="all")
                     if p["user"]["login"] == username]

            if pulls:
                ret.append(Repo(repo["name"], repo["url"], repo["html_url"],
                                pulls, repo["fork"]))
            else:
                ret.append(Repo(repo["name"], repo["url"], repo["html_url"],
                                None, repo["fork"]))

        return ret

    @staticmethod
    def validate_user(username, password):
        headers = {
            "Accept": "application/json",
            "Authorization": b"Basic " + base64.b64encode(
                username.encode("ascii") + b":" + password.encode("ascii")
            )
        }
        response = github.search_for_user(username, headers=headers)
        if "error" in response:
            return False
        else:
            return True
