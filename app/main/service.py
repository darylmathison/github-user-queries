from ..client import github


class GithubUserService(object):
    @staticmethod
    def search_for_user(name):
        results = github.search_for_user(name)
        if isinstance(results, dict) and "error" in results:
            return results["error"]
        else:
            return results