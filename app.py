import streamlit as st
from urllib.parse import urlparse
from repo_chain.embedder import RepoEmbedder
from repo_chain.chain import RepoChain

from state_store import CURR_GITHUB_REPO


def main():
    global CURR_GITHUB_REPO

    st.set_page_config("Repo Amigo 2")
    st.header("Repo Amigo 2")

    github_url = st.text_input("Enter a public github url")
    if github_url and CURR_GITHUB_REPO != github_url:
        repo_name = urlparse(github_url).path.split("/")[1]

    if github_url:
        with st.spinner("Loading..."):
            embedder = RepoEmbedder(github_url, repo_name)
            embedder.clone_repo()
            embedder.generate_vector_store()

            repo_chain = RepoChain(embedder.index_path)
            repo_chain.generate_conversational_chain()

            st.success(f"{embedder.repo_name} has been loaded!")
            CURR_GITHUB_REPO = github_url

        question = st.text_input("Ask a question about this repo!", key="question")
        if question:
            with st.spinner("Answering question..."):
                st.write(repo_chain.get_response(question))


if __name__ == "__main__":
    main()
