import re
import sys
sys.path.append('../..')

from langchain_community.vectorstores import FAISS
from langchain_core.runnables import ConfigurableField

from services.embeddings.embedding_manager import EmbeddingManager

embedding_data_path = {
    "sample_01" : "database/embedding_data/sample_01",
    "sample_02": "database/embedding_data/sample_02",
}

def create_retrieval(embedding_data_path: str):
    try:
        vectorstore = FAISS.load_local(embedding_data_path, 
                                       embeddings=EmbeddingManager().get_embeddings('BAAI/bge-m3'), 
                                       allow_dangerous_deserialization=True)
        retrieval = vectorstore.as_retriever()
    except FileNotFoundError:
        print(f"Error: \"{embedding_data_path}\" does not exist.")
        print("Start the embedding process.")

    configurable_retrieval = retrieval.configurable_fields(
        metadata=ConfigurableField(
            id="metadata",
            name="Metadata Filter",
            description="The metadata filter to apply",),
        search_kwargs=ConfigurableField(
            id="search_kwargs")
    )

    return configurable_retrieval

class retrievalManager:
    retrievals = {}
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self.retrievals:
            self.retrievals['sample_01'] = create_retrieval(embedding_data_path["sample_01"])
            self.retrievals['sample_02'] = create_retrieval(embedding_data_path["sample_02"])

    def get_retrieval(self, sample_name: str):
        return self.retrievals[sample_name]
    
    def get_configurable_retrievals(self):
        sample_01 = self.get_retrieval('sample_01')

        return sample_01.configurable_alternatives(
            ConfigurableField(id='retrieval'),
            default_key='sample_01',
            sample_02=self.get_retrieval('sample_02'),
        )