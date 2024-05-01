import streamlit as st
from enum import Enum
import copy
from urllib.parse import urlparse


class AuthState(Enum):
    USERNAME = "username"
    ACCESS_TOKEN = "access_token"


class RepoState(Enum):
    CURR_REPO_URL = "repo_url"
    CURR_REPO_NAME = "repo_name"
    CURR_REPO_OWNER = "repo_owner"


AUTH_DEFUALTS = {
    AuthState.USERNAME: "",
    AuthState.ACCESS_TOKEN: "",
}

REPO_DEFAULTS = {
    RepoState.CURR_REPO_URL: "",
    RepoState.CURR_REPO_NAME: "",
    RepoState.CURR_REPO_OWNER: "",
}


def is_default_state(key: str) -> bool:
    if key not in st.session_state:
        return True
    val = st.session_state[key]
    return val == AUTH_DEFUALTS.get(key, None) or val == REPO_DEFAULTS.get(key, None)


def init_auth_states() -> None:
    for key, default in AUTH_DEFUALTS.items():
        set_state(key, copy.deepcopy(default))


def init_repo_states() -> None:
    for key, default in REPO_DEFAULTS.items():
        set_state(key, copy.deepcopy(default))


def set_repo_states(github_url: str) -> None:
    if github_url:
        url_components = urlparse(github_url).path.split("/")
        set_state(RepoState.CURR_REPO_URL, github_url)
        set_state(RepoState.CURR_REPO_NAME, url_components[2])
        set_state(RepoState.CURR_REPO_OWNER, url_components[1])


def set_state(key: str, value) -> None:
    st.session_state[key] = value


def get_state(key: str):
    if key not in st.session_state:
        return None
    return st.session_state[key]


init_auth_states()
init_repo_states()
