import re
import sys
sys.path.append('../..')

from langchain_community.vectorstores import FAISS
from langchain_core.runnables import ConfigurableField

from services.embeddings.embedding_manager import EmbeddingManager

source_data_path = {
    "toyota" : {
        "manual": "database/source_documents/toyota_manual.csv",
        "parts_book": "database/source_documents/toyota_parts_book.csv"
    },
    "doosan": {
        "manual": "database/source_documents/doosan_manual.csv",
        "parts_book": "database/source_documents/doosan_parts_book.csv"
    },
    "single_turn": "database/source_documents/single_turn.csv"
}
embedding_data_path = {
    "toyota" : {
        "manual": "database/toyota_manual",
        "parts_book": "database/toyota_parts_book"
    },
    "doosan": {
        "manual": "database/doosan_manual",
        "parts_book": "database/doosan_parts_book"
    },
    "single_turn": "database/single_turn"
}

def create_retriever(embedding_file_path: str):

    try:
        vectorstore = FAISS.load_local(embedding_file_path, 
                                       embeddings=EmbeddingManager().get_embeddings('BAAI/bge-m3'), 
                                       allow_dangerous_deserialization=True)
        retriever = vectorstore.as_retriever()
    except FileNotFoundError:
        print(f"Error: \"{embedding_file_path}\" does not exist.")
        print("Start the embedding process.")

    configurable_retriever = retriever.configurable_fields(
        metadata=ConfigurableField(
            id="metadata",
            name="Metadata Filter",
            description="The metadata filter to apply",),
        search_kwargs=ConfigurableField(
            id="search_kwargs")
    )

    return configurable_retriever

class RetrieverManager:
    retrievers = { "toyota": {}, "doosan": {}, "common": {} }
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.retrievers['toyota']['manual'] = create_retriever(embedding_data_path["toyota"]["manual"])
        self.retrievers['toyota']['parts_book'] = create_retriever(embedding_data_path["toyota"]["parts_book"])
        self.retrievers['doosan']['manual'] = create_retriever(embedding_data_path["doosan"]["manual"])
        self.retrievers['doosan']['parts_book'] = create_retriever(embedding_data_path["doosan"]["parts_book"])
        self.retrievers['common']['single_turn'] = create_retriever(embedding_data_path["single_turn"])

    def get_retriever(self, brand_name: str, knowledge_type: str):
        return self.retrievers[brand_name][knowledge_type]
    
    def get_configurable_retrievers(self):
        toyota_manual = self.get_retriever('toyota','manual')

        return toyota_manual.configurable_alternatives(
            ConfigurableField(id='retriever'),
            default_key='toyota_manual',
            toyota_parts_book=self.get_retriever('toyota','parts_book'),
            doosan_manual=self.get_retriever('toyota','manual'),
            doosan_parts_book=self.get_retriever('doosan','parts_book'),
            single_turn=self.get_retriever('common','single_turn'),
        )