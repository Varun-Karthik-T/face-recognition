import cv2
import requests
import pyttsx3

DETECT_URL = 'http://localhost:5000/detect'

def capture_and_send_image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video device.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture image.")
            break

        cv2.imshow('Press Space to Capture', frame)

        if cv2.waitKey(1) & 0xFF == ord(' '):
            _, buffer = cv2.imencode('.jpg', frame)
            files = {
                'image': ('image.jpg', buffer.tobytes(), 'image/jpeg')
            }
            data = {
                'username': 'Salai' 
            }
            response = requests.post(DETECT_URL, files=files, data=data)
            response_data = response.json()
            print("Response from server:", response_data)

            closest_match = response_data.get('closest_match', 'Unknown person')
            engine = pyttsx3.init()
            engine.say(f"{closest_match} at the door!")
            engine.say(f"{closest_match} at the door!")
            if closest_match == 'Unknown person':
                engine.say("You are new here, please state your reasons for visiting.")
            else:
                engine.say("Door opened!")
            engine.runAndWait()

            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    capture_and_send_image()