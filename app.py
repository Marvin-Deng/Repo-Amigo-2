import os
import shutil
import streamlit as st

from repo_chain.embedder import RepoEmbedder
from repo_chain.chain import RepoChain
from auth.oauth import oauth_button, get_user_repos
from utils.utils import is_valid_github_url
from state.state_store import (
    RepoState,
    AuthState,
    is_default_state,
    init_repo_states,
    set_repo_states,
    get_state,
)


def main():

    st.set_page_config("Repo Amigo 2")
    st.header("Repo Amigo 2")

    # GITHUB OAUTH BUTTON
    oauth_button()

    # REPOSITORY DROPDOWN
    if not is_default_state(AuthState.ACCESS_TOKEN):
        token = get_state(AuthState.ACCESS_TOKEN)
        repo_info = get_user_repos("Marvin-Deng")
        if repo_info:
            repo_options = [("", None)] + [(name, url) for name, url in repo_info]
            st.markdown(
                """
                    <style>
                        .stSelectbox .css-2b097c-container:hover {
                            cursor: pointer;
                        }
                    </style>
                """,
                unsafe_allow_html=True,
            )
            selected_repo = st.selectbox(
                "Select a repository form the dropdown:",
                options=repo_options,
                format_func=lambda x: x[0] if x != "None" else "None",
            )

            # SELECT REPO BUTTON
            if selected_repo[1] != None:
                if st.button("Select Repository"):
                    github_url = selected_repo[1]
                    set_repo_states(github_url)
        else:
            st.write("No repositories found or unable to retrieve repositories.")

    # GITHUB URL INPUT
    github_url = st.text_input(
        "Enter a public github url or a private repo if logged in"
    )
    if is_valid_github_url(github_url):
        set_repo_states(github_url)
    else:
        st.error("Please enter a valid github url.")

    # SELECTED REPO TEXT
    st.write(f"Selected repository: {get_state(RepoState.CURR_REPO_NAME)}")

    # CLEAR REPO STATE BUTTON
    if st.button("Clear Repository"):
        index_path = f"./store/{get_state(RepoState.CURR_REPO_OWNER)}-{get_state(RepoState.CURR_REPO_NAME)}"
        if os.path.exists(index_path):
            shutil.rmtree(index_path)
        init_repo_states()

    # GEMINI RESPONSE
    if get_state(RepoState.CURR_REPO_URL):
        with st.spinner("Loading"):
            token = get_state(AuthState.ACCESS_TOKEN)
            embedder = RepoEmbedder(
                repo_owner=get_state(RepoState.CURR_REPO_OWNER),
                repo_name=get_state(RepoState.CURR_REPO_NAME),
                github_url=get_state(RepoState.CURR_REPO_URL),
                github_token=token,
            )
            try:
                embedder.clone_repo()
                embedder.generate_vector_store()

                repo_chain = RepoChain(embedder.index_path)
                repo_chain.generate_conversational_chain()

                st.success(f"{embedder.repo_name} has been loaded!")

            except:
                init_repo_states()
                st.error("Error cloning repo. Please enter a valid github url.")

        # QUESTION INPUT
        if get_state(RepoState.CURR_REPO_URL):
            question = st.text_input("Ask a question about this repo!", key="question")
            if question:
                with st.spinner("Answering question..."):
                    st.write(
                        repo_chain.get_response(
                            repo_owner=get_state(RepoState.CURR_REPO_OWNER),
                            repo_name=get_state(RepoState.CURR_REPO_NAME),
                            github_url=get_state(RepoState.CURR_REPO_URL),
                            user_question=question,
                        )
                    )


if __name__ == "__main__":
    main()
