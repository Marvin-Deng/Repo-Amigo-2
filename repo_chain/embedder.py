import os
import re
import shutil
import streamlit as st
from git import Repo
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from constants import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)


class RepoEmbedder:
    def __init__(
        self, github_url: str, repo_owner: str, repo_name: str, github_token=None
    ):
        self.github_url = github_url
        self.repo_name = repo_name
        self.repo_path = f"./repo/{repo_owner}-{repo_name}"
        self.index_path = f"./store/{repo_owner}-{repo_name}"
        self.token = github_token

    def clone_repo(self):
        if os.path.exists(self.repo_path) or os.path.exists(self.index_path):
            return
        try:
            if self.token:
                parts = re.split(r"(github\.com)", self.github_url)
                formatted_url = f"{parts[0]}{self.token}@{parts[1]}{parts[2]}.git"

                print(f"formatted_url: {formatted_url}")
            else:
                formatted_url = self.github_url
            Repo.clone_from(formatted_url, self.repo_path)
        except Exception:
            st.write("Error cloning repo")

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
                    # print(f"Failed to load file: {file_name} with error {e}")
        shutil.rmtree("./repo")
        return doc_chunks

    def generate_vector_store(self):
        if os.path.exists(self.index_path):
            return
        doc_chunks = self.recursively_parse_repo_files()
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_documents(doc_chunks, embedding=embeddings)
        vector_store.save_local(self.index_path)
