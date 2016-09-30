import unittest
from unittest.mock import patch
from app.main.service import GitHubUserService
from app.main.model import FoundGitHubUser


@patch("app.main.service.github")
class TestGitHubUserService(unittest.TestCase):
    def test_search_for_users_error(self, github_client):
        message = "too many"
        github_client.search_for_user.return_value = {"error": message}
        assert GitHubUserService.search_for_user("nobody") == message

    def test_search_for_users_success(self, github_client):
        github_client_return = [{
            "avatar_url": "test",
            "repos_url": "http://localhost",
            "html_url": "https://localhost",
            "login": "nobody"
        }]
        github_client.search_for_user.return_value = github_client_return
        found_users = GitHubUserService.search_for_users("nobody")
        self.assertEqual(found_users[0].avatar_url, github_client_return[0]["avatar_url"])
        self.assertEqual(found_users[0].repos_url, github_client_return[0]["repos_url"])
        self.assertEqual(found_users[0].url, github_client_return[0]["html_url"])
        self.assertEqual(found_users[0].login, github_client_return[0]["login"])

    def test_retrieve_repos_if_fork_with_pr(self, github_client):
        test_user = "test_user"
        retrieved_repos_return = [
            {
                "fork": False,
                "name": "test_non_fork",
                "pull_url": "http://localhost/non_fork/pulls",
                "url": "https://localhost/non_fork",
                "full_name": test_user + "/test_non_fork",
                "html_url": "https://localhost"
            },
            {
                "fork": True,
                "name": "test_fork",
                "full_name": test_user + "/test_fork",
                "url": "https://localhost/child",
                "html_url": "https://localhost",
                "parent": {
                    "fork": False,
                    "name": "parent",
                    "url": "http://parent",
                    "full_name": test_user + "1/test_parent",
                    "pull_url": "https://localhost/parent/pulls",
                    "html_url": "https://localhost/parent"
                }
            }
        ]

        def mock_retrieve_repo(url):
            if "non_fork" in url:
                return retrieved_repos_return[0]
            elif "parent" in url:
                return retrieved_repos_return[1]["parent"]
            else:
                return retrieved_repos_return[1]

        def mock_retrieve_pulls(url, state):
            pulls = [
                {
                    "html_url": "https://localhost/parent/pulls",
                    "title": "test title",
                    "user": {
                        "login": test_user
                    }
                }
            ]
            if "parent" in url:
                return pulls
            else:
                pulls[0]["html_url"] = retrieved_repos_return[0]["html_url"]
            return pulls
        # mocks
        github_client.retrieve_repos.return_value = retrieved_repos_return
        github_client.retrieve_repo.side_effect = mock_retrieve_repo
        github_client.retrieve_pulls.side_effect = mock_retrieve_pulls

        actual_repos = GitHubUserService.retrieve_repos(test_user)
        self.assertEqual(2, len(actual_repos))
        for repo in actual_repos:
            if repo.is_fork:
                self.assertTrue("parent" in
                                repo.pull_requests[0].url,
                                "The parent pulls are not in the repo: {}"
                                .format(repo.name))

if __name__ == '__main__':
    unittest.main()
