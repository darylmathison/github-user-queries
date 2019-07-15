import unittest
from unittest.mock import patch
from app.main.service import GitHubUserService


@patch("app.main.service.github")
class TestGitHubUserService(unittest.TestCase):

    def setUp(self):
        self.test_user = "test"
        self.retrieved_repos_return = [
            {
                "fork": False,
                "name": "test_non_fork",
                "pull_url": "http://localhost/non_fork/pulls",
                "url": "https://localhost/non_fork",
                "full_name": self.test_user + "/test_non_fork",
                "html_url": "https://localhost"
            },
            {
                "fork": True,
                "name": "test_fork",
                "full_name": self.test_user + "/test_fork",
                "url": "https://localhost/child",
                "html_url": "https://localhost",
                "parent": {
                    "fork": False,
                    "name": "parent",
                    "url": "http://parent",
                    "full_name": self.test_user + "1/test_parent",
                    "pull_url": "https://localhost/parent/pulls",
                    "html_url": "https://localhost/parent"
                }
            }
        ]

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
        def local_mock_retrieve_pulls(url, state):
            pulls = [
                {
                    "html_url": "https://localhost/parent/pulls",
                    "title": "test title",
                    "user": {
                        "login": self.test_user
                    }
                }
            ]
            if "parent" in url:
                return pulls
            else:
                pulls[0]["html_url"] = self.retrieved_repos_return[0]["html_url"]
            return pulls
        # mocks
        github_client.retrieve_repos.return_value = self.retrieved_repos_return
        github_client.retrieve_repo.side_effect = self.mock_retrieve_repo
        github_client.retrieve_pulls.side_effect = local_mock_retrieve_pulls

        actual_repos = GitHubUserService.retrieve_repos(self.test_user)
        self.assertEqual(2, len(actual_repos))
        for repo in actual_repos:
            if repo.is_fork:
                self.assertTrue("parent" in
                                repo.pull_requests[0].url,
                                "The parent pulls are not in the repo: {}"
                                .format(repo.name))

    def test_retrieve_repos_if_fork_without_pr(self, github_client):
        def local_mock_retrieve_pulls(url, state):
            pulls = [
                {
                    "html_url": "https://localhost/parent/pulls",
                    "title": "test title",
                    "user": {
                        "login": self.test_user
                    }
                }
            ]
            if "parent" in url:
                return []
            else:
                pulls[0]["html_url"] = self.retrieved_repos_return[0]["html_url"]
            return pulls

        # mocks
        github_client.retrieve_repos.return_value = self.retrieved_repos_return
        github_client.retrieve_repo.side_effect = self.mock_retrieve_repo
        github_client.retrieve_pulls.side_effect = local_mock_retrieve_pulls

        actual_repos = GitHubUserService.retrieve_repos(self.test_user)
        for repo in actual_repos:
            if repo.is_fork:
                self.assertIsNone(repo.pull_requests,
                                  "The parent pulls are not in the repo: {}"
                                  .format(repo.name))

    def test_retrieve_repos_if_source_with_pr(self, github_client):
        def local_mock_retrieve_pulls(url, state):
            pulls = [
                {
                    "html_url": "https://localhost/non_fork/pulls",
                    "title": "test title",
                    "user": {
                        "login": self.test_user
                    }
                }
            ]
            return pulls

        # mocks
        github_client.retrieve_repos.return_value = self.retrieved_repos_return
        github_client.retrieve_repo.side_effect = self.mock_retrieve_repo
        github_client.retrieve_pulls.side_effect = local_mock_retrieve_pulls

        actual_repos = GitHubUserService.retrieve_repos(self.test_user)
        self.assertEqual(2, len(actual_repos))

        for repo in actual_repos:
            if not repo.is_fork:
                self.assertTrue("non_fork" in
                                repo.pull_requests[0].url,
                                "The non_fork pulls are not in the repo: {}"
                                .format(repo.name))

    def test_retrieve_repos_if_source_without_pr(self, github_client):
            def local_mock_retrieve_pulls(url, state):
                return []

            # mocks
            github_client.retrieve_repos.return_value = self.retrieved_repos_return
            github_client.retrieve_repo.side_effect = self.mock_retrieve_repo
            github_client.retrieve_pulls.side_effect = local_mock_retrieve_pulls

            actual_repos = GitHubUserService.retrieve_repos(self.test_user)
            self.assertEqual(2, len(actual_repos))

            for repo in actual_repos:
                if not repo.is_fork:
                    self.assertIsNone(repo.pull_requests,
                                      "The non_fork pulls are not in the repo: {}"
                                      .format(repo.name))

    # -----------------helper mock functions--------------------

    def mock_retrieve_repo(self, url):
        if "non_fork" in url:
            return self.retrieved_repos_return[0]
        elif "parent" in url:
            return self.retrieved_repos_return[1]["parent"]
        else:
            return self.retrieved_repos_return[1]

    def mock_retrieve_pulls(self, url, state):
        pulls = [
            {
                "html_url": "https://localhost/parent/pulls",
                "title": "test title",
                "user": {
                    "login": self.test_user
                }
            }
        ]
        if "parent" in url:
            return pulls
        else:
            pulls[0]["html_url"] = self.retrieved_repos_return[0]["html_url"]
        return pulls

if __name__ == '__main__':
    unittest.main()
