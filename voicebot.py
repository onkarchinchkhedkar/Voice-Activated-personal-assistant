import pyttsx3
import speech_recognition as sr
import requests
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()
recognizer = sr.Recognizer()
mic = sr.Microphone()

def listen():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        return ""
WEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"
NEWS_API_KEY = "YOUR_NEWS_API_KEY"
CITY = "Nashik"
def get_weather():
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={CITY}&appid={WEATHER_API_KEY}&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return "I couldn't get the weather."

    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    return f"The temperature in {CITY} is {temp} degrees with {description}."

def get_news():
    url = (
        f"https://newsapi.org/v2/top-headlines"
        f"?country=in&apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    if data["status"] != "ok":
        return "I couldn't fetch the news."

    headlines = [a["title"] for a in data["articles"][:3]]
    return "Here are the top headlines: " + ". ".join(headlines)
def handle_command(command):
    if "weather" in command:
        return get_weather()
    elif "news" in command:
        return get_news()
    elif "exit" in command or "stop" in command:
        return "exit"
    else:
        return "Sorry, I didn't understand that."
speak("Hello! How can I help you?")

while True:
    command = listen()
    if not command:
        continue

    response = handle_command(command)

    if response == "exit":
        speak("Goodbye!")
        break

    speak(response)
