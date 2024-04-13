import streamlit as st

from embedder import RepoEmbedder


def main():
    st.set_page_config("Repo Amigo 2")
    st.header("Repo Amigo 2")

    github_url = st.text_input("Enter a github url")

    if github_url:
        embedder = RepoEmbedder(github_url)
        embedder.clone_repo()
        embedder.generate_vector_store()


if __name__ == "__main__":
    main()
