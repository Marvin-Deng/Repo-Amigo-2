import os
import sys
import shutil
import streamlit as st
from urllib.parse import urlparse
from repo_chain.embedder import RepoEmbedder
from repo_chain.chain import RepoChain

from components.oauth import oauth_button
from state_store import (
    State,
    init_states,
    set_state,
    get_state,
)

init_states()

def main():
    

    st.set_page_config("Repo Amigo 2")
    st.header("Repo Amigo 2")

    oauth_button()

    github_url = st.text_input("Enter a public github url")
    reset_button = st.button("Reset")

    if reset_button:
        index_path = f"./store/{get_state(State.CURR_REPO_OWNER)}-{get_state(State.CURR_REPO_NAME)}"
        if os.path.exists(index_path):
            init_states()
            shutil.rmtree(index_path)

    if github_url:
        question = ""
        url_components = urlparse(github_url).path.split("/")
        set_state(State.CURR_REPO_URL, github_url)
        set_state(State.CURR_REPO_NAME, url_components[2])
        set_state(State.CURR_REPO_OWNER, url_components[1])

        with st.spinner("Loading"):
            embedder = RepoEmbedder(
                github_url=get_state(State.CURR_REPO_URL),
                repo_owner=get_state(State.CURR_REPO_OWNER),
                repo_name=get_state(State.CURR_REPO_NAME),
            )
            embedder.clone_repo()
            embedder.generate_vector_store()

            repo_chain = RepoChain(embedder.index_path)
            repo_chain.generate_conversational_chain()

            st.success(f"{embedder.repo_name} has been loaded!")

        question = st.text_input("Ask a question about this repo!", key="question")
        if question:
            with st.spinner("Answering question..."):
                st.write(
                    repo_chain.get_response(
                        repo_name=get_state(State.CURR_REPO_NAME),
                        repo_owner=get_state(State.CURR_REPO_OWNER),
                        github_url=get_state(State.CURR_REPO_URL),
                        user_question=question,
                    )
                )


if __name__ == "__main__":
    main()
