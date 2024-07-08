import os
from db import db as database
from deepface import DeepFace

def extract_embedding(photo_path):
    """
    Extract facial embedding for a given photo.
    """
    embedding = DeepFace.represent(img_path=photo_path, model_name='Facenet', enforce_detection=False)
    return embedding

def store_embedding(name, embedding):
    """
    Store the embedding into MongoDB collection.
    """
    collection = database['embeddings']
    document = {"name": name, "embedding": embedding}
    collection.insert_one(document)
    print(f"Stored embedding for {name} in the database.")

def process_directory(directory_path):
    """
    Process each photo in the directory and its subdirectories, extract embeddings, and store them.
    Uses the subdirectory name as the identifier for the embeddings.
    """
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                photo_path = os.path.join(root, file)
                # Extract the directory name from the path
                dirname = os.path.basename(root)
                embedding = extract_embedding(photo_path)
                # Use the directory name as the identifier
                store_embedding(dirname, embedding)
                print(f"Processed {file} in {dirname} directory.")
                print("Embedding stored.")

# Ask for the directory path
directory_path = input("Enter the path to the directory: ")

# Process the directory
process_directory(directory_path)