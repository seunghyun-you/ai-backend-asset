from typing import (
    List,
    Optional,
)

from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain_text_splitters import CharacterTextSplitter

from services.embeddings.embedding_manager import EmbeddingManager
from services.utils.data_utils import check_file_extension, text_loader, csv_loader, metadata_generator, excel_loader

class EmbeddingService:

    def __init__(self, vectorstore):
        self.vectorstore = vectorstore

    def add_embedding_vectors(self, page_contents: List[str],
                                    metadatas: Optional[List[dict]]) -> List[str]:
        added_questions_vectors = self.vectorstore._embed_documents(texts=page_contents)

        added_vectors = []
        for question, vector in zip(page_contents, added_questions_vectors):
            added_vectors.append((question, vector))

        return self.vectorstore.add_embeddings(added_vectors, metadatas=metadatas)

    def add_embedding_docs(self, documents: List[Document]) -> List[str]:

        page_contents = [document.page_content for document in documents]
        metadatas = [document.metadata for document in documents]

        return self.add_embedding_vectors(page_contents, metadatas)

    def embedding_contents(self, embedding_file_path: str, contents_path: str):
        file_extension = check_file_extension(contents_path)

        if file_extension == '.txt':
            load_contents = text_loader(contents_path)
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            docs = text_splitter.split_documents(load_contents)

        elif file_extension == '.csv':
            load_contents = csv_loader(contents_path)
            docs = metadata_generator(load_contents)
            print(docs)

        elif file_extension == '.xlsx':
            load_contents = excel_loader(contents_path)
            docs = metadata_generator(load_contents)

        vectorstore = FAISS.from_documents(docs, embedding=EmbeddingManager().get_embeddings('BAAI/bge-m3'))
        vectorstore.save_local(embedding_file_path)