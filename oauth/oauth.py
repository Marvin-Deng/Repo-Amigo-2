import requests
import streamlit as st
from streamlit_oauth import OAuth2Component

from constants import (
    CLIENT_ID,
    CLIENT_SECRET,
    GITHUB_AUTHORIZATION_URL,
    GITHUB_TOKEN_URL,
    REDIRECT_URI,
    GITHUB_INSTALLATION_URL,
    JWT_TOKEN,
)


def oauth_button():
    if "token" not in st.session_state:
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
            redirect_uri=REDIRECT_URI,
            icon="https://icons.iconarchive.com/icons/simpleicons-team/simple/72/github-icon.png",
            scope="",
        )

        if res and "token" in res and "access_token" in res["token"]:
            st.session_state["token"] = res["token"]["access_token"]
            st.rerun()
    else:
        st.write("You are logged in!")
        if st.button("Logout"):
            del st.session_state["token"]
            st.rerun()


def get_installation_id(username):
    url = f"https://api.github.com/users/{username}/installation"
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve installation ID: {response.status_code}")
        return None


def get_user_repo_list(token):

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.get(GITHUB_INSTALLATION_URL, headers=headers)

    if response.status_code == 200:
        repositories = response.json()
        for repo in repositories:
            st.write(repo["name"])
    else:
        print("Failed to retrieve repositories")
        print("Status Code:", response.status_code)
        print("Response:", response.text)

print(get_installation_id("Marvin-Deng"))