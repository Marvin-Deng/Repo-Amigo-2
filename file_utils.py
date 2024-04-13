import os
from git import Repo
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader


def clone_repo(github_url: str, repo_path: str, token=None) -> bool:
    if os.path.exists(repo_path):
        return True
    try:
        if token:
            formatted_url = f"https://{token}@{github_url.split('https://')[1]}"
        else:
            formatted_url = github_url

        Repo.clone_from(formatted_url, repo_path)
        return True

    except Exception as e:
        print(f"Failed to clone repository: {e}")
        return False


def recursively_parse_repo_files(repo_path: str) -> str:
    document_chunks = []

    for curr, _, files in os.walk(repo_path):
        for file_name in files:
            file_path = os.path.join(curr, file_name)
            try:
                loader = TextLoader(file_path, encoding="utf-8")
                chunks = loader.load_and_split(
                    text_splitter=RecursiveCharacterTextSplitter(chunk_size=250)
                )
                document_chunks.extend(chunks)
            except Exception as e:
                print(f"Failed to load file: {file_name} with error {e}")

    return document_chunks
