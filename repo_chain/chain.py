import os
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

from state_store import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)


class RepoChain:

    def __init__(self, index_path: str):
        self.index_path = index_path
        self.chain = None

    def load_faiss_index(self):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        if not os.path.exists(self.index_path):
            return
        faiss_index = FAISS.load_local(
            self.index_path, embeddings, allow_dangerous_deserialization=True
        )
        return faiss_index

    def generate_conversational_chain(self) -> None:
        prompt_template = f"""
            Answer the question about the github repo. Provide suggestions on improvements\n
            Consider the following:
            - Relevant code to the question
            - Relevant code in other parts of the repository
            - Context of the question
            \n\n
            Context:\n{{context}}?\n
            Question: \n{{question}}\n

            Answer:
            """
        model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.5)
        prompt = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )
        self.chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    def get_response(self, user_question: str) -> str:
        db = self.load_faiss_index()
        if db is None:
            return "Couldn't find the repo"
        try:
            docs = db.similarity_search(user_question)
            if not self.chain:
                return "Chain has not been generated"
            response = self.chain(
                {"input_documents": docs, "question": user_question},
                return_only_outputs=True,
            )
            return response["output_text"]
        except Exception:
            return "The model stopped generating text unexpectedly. Please try again with a different query."
