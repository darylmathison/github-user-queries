import requests
from urllib.parse import quote_plus
import base64
from flask_login import current_user

_github_api_url = "https://api.github.com"
_search_user_uri = _github_api_url + "/search/users"
_repo_uri = _github_api_url + "/repos"


def search_for_user(user_search, headers=None):
    """This does a search of github for a pa"""
    search_uri = "{}?q={}+type:user".format(_search_user_uri, quote_plus(user_search))
    if headers is None:
        response = requests.get(search_uri, headers=create_headers(current_user))
    else:
        response = requests.get(search_uri, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        if response_data["total_count"] > 100:
            return {"error": "number of results greater than 100"}
        else:
            return response_data["items"]
    else:
        return {"error": "{}".format(response.status_code)}


def retrieve_repo(repo_url):
    """This retrieves information about a particular repo"""
    response = requests.get(repo_url, headers=create_headers(current_user))
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "{}".format(response.json()["message"])}


def retrieve_repos(login):
    """This gets every repo that a login has"""
    search_uri = "{}/users/{}/repos".format(_github_api_url, login)
    response = requests.get(search_uri, headers=create_headers(current_user))
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "{}".format(response.json()["message"])}


def retrieve_pulls(full_repo_name, state="open"):
    search_uri = "{}/repos/{}/pulls?state={}".format(_github_api_url, full_repo_name, state)
    response = requests.get(search_uri, headers=create_headers(current_user))
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "{}".format(response.json()["message"])}


def create_headers(user):
    return {
        "Accept": "application/json",
        "Authorization":
            b"Basic " + base64.b64encode(user.username.encode("ascii") + b":"
                                         + user.password.encode("ascii"))
    }
