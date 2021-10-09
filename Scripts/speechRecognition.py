import speech_recognition as sr
import os

# Function to convert audio to text
def audio_to_text(audioFile):
    file_format = os.path.splitext(audioFile)[-1].lower()
    name = os.path.basename(audioFile)
    name = name.replace(file_format, '')

    r = sr.Recognizer()
    with sr.AudioFile(audioFile) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)

    with open('Scripts\\static\speechRecog\\' + name + '_speech_text.txt', 'w') as f:
        f.write(text)
    
    return 'Scripts\\static\speechRecog\\' + name + '_speech_text.txt'