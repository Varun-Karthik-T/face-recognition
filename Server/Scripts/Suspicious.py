import cv2
import time
import requests
from datetime import datetime, timedelta
from ultralytics import YOLO

# Load YOLO model
model = YOLO('Scripts/models/best.pt') 

# Initialize the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video device.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Initialize the last notification times
last_person_notification_time = datetime.min
last_mask_notification_time = datetime.min

# User ID for the notification
USER_ID = '66d36a9d42d9a5784e1a59fe'  # Replace with the actual user ID
NOTIFICATION_URL = f'http://localhost:5000/notifications/{USER_ID}/suspicious'

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    # Send the frame to the YOLO model for prediction
    results = model(frame)

    # Count the number of person classes detected
    person_count = 0
    mask_found = False
    class_counts = {}
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            confidence = box.conf[0]
            if class_name == "person" and confidence < 0.5:
                continue
            if class_name == "person":
                person_count += 1
            if class_name == "mask":
                mask_found = True
            if class_name in class_counts:
                class_counts[class_name] += 1
            else:
                class_counts[class_name] = 1

    # Print the class counts
    for class_name, count in class_counts.items():
        print(f"Class: {class_name}, Count: {count}")

    # Annotate the frame with the prediction results
    annotated_frame = results[0].plot()

    # Display the annotated frame
    cv2.imshow('Webcam', annotated_frame)

    # Check if more than 3 person classes are detected and if 5 minutes have passed since the last notification
    if person_count > 3 and datetime.now() - last_person_notification_time > timedelta(minutes=5):
        # Update the last notification time
        last_person_notification_time = datetime.now()

        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        files = {
            'image': ('image.jpg', buffer.tobytes(), 'image/jpeg')
        }
        data = {
            'classification': 'Many people found in front of your house!'
        }

        # Send the notification
        response = requests.post(NOTIFICATION_URL, files=files, data=data)
        print("Notification response:", response.json())

    # Check if a mask class is found and if 5 minutes have passed since the last notification
    if mask_found and datetime.now() - last_mask_notification_time > timedelta(minutes=5):
        # Update the last notification time
        last_mask_notification_time = datetime.now()

        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        files = {
            'image': ('image.jpg', buffer.tobytes(), 'image/jpeg')
        }
        data = {
            'classification': 'A masked person found'
        }

        # Send the notification
        response = requests.post(NOTIFICATION_URL, files=files, data=data)
        print("Notification response:", response.json())

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(2)  # Change the frequency to 2 seconds

cap.release()
cv2.destroyAllWindows()