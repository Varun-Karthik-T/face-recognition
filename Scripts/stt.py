#pip install SpeechRecognition PyAudio


import speech_recognition as sr

def speech_to_text_from_mic():
    recognizer = sr.Recognizer()


    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")

        audio_data = recognizer.listen(source)
        
        try:
            # Recognize the speech using Google's free web-based API
            print("Recognizing...")
            text = recognizer.recognize_google(audio_data)
            print("You said: " + text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

# Run the function
speech_to_text_from_mic()
