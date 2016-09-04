import requests
import collections
from urllib.parse import quote_plus

_github_api_url = "https://api.github.com"
_search_user_uri = _github_api_url + "/search/users"
_headers = {
    "Accept": "application/json",
}

FoundUser = collections.namedtuple("FoundUser", ("avatar_url", "repos_url", "url", "login"))

def search_for_user(username):
    search_uri = "{}?q={}+type:user".format(_search_user_uri, quote_plus(username))
    response = requests.get(search_uri, headers=_headers)
    if response.status_code == 200:
        response_data = response.json()
        if response_data["total_count"] > 100:
            return {"error": "number of results greater than 100"}
        else:
            results = response_data["items"]
            ret = []
            for result in results:
                ret.append(from_result_to_user(result))
            return ret
    else:
        return {"error": "{}".format(response.status_code)}


def from_result_to_user(result):
    return FoundUser(result["avatar_url"], result["repos_url"], result["html_url"], result["login"])