import cv2
import time
import os
from Server.db import db as database
from deepface import DeepFace
from scipy.spatial import distance

collection = database['embeddings']

threshold = 0.3;

def capture_image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Countdown from 3 to 1
    for i in range(3, 0, -1):
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.putText(frame, str(i), (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 7, (0, 255, 0), 4, cv2.LINE_AA)
        cv2.imshow('Face Detection', frame)
        cv2.waitKey(1000)  # Wait for 1 second

    # Capture the frame after countdown
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("current.jpg", frame)
        print("Image captured")

    cap.release()
    cv2.destroyAllWindows()

def extract_embedding(photo_path):
    embedding = DeepFace.represent(img_path=photo_path, model_name='Facenet', enforce_detection=False)
    return embedding[0]['embedding']

def store_embedding(name, embedding):
    document = {"name": name, "embedding": embedding}
    collection.insert_one(document)
    print(f"Stored embedding for {name} in the database.")

def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                photo_path = os.path.join(root, file)
                dirname = os.path.basename(root)
                embedding = extract_embedding(photo_path)
                store_embedding(dirname, embedding)
                print(f"Processed {file} in {dirname} directory.")
                print("Embedding stored.")

def calculate_distances(new_embedding):
    documents = collection.find({})
    min_cosine_distance = float('inf')
    closest_name = ""

    for doc in documents:
        db_embedding = doc['embedding'][0]['embedding']
        cosine_dist = distance.cosine(new_embedding, db_embedding)

        print(f"Comparing with {doc['name']}: Cosine Distance = {cosine_dist}")

        if cosine_dist < min_cosine_distance:
            min_cosine_distance = cosine_dist
            closest_name = doc['name']

    return closest_name, min_cosine_distance

def main_menu():
    while True:
        print("\nMenu:")
        print("1. Capture and identify face")
        print("2. Process directory and store embeddings")
        print("3. Identify face from a photo")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            capture_image()
            photo_path = "current.jpg"
            embedding = extract_embedding(photo_path)
            closest_name, cosine_distance = calculate_distances(embedding)
            print(f"Closest match: {closest_name}")
            print(f"Cosine Distance: {cosine_distance}")
        elif choice == '2':
            directory_path = input("Enter the path to the directory: ")
            process_directory(directory_path)
        elif choice == '3':
            photo_path = input("Enter the path to the photo: ")
            embedding = extract_embedding(photo_path)
            closest_name, cosine_distance = calculate_distances(embedding)
            print(f"Closest match: {closest_name}")
            print(f"Cosine Distance: {cosine_distance}")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main_menu()