import os
import shutil
import streamlit as st
from urllib.parse import urlparse
from repo_chain.embedder import RepoEmbedder
from repo_chain.chain import RepoChain
from state_store import (
    State,
    init_states,
    set_state,
    get_state,
)


def main():
    init_states()

    st.set_page_config("Repo Amigo 2")
    st.header("Repo Amigo 2")

    github_url = st.text_input("Enter a public github url")
    reset_button = st.button("Reset")

    if github_url and github_url != get_state(State.CURR_REPO_URL):
        url_components = urlparse(github_url).path.split("/")
        repo_owner = url_components[1]
        repo_name = url_components[2]
        set_state(State.CURR_REPO_URL, github_url)
        set_state(State.CURR_REPO_NAME, repo_name)
        set_state(State.CURR_REPO_OWNER, repo_owner)

    if reset_button:
        github_url = ""
        index_path = f"./store/{get_state(State.CURR_REPO_NAME)}"
        if os.path.exists(index_path):
            shutil.rmtree(index_path)

    if github_url:
        with st.spinner("Loading..."):
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
                st.write(repo_chain.get_response(question))


if __name__ == "__main__":
    main()
