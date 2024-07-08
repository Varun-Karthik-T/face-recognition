from db import db as database
from deepface import DeepFace
from scipy.spatial import distance

def extract_embedding(photo_path):
    """
    Extract facial embedding for a given photo.
    """
    embedding = DeepFace.represent(img_path=photo_path, model_name='Facenet', enforce_detection=False)
    return embedding[0]['embedding']

# Ask for the photo path
photo_path = input("Enter the path to the photo: ")
def calculate_distances(new_embedding):
    """
    Calculate Cosine distances between the new embedding and all embeddings in the database.
    Prints the distances for every comparison.
    Returns the name of the closest embedding based on Cosine distance.
    """
    collection = database['embeddings']
    documents = collection.find({})
    
    min_cosine_distance = float('inf')
    closest_name = ""
    
    for doc in documents:
        db_embedding = doc['embedding'][0]['embedding']
        cosine_dist = distance.cosine(new_embedding, db_embedding)
        
        # Print distances for each comparison
        print(f"Comparing with {doc['name']}: Cosine Distance = {cosine_dist}")
        
        if cosine_dist < min_cosine_distance:
            min_cosine_distance = cosine_dist
            closest_name = doc['name']
    
    return closest_name, min_cosine_distance

# Extract embedding
embedding = extract_embedding(photo_path)

# Calculate distances and find the closest embedding
closest_name, cosine_distance = calculate_distances(embedding)

# Print the results
print(f"Closest match: {closest_name}")
print(f"Cosine Distance: {cosine_distance}")