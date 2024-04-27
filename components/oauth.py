import streamlit as st
from streamlit_oauth import OAuth2Component

from constants import (
    CLIENT_ID,
    CLIENT_SECRET,
    GITHUB_AUTHORIZATION_URL,
    GITHUB_TOKEN_URL,
    REDIRECT_URI,
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
