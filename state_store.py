import streamlit as st
from enum import Enum
import copy
import streamlit as st

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]


class State(Enum):
    CURR_REPO_URL = "repo_url"
    CURR_REPO_NAME = "repo_name"
    CURR_REPO_OWNER = "repo_owner"


STATE_DEFAULTS = {
    State.CURR_REPO_URL: "",
    State.CURR_REPO_NAME: "",
    State.CURR_REPO_OWNER: "",
}


def init_states():
    if st.session_state:
        return
    for key, default in STATE_DEFAULTS.items():
        set_state(key, copy.deepcopy(default))


def set_state(key, value):
    st.session_state[key] = value


def get_state(key):
    return st.session_state[key]
