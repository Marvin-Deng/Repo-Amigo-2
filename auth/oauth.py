import requests
import streamlit as st
from streamlit_oauth import OAuth2Component

from constants import (
    BASE_URI,
    CLIENT_ID,
    CLIENT_SECRET,
    GITHUB_AUTHORIZATION_URL,
    GITHUB_TOKEN_URL,
    GITHUB_USER_URL,
    GITHUB_REPOS_URL,
    GITHUB_ICON,
)
from state_store import (
    AuthState,
    is_default_state,
    init_auth_states,
    set_state,
    get_state,
)


def oauth_button() -> None:
    if is_default_state(AuthState.ACCESS_TOKEN):
        oauth2 = OAuth2Component(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            authorize_endpoint=GITHUB_AUTHORIZATION_URL,
            token_endpoint=GITHUB_TOKEN_URL,
            refresh_token_endpoint="",
            revoke_token_endpoint="",
        )
        res = oauth2.authorize_button(
            name="Login with GitHub",
            redirect_uri=BASE_URI,
            icon=GITHUB_ICON,
            scope="repo",
        )
        if res and "token" in res and "access_token" in res["token"]:
            token = res["token"]["access_token"]
            set_state(AuthState.ACCESS_TOKEN, token)
            __fetch_and_store_username(token)
            st.rerun()
    else:
        st.write("You are logged in!")
        if st.button("Logout"):
            init_auth_states()
            st.rerun()


def __fetch_and_store_username(access_token: str) -> None:
    """
    Fetches the GitHub user's username using the provided OAuth access token and stores it in the session state.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(GITHUB_USER_URL, headers=headers)

    if response.status_code == 200:
        username = response.json().get("login")

        if username:
            set_state(AuthState.USERNAME, username)
        else:
            st.error("Username not found in GitHub response.")
    else:
        st.error(f"Failed to fetch user data from GitHub: {response.status_code}")


def get_user_repos(username: str) -> list:
    """
    Retrieves a list of public and private repository names for a GitHub user.
    """
    access_token = get_state(AuthState.ACCESS_TOKEN)
    api_url = f"{GITHUB_REPOS_URL}{username}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(api_url, headers=headers)
    return [
        (repo["name"], repo["html_url"]) for repo in response.json().get("items", [])
    ]
