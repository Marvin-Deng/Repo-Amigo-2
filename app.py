import streamlit as st
from urllib.parse import urlparse
from embedder import RepoEmbedder
from chain import RepoChain


def main():
    repo_chain = None
    st.set_page_config("Repo Amigo 2")
    st.header("Repo Amigo 2")

    github_url = st.text_input("Enter a public github url")
    if github_url:
        repo_name = urlparse(github_url).path.split("/")[1]

    if github_url:
        with st.spinner("Loading..."):
            embedder = RepoEmbedder(github_url, repo_name)
            embedder.clone_repo()
            embedder.generate_vector_store()

        st.success(f"{embedder.repo_name} has been loaded!")

        if repo_chain is None or embedder.index_path != repo_chain.index_path:
            repo_chain = RepoChain(embedder.index_path)
            repo_chain.generate_conversational_chain()

        if repo_chain:
            question = st.text_input("Ask a question about this repo!", key="question")
            if question:
                response = repo_chain.get_response(question)
                st.write(response)


if __name__ == "__main__":
    main()
