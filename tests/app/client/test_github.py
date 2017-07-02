import unittest
from unittest.mock import patch


@patch("app.client.github.requests")
class TestGithubClient(unittest.TestCase):

    def test_search_for_user_successful(self, mock_requests):
        pass

if __name__ == '__main__':
    unittest.main()
