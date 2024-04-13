from git import Repo
from langchain.text_splitter import RecursiveCharacterTextSplitter


def clone_repo(github_url: str, repo_path: str, token=None) -> bool:
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


def get_text_chunks(text: str) -> list:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks
