import time
import requests
import pyttsx3
import speech_recognition as sr

USER_ID = '66d36a9d42d9a5784e1a59fe'
GET_PERMISSIONS_URL = f'http://localhost:5000/permissions/{USER_ID}'
UPDATE_PERMISSION_URL = f'http://localhost:5000/permissions/{USER_ID}'

def fetch_permissions(user_id):
    try:
        response = requests.get(GET_PERMISSIONS_URL)
        if response.status_code == 200:
            return response.json().get('entries', [])
        else:
            print(f"Failed to fetch permissions: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching permissions: {str(e)}")
        return []

def update_permission(user_id, index, allow):
    try:
        data = {'allow': allow}
        response = requests.put(f'{UPDATE_PERMISSION_URL}/{index}', json=data)
        if response.status_code == 200:
            print("Permission updated successfully")
        else:
            print(f"Failed to update permission: {response.status_code}")
    except Exception as e:
        print(f"Error updating permission: {str(e)}")

def main():
    engine = pyttsx3.init()
    recognizer = sr.Recognizer()

    while True:
        permissions = fetch_permissions(USER_ID)
        for index, entry in enumerate(permissions):
            name = entry.get('name', 'Unknown')
            reason = entry.get('reason', 'No reason provided')

            engine.say(f"{name} wants to visit for the following reason: {reason}. Do you want to allow this person?")
            engine.runAndWait()

            with sr.Microphone() as source:
                while True:
                    print("Listening for your response...")
                    audio = recognizer.listen(source)
                    try:
                        response = recognizer.recognize_google(audio)
                        print(f"Response: {response}")

                        if 'yes' in response.lower():
                            update_permission(USER_ID, index, True)
                            break
                        elif 'no' in response.lower():
                            update_permission(USER_ID, index, False)
                            break
                        else:
                            print("Could not understand the response. Please say 'yes' or 'no'.")
                    except sr.UnknownValueError:
                        print("Could not understand the audio")
                    except sr.RequestError as e:
                        print(f"Could not request results; {e}")

        time.sleep(10)

if __name__ == '__main__':
    main()