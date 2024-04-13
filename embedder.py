import os
import shutil
from git import Repo
from urllib.parse import urlparse
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader


class RepoEmbedder:
    def __init__(self, github_url: str, github_token=None):
        self.github_url = github_url
        self.repo_name = self.get_repo_name()
        self.repo_path = f"./repo/{self.repo_name}"
        self.token = github_token

        self.clone_repo()
        self.recursively_parse_repo_files()

    def get_repo_name(self) -> str:
        parsed_url = urlparse(self.github_url)
        path_components = parsed_url.path.strip("/").split("/")
        return path_components[-1] if path_components else None

    def clone_repo(self):
        if os.path.exists(self.repo_path):
            return
        try:
            if self.token:
                formatted_url = (
                    f"https://{self.token}@{self.github_url.split('https://')[1]}"
                )
            else:
                formatted_url = self.github_url
            Repo.clone_from(formatted_url, self.repo_path)
        except Exception as e:
            print(f"Failed to clone repository: {e}")

    def recursively_parse_repo_files(self) -> list:
        document_chunks = []
        for curr, _, files in os.walk(self.repo_path):
            for file_name in files:
                file_path = os.path.join(curr, file_name)
                try:
                    loader = TextLoader(file_path, encoding="utf-8")
                    chunks = loader.load_and_split(
                        text_splitter=RecursiveCharacterTextSplitter(chunk_size=250)
                    )
                    document_chunks.extend(chunks)
                except Exception as e:
                    pass
                    # print(f"Failed to load file: {file_name} with error {e}")
        shutil.rmtree("./repo")
        return document_chunks
