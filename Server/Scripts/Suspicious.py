import cv2
import time
import requests
from datetime import datetime, timedelta
from ultralytics import YOLO

model = YOLO('./Models/best.pt') 

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video device.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

last_person_notification_time = datetime.min
last_mask_notification_time = datetime.min
last_suspicious_notification_time = datetime.min
last_summa_notification_time = datetime.min

USER_ID = '66d36a9d42d9a5784e1a59fe'
NOTIFICATION_URL = f'http://localhost:5000/notifications/{USER_ID}/suspicious'

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    results = model(frame)

    person_count = 0
    mask_found = False
    suspicious_found = False
    summa_found = False
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
            if class_name == "mask" and confidence > 0.3:
                mask_found = True
            if class_name == "suspicious" and confidence > 0.85:
                suspicious_found = True
            if (class_name == "knife" or class_name == "weapon")  and confidence > 0.1:
                summa_found = True
            if class_name in class_counts:
                class_counts[class_name] += 1
            else:
                class_counts[class_name] = 1

    for class_name, count in class_counts.items():
        print(f"Class: {class_name}, Count: {count}")

    annotated_frame = results[0].plot()

    cv2.imshow('Webcam', annotated_frame)

    if person_count > 3 and datetime.now() - last_person_notification_time > timedelta(minutes=1):
        last_person_notification_time = datetime.now()
        _, buffer = cv2.imencode('.jpg', frame)
        files = {
            'image': ('image.jpg', buffer.tobytes(), 'image/jpeg')
        }
        data = {
            'classification': 'Many people found in front of your house!'
        }
        response = requests.post(NOTIFICATION_URL, files=files, data=data)
        print("Notification response:", response.json())

    if mask_found and datetime.now() - last_mask_notification_time > timedelta(minutes=1):
        last_mask_notification_time = datetime.now()
        _, buffer = cv2.imencode('.jpg', frame)
        files = {
            'image': ('image.jpg', buffer.tobytes(), 'image/jpeg')
        }
        data = {
            'classification': 'A masked person found'
        }
        response = requests.post(NOTIFICATION_URL, files=files, data=data)
        print("Notification response:", response.json())

    if suspicious_found and datetime.now() - last_suspicious_notification_time > timedelta(minutes=5):
        last_suspicious_notification_time = datetime.now()
        _, buffer = cv2.imencode('.jpg', frame)
        files = {
            'image': ('image.jpg', buffer.tobytes(), 'image/jpeg')
        }
        data = {
            'classification': 'Something blocked the camera!'
        }
        response = requests.post(NOTIFICATION_URL, files=files, data=data)
        print("Notification response:", response.json())

    if summa_found and datetime.now() - last_summa_notification_time > timedelta(minutes=5):
        last_summa_notification_time = datetime.now()
        _, buffer = cv2.imencode('.jpg', frame)
        files = {
            'image': ('image.jpg', buffer.tobytes(), 'image/jpeg')
        }
        data = {
            'classification': 'Weapon detected!'
        }
        response = requests.post(NOTIFICATION_URL, files=files, data=data)
        print("Notification response:", response.json())

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(2)

cap.release()
cv2.destroyAllWindows()