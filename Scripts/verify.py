import cv2
import time
from deepface import DeepFace
from scipy.spatial import distance

from Server.db import db as database
collection = database['embedding']

def capture_image():
    
    cap = cv2.VideoCapture(0)
    frames = 0
    start_time = time.time()

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
       
        ret, frame = cap.read()

        detections = DeepFace.extract_faces(frame, detector_backend='opencv', enforce_detection=False)

        if detections is not None:
            for face in detections:
                if frames > 150 & frames % 60 == 0:
                    cv2.imwrite("current.jpg", frame)
                    return True

                x = face['facial_area']['x']
                y = face['facial_area']['y']
                w = face['facial_area']['w']
                h = face['facial_area']['h']

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        frames += 1
        elapsed_time = time.time() - start_time
        fps = frames / elapsed_time
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        last_capture_time = time.time()
       
        cv2.imshow('Face Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def extract_embedding(photo_path):
    """
    Extract facial embedding for a given photo.
    """
    embedding = DeepFace.represent(img_path=photo_path, model_name='Facenet', enforce_detection=False)
    return embedding[0]['embedding']

photo_path = "current.jpg"
def calculate_distances(new_embedding):
    """
    Calculate Cosine distances between the new embedding and all embeddings in the database.
    Prints the distances for every comparison.
    Returns the name of the closest embedding based on Cosine distance.
    """
    
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

capture_image()
# Extract embedding
embedding = extract_embedding(photo_path)

# Calculate distances and find the closest embedding
closest_name, cosine_distance = calculate_distances(embedding)

# Print the results
print(f"Closest match: {closest_name}")
print(f"Cosine Distance: {cosine_distance}")