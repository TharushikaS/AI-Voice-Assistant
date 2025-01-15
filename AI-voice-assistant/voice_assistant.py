import pyttsx3
import speech_recognition as sr
import openai
import env

# OpenAI key
openai.api_key = env.OPEN_AI_KEY

# Initialize speech engine
engine = pyttsx3.init()

def speak(word):
    engine.setProperty('rate', 135)
    engine.setProperty('volume', 0.8)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(str(word))
    engine.runAndWait()
    engine.stop()

# Initialize Speech Recognizer
rec = sr.Recognizer()
speak("Hello Sir, I am listening for your command.")

try:
    with sr.Microphone() as source:
        print("Listening...")
        audio = rec.listen(source)
        speak("I am computing an answer for your request. I will be done soon.")

    text = rec.recognize_google(audio)
    print(f"You said: {text}")

    # Use ChatCompletion API
    discussion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if available
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ],
        max_tokens=1000,
    )

    answer = discussion["choices"][0]["message"]["content"]

    if answer:
        print(f"AI's response: {answer}")
        speak(answer)

except sr.UnknownValueError:
    speak("Sorry, I could not understand your command. Please try again.")
except sr.RequestError as e:
    speak(f"Could not request results from the microphone; {e}")
except Exception as ex:
    print(f"An error occurred: {ex}")  # Log error for debugging
    speak("An error occurred while processing your request. Please try again.")
