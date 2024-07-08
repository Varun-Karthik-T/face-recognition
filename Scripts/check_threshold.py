from db import db as database
from deepface import DeepFace
from scipy.spatial import distance

def extract_embedding(photo_path):
    """
    Extract facial embedding for a given photo.
    """
    embedding = DeepFace.represent(img_path=photo_path, model_name='Facenet512', enforce_detection=False)
    return embedding

# Define an array of paths to images
photo_paths = [
    "./test_photos/Lana Del Rey/test1.jpg",
    "./test_photos/Lana Del Rey/test2.jpg",
    "./test_photos/Lana Del Rey/test3.jpg",
    "./test_photos/Lana Del Rey/test4.jpg",
    "./test_photos/Lana Del Rey/test5.jpg",
    "./test_photos/Lana Del Rey/no2.jpg",
    "./test_photos/Lana Del Rey/no3.jpg",
    "./test_photos/Lana Del Rey/no4.jpg",
    "./test_photos/Lana Del Rey/no5.jpg",
    ]

# Initialize the global threshold variable
threshold = 0.3

def calculate_distances(new_embedding, threshold):
    """
    Calculate Cosine distances between the new embedding and all embeddings in the database.
    Prints the distances for every comparison within the threshold.
    Returns the top 3 closest embeddings based on Cosine distance.
    """
    collection = database['Salai_test']
    documents = collection.find({})
    
    distances = []
    
    for doc in documents:
        db_embedding = doc['embedding'][0]['embedding']
        cosine_dist = distance.cosine(new_embedding, db_embedding)
        
        if cosine_dist <= threshold:
            # Store distances with name for each comparison if within threshold
            distances.append((doc['name'], cosine_dist))
    
    # Sort by distance
    distances.sort(key=lambda x: x[1])
    
    # Return top 3 closest matches
    return distances[:3]

while threshold <= 1:
    print(f"\nProcessing with threshold: {threshold}")
    for path in photo_paths:
        # Extract embedding
        embedding = extract_embedding(path)
        face_confidence = embedding[0]['face_confidence']
        if face_confidence < 0.85:
            print(f"Face not detected in {path}. Confidence: {face_confidence}")
            continue
        print(f"\nProcessing {path}")
        # Calculate distances and find the top 3 closest embeddings
        top_matches = calculate_distances(embedding[0]['embedding'], threshold)
        
        # Print the top 3 results
        print("Top 3 closest matches:")
        for i, (name, dist) in enumerate(top_matches, start=1):
            print(f"{i}. {name} with Cosine Distance: {dist}")
    
    # Increase the threshold by 0.1
    threshold += 0.05