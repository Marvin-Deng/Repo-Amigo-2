import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class Chain():

    def __init__(self, index_path: str):
        self.index_path = index_path

    def load_faiss_index_by_topic(self):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        if not os.path.exists(self.index_path):
            return None

        faiss_index = FAISS.load_local(
            self.index_path, embeddings, allow_dangerous_deserialization=True
        )
        return faiss_index
