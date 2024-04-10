from git import Repo
import os


def clone_repo(github_url: str, repo_path: str, token=None):
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
