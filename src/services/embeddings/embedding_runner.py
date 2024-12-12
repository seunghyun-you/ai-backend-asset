import sys
sys.path.append('.')
import glob
import json
import pandas as pd

from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain_text_splitters import CharacterTextSplitter

from services.embeddings.embedding_manager import EmbeddingManager
from services.utils.data_utils import check_file_extension, text_loader, csv_loader, metadata_generator, excel_loader, merge_multiple_contents, single_turn_metadata_generator

from services.embeddings.embedding_service import EmbeddingService
from services.retrievers.retriever_manager import RetrieverManager


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

def embedding_contents_maker(embedding_file_path: str, original_content_path: str):
    file_extension = check_file_extension(original_content_path)

    if file_extension == '.txt':
        loaded_content = text_loader(original_content_path)
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(loaded_content)

    elif file_extension == '.csv':
        loaded_content = csv_loader(original_content_path)
        docs = metadata_generator(loaded_content)

    elif file_extension == '.xlsx':
        loaded_content = excel_loader(original_content_path)
        docs = metadata_generator(loaded_content)

    vectorstore = FAISS.from_documents(docs, embedding=EmbeddingManager().get_embeddings('BAAI/bge-m3'))
    vectorstore.save_local(embedding_file_path)

def single_turn_embedding_content_maker(embedding_file_path: str, original_contents_dir_path: str, content_save_path: str):
    merge_multiple_contents(original_contents_dir_path, content_save_path)

    loaded_content = csv_loader(content_save_path)
    docs = single_turn_metadata_generator(loaded_content)
    print(docs)

    vectorstore = FAISS.from_documents(docs, embedding=EmbeddingManager().get_embeddings('BAAI/bge-m3'))
    vectorstore.save_local(embedding_file_path)

#embedding_contents_maker(embedding_data_path["toyota"]["manual"], source_data_path["toyota"]["manual"])
#embedding_contents_maker(embedding_data_path["doosan"]["parts_book"], source_data_path["doosan"]["parts_book"])
single_turn_embedding_content_maker(embedding_data_path["single_turn"], "database/source_documents/*.csv", source_data_path["single_turn"])
