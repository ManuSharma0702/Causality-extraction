import argparse
import os
import shutil
import json
from dataprocess_utils import *
from langchain.vectorstores.chroma import Chroma
from langchain.schema.document import Document
from get_embeddings_function import get_embedding_function
from tqdm import tqdm

CHROMA_PATH = "chroma"
DATA_PATH = "data"

def main():
    # Check if the database should be cleared (using the --reset flag).
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    # Create (or update) the data store.
    elements = load_elements()  # Load your list of elements here
    add_elements_to_chroma(elements)

def load_elements():
    # Replace with the actual logic to load your list of elements.
    # For example, this could read from a file or be a hardcoded list.
    
    train_path = 'C:/Users/USER/Desktop/final_project/BioRED/Train.BioC.JSON'
    test_path = 'C:/Users/USER/Desktop/final_project/BioRED/Test.BioC.JSON'
    val_path = 'C:/Users/USER/Desktop/final_project/BioRED/Dev.BioC.JSON'

    with open(train_path, 'r') as file:
        train_data_j = json.load(file)

    with open(test_path, 'r') as file:
        test_data_j = json.load(file)

    with open(val_path, 'r') as file:
        val_data_j = json.load(file)

    all_train_documents_information = train_data_j["documents"]
    all_test_documents_information = test_data_j["documents"]
    all_val_documents_information = val_data_j["documents"]
    train_data, test_data, val_data = creating_readable_chunks(all_train_documents_information, all_test_documents_information, all_val_documents_information)
    return train_data

def add_elements_to_chroma(elements):
    # Load the existing database.
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    # Prepare documents with metadata for each element.
    documents = []
    for i, element in enumerate(elements):

        metadata = {
            'id': f"element_{i}",  # Unique ID for each element
            'source': 'manual_input',  # Indicate the source
            'entities': str(element['entities']),  # Add any relevant entities here
            'relations': str(element['relations'])  # Add any relevant relations here
        }
        document = Document(page_content=element['text'], metadata=metadata)

        documents.append(document)


    # Add or update the documents in the database.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    new_chunks = []
    for document in documents:
        if document.metadata["id"] not in existing_ids:
            new_chunks.append(document)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]

        # Use tqdm to show a progress bar
        for chunk, chunk_id in tqdm(zip(new_chunks, new_chunk_ids), total=len(new_chunks), desc="Adding documents"):
            db.add_documents([chunk], ids=[chunk_id])
        
        print("✅ New documents added.")
    else:
        print("✅ No new documents to add")

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

if __name__ == "__main__":
    main()
    
