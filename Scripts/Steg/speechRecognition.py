import speech_recognition as sr

# Function to convert audio to text
def audio_to_text(audioFile):
    r = sr.Recognizer()
    with sr.AudioFile(audioFile) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
    return text