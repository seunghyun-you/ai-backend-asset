import os
import sys
import glob
sys.path.append('../..')

# import base64
# import json
# sagemaker_endpoint_name = os.environ.get("SAGEMAKER_ENDPOINT_NAME",
#                                          'huggingface-pytorch-inference-2024-03-21-02-35-43-380')
# sagemaker_endpoint_region = os.environ.get("SAGEMAKER_ENDPOINT_REGION", 'ap-northeast-2')

import pandas as pd

from langchain.docstore.document import Document
from langchain_community.document_loaders import TextLoader
# from datetime import datetime

# from langchain_community.storage import SQLStore
# from langchain_community.retrievers import BM25Retriever
# from langchain_community.vectorstores import FAISS

# from langchain.retrievers.multi_vector import MultiVectorRetriever

# NOTE :: Function to check the extension of the file 
def check_file_extension(file_path):
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    return file_extension

# NOTE :: Data Loader
def text_loader(file_path: str):
    try:
        loader = TextLoader(file_path, encoding='utf-8')
        return loader.load()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def csv_loader(file_path: str):
    return pd.read_csv(file_path)


def excel_loader(file_path: str):
    return pd.read_excel(file_path)

# NOTE :: Metadata generator (auto)
def metadata_generator(documents: str):
    docs = []
    for _, row in documents.iterrows():
        page_content = row['page_content']
        metadata = {col: row[col] for col in documents.columns if col != 'page_content'}
        
        docs.append(Document(page_content=page_content, metadata=metadata))
    return docs

def single_turn_metadata_generator(documents: str):
    docs = []
    for _, row in documents.iterrows():
        page_content = f"{row['page_content']} {row['brand_name']} {row['model_name']}"
        metadata = {col: row[col] for col in documents.columns if col != 'page_content'}
        
        docs.append(Document(page_content=page_content, metadata=metadata))
    return docs

# NOTE :: Single_Turn Content Maker (Merge content)
def merge_multiple_contents(file_dir_path: str, file_save_path: str):
    file_list = glob.glob(file_dir_path)

    columns_to_extract = ['brand_name', 'model_name', 'knowledge_type', 'file_name', 'page_content', 'page_number', 'title']
    combined_data = pd.DataFrame(columns=columns_to_extract)

    for file in file_list:
        df = pd.read_csv(file)
        extracted_data = df[columns_to_extract]
        combined_data = pd.concat([combined_data, extracted_data], ignore_index=True)

    combined_data.to_csv(file_save_path, index=False)

# NOTE :: select option extractor
def front_select_option_extractor(content_path: str, column_name: str):
    df = pd.read_csv(content_path)
    
    unique_titles = df[column_name].unique()
    sorted_titles = sorted(unique_titles)
    
    options = [f'{{ value: "{title}", label: "{title}" }}' for title in sorted_titles]
    result = 'export const abnormalSymptomOptions = [\n'
    result += ',\n'.join(options)
    result += '\n];\n'
    print(result)