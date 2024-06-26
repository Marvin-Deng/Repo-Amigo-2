import os
import re
import shutil
from git import Repo
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from state.constants import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)


class RepoEmbedder:
    def __init__(
        self, repo_owner: str, repo_name: str, github_url: str, github_token=None
    ):
        self.github_url = github_url
        self.repo_name = repo_name
        self.repo_path = f"./repo/{repo_owner}-{repo_name}"
        self.index_path = f"./store/{repo_owner}-{repo_name}"
        self.token = github_token

    def clone_repo(self):
        if os.path.exists(self.repo_path) or os.path.exists(self.index_path):
            return
        if self.token:
            componenets = re.split(r"(github\.com)", self.github_url)
            formatted_url = (
                f"{componenets[0]}{self.token}@{componenets[1]}{componenets[2]}.git"
            )
        else:
            formatted_url = self.github_url
        Repo.clone_from(formatted_url, self.repo_path)
        

    def recursively_parse_repo_files(self) -> list:
        doc_chunks = []
        for curr, _, files in os.walk(self.repo_path):
            for file_name in files:
                file_path = os.path.join(curr, file_name)
                try:
                    loader = TextLoader(file_path, encoding="utf-8")
                    doc_chunks.extend(
                        loader.load_and_split(
                            text_splitter=RecursiveCharacterTextSplitter(chunk_size=250)
                        )
                    )
                except Exception:
                    pass
        shutil.rmtree("./repo")
        return doc_chunks

    def generate_vector_store(self):
        if os.path.exists(self.index_path):
            return
        doc_chunks = self.recursively_parse_repo_files()
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_documents(doc_chunks, embedding=embeddings)
        vector_store.save_local(self.index_path)
