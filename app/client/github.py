import requests
from urllib.parse import quote_plus
import base64
import config

_github_api_url = "https://api.github.com"
_search_user_uri = _github_api_url + "/search/users"
_repo_uri = _github_api_url + "/repos"

_headers = {
    "Accept": "application/json",
    "Authorization": b"Basic " + base64.b64encode(config.username + b":" + config.password)
}


def search_for_user(user_search):
    """This does a search of github for a pa"""
    search_uri = "{}?q={}+type:user".format(_search_user_uri, quote_plus(user_search))
    response = requests.get(search_uri, headers=_headers)
    if response.status_code == 200:
        response_data = response.json()
        if response_data["total_count"] > 100:
            return {"error": "number of results greater than 100"}
        else:
            return response_data["items"]
    else:
        return {"error": "{}".format(response.status_code)}


def retrieve_repo(username, repo_name):
    """This retrieves information about a particular repo"""
    search_uri = "{}/{}/{}".format(_repo_uri, username, repo_name)
    response = requests.get(search_uri, headers=_headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "{}".format(response.json()["message"])}


def retrieve_repos(login):
    """This gets every repo that a login has"""
    search_uri = "{}/users/{}/repos".format(_github_api_url, login)
    response = requests.get(search_uri, headers=_headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "{}".format(response.json()["message"])}


def retrieve_pulls(full_repo_name, state="open"):
    search_uri = "{}/repos/{}/pulls?state={}".format(_github_api_url, full_repo_name, state)
    response = requests.get(search_uri, headers=_headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "{}".format(response.json()["message"])}
