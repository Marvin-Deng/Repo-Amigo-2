import streamlit as st

# Load settings from secrets
DEV_MODE = st.secrets["DEV_MODE"] == "True"
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
BASE_URI = "http://localhost:8501" if DEV_MODE else "https://repo-amigo-2.streamlit.app"
CLIENT_ID = (
    st.secrets["GITHUB_CLIENT_ID_DEV"] if DEV_MODE else st.secrets["GITHUB_CLIENT_ID"]
)
CLIENT_SECRET = (
    st.secrets["GITHUB_CLIENT_SECRET_DEV"]
    if DEV_MODE
    else st.secrets["GITHUB_CLIENT_SECRET"]
)
REDIRECT_URI = f"{BASE_URI}/callback"
PEM_PATH=st.secrets["PEM_PATH"]

# GitHub URLs
GITHUB_AUTHORIZATION_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"
GITHUB_INSTALLATION_URL = "https://api.github.com/installation/repositories"

