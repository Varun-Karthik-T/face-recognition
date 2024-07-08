from gtts import gTTS
import os

# Text to be converted to speech
text = "Hello, how are you doing today?"

# Language in which you want to convert
language = 'en'

# Passing the text and language to the engine
speech = gTTS(text=text, lang=language, slow=False)

# Saving the converted audio in a mp3 file named "output.mp3"
speech.save("output.mp3")

# Playing the converted file
os.system("start output.mp3")  # For Windows
# os.system("mpg321 output.mp3")  # For Linux
