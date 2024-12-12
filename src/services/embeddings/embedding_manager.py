import os
# os.environ["HTTP_PROXY"] = "http://70.10.15.10:8080"
# os.environ["HTTPS_PROXY"] = "http://70.10.15.10:8080"

from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingManager:
    embeddings = {}
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if 'BAAI/bge-m3' not in self.embeddings:
            EmbeddingManager.embeddings['BAAI/bge-m3'] = HuggingFaceEmbeddings(model_name='BAAI/bge-m3')

    def get_embeddings(self, model_name: str):
        return self.embeddings[model_name]
