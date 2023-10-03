import os

import pytest
from github import Auth, Github

ORGANIZATION = "ckids-datafirst"

token = os.environ.get("GITHUB_TOKEN")


@pytest.fixture
def client():
    auth = Auth.Token(token)
    return Github(auth=auth)


@pytest.fixture
def organization():
    auth = Auth.Token(token)
    client = Github(auth=auth)
    return client.get_organization(ORGANIZATION)
