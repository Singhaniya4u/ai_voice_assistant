import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pyjokes
import re

engine = pyttsx3.init()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def wish_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your offline AI assistant. How can I help you today?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("🧠 Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
    except Exception:
        speak("Sorry, I didn't catch that. Please say again.")
        return ""
    return query.lower()

def calculate(query):
    try:
        expression = re.sub(r"[a-zA-Z]", "", query)  # Remove non-numeric parts
        result = eval(expression)
        return f"The result is {result}"
    except:
        return "Sorry, I couldn't calculate that."

def run_assistant():
    wish_user()
    while True:
        query = take_command()
        if query == "":
            continue

        elif 'time' in query:
            time = datetime.datetime.now().strftime("%H:%M")
            speak(f"The time is {time}")

        elif 'date' in query:
            date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            speak(f"Today is {date}")

        elif 'joke' in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif 'who is' in query or 'what is' in query:
            topic = query.replace("who is", "").replace("what is", "")
            try:
                summary = wikipedia.summary(topic, sentences=2)
                speak(summary)
            except:
                speak("Sorry, I couldn't find information about that.")

        elif 'calculate' in query or any(op in query for op in ['plus', 'minus', 'times', 'divided']):
            speak(calculate(query))

        elif 'exit' in query or 'bye' in query:
            speak("Goodbye! Have a wonderful day!")
            break

        else:
            speak("Sorry, I didn't understand that.")

# 🚀 Run the assistant
run_assistant()
