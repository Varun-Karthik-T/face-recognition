import cv2
import requests
import pyttsx3
import speech_recognition as sr

DETECT_URL = 'http://localhost:5000/detect'
ADD_PERMISSION_URL = 'http://localhost:5000/permissions/66d36a9d42d9a5784e1a59fe'
USER_ID = '66d36a9d42d9a5784e1a59fe'

def get_active_profile(user_id):
    ACTIVE_PROFILE_URL = f'http://localhost:5000/profiles/{user_id}/active'
    try:
        response = requests.get(ACTIVE_PROFILE_URL)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch active profile: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching active profile: {str(e)}")
        return None

def get_profiles(user_id):
    PROFILES_URL = f'http://localhost:5000/profiles/{user_id}'
    try:
        response = requests.get(PROFILES_URL)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch profiles: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching profiles: {str(e)}")
        return None

def capture_and_send_image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video device.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    active_profile = get_active_profile(USER_ID)
    if not active_profile:
        print("No active profile found.")
        return

    print(f"Active Profile: {active_profile}")

    profiles = get_profiles(USER_ID)
    if not profiles:
        print("No profiles found.")
        return

    active_profile_id = active_profile.get('active_profile_id')
    allowed_people = []
    for profile in profiles.get('profiles', []):
        if profile.get('id') == active_profile_id:
            allowed_people = profile.get('allowed_people', [])
            break

    print(f"Allowed People in Active Profile: {allowed_people}")
    child_mode = active_profile_id == 2

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
                'username': active_profile.get('username', 'Unknown')
            }
            response = requests.post(DETECT_URL, files=files, data=data)
            response_data = response.json()
            print("Response from server:", response_data)

            closest_match = response_data.get('closest_match', 'Unknown person')
            engine = pyttsx3.init()
            engine.say(f"{closest_match} at the door!")

            is_allowed = any(person['name'] == closest_match for person in allowed_people)

            if (child_mode and not is_allowed):
                engine.say("Nobody at home, please come back later.")
                engine.runAndWait()
                continue

            if closest_match == 'Unknown person' or not is_allowed:
                if closest_match == 'Unknown person':
                    engine.say("You are new here, please state your reasons for visiting.")
                else:
                    engine.say("Please state your reasons for visiting.")

                engine.runAndWait()

                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    while True:
                        print("Listening for reason...")
                        audio = recognizer.listen(source)
                        try:
                            reason = recognizer.recognize_google(audio)
                            print(f"Reason: {reason}")

                            permission_data = {
                                'name': closest_match if closest_match != 'Unknown person' else 'Unknown',
                                'reason': reason
                            }
                            permission_files = {
                                'image': ('image.jpg', buffer.tobytes(), 'image/jpeg')
                            }
                            permission_response = requests.post(ADD_PERMISSION_URL, files=permission_files, data=permission_data)
                            print("Permission response:", permission_response.json())
                            break
                        except sr.UnknownValueError:
                            engine.say("I could not understand you, please try again.")
                            print("Could not understand the audio")
                        except sr.RequestError as e:
                            print(f"Could not request results; {e}")
            else:
                engine.say("Door opened!")
                engine.runAndWait()
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    active_profile = get_active_profile(USER_ID)
    if active_profile:
        print(f"Active Profile: {active_profile}")
    capture_and_send_image()