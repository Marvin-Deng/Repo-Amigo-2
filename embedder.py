import os
import shutil
from git import Repo
from dotenv import load_dotenv
from urllib.parse import urlparse
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class RepoEmbedder:
    def __init__(self, github_url: str, github_token=None):
        self.github_url = github_url
        self.repo_name = self.get_repo_name()
        self.repo_path = f"./repo/{self.repo_name}"
        self.index_path = f"./store/{self.repo_name}"
        self.token = github_token

    def get_repo_name(self) -> str:
        parsed_url = urlparse(self.github_url)
        path_components = parsed_url.path.strip("/").split("/")
        return path_components[1] if path_components else None

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
                except Exception as e:
                    pass
                    # print(f"Failed to load file: {file_name} with error {e}")
        shutil.rmtree("./repo")
        return doc_chunks

    def generate_vector_store(self):
        doc_chunks = self.recursively_parse_repo_files()
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_documents(doc_chunks, embedding=embeddings)
        vector_store.save_local(self.index_path)
