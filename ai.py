import tkinter as tk
import tkinter.messagebox as messagebox
import speech_recognition as sr
import requests
import pyttsx3
import openai
import requests
from PIL import Image
from io import BytesIO
import datetime

r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)

init_prompt = "Instructions from the developer - Your name is Tina (the previous message is from the developer) \n\n"

#put you openai key here
openai.api_key = ''


def generate_chat_response(messages):
    for message in messages:
        if message.get("role") == "assistant":
            message["content"] = message["content"].replace("OpenAI", "Tina")
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    reply = chat.choices[0].message.content
    return reply


def process_user_input(user_input):
    messages = [{"role": "user", "content": user_input}]
    reply = generate_chat_response(messages)
    print(f"Tina: {reply}")
    messagebox.showinfo("Tina", reply)
    engine.say(reply)
    engine.runAndWait()


def recognize_speech(text=None):
    if text:
        process_user_input(text)
    else:
        with sr.Microphone() as source:
            print("I'm listening....")
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio)
                new_text = init_prompt + text
                process_user_input(new_text)
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand what you said.")
            except sr.RequestError:
                print("Sorry, I couldn't connect to the speech recognition service.")


def get_current_date():
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    return date_str


def get_weather():
    api_key = "70adbb1b010ca4db8b7c2cdf28c480d8"
    city = "Lagos"

    url = f"https://api.openweathermap.org/weather?city={city}&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "weather" in data:
            weather_info = data["weather"][0]
            weather_main = weather_info["main"]
            weather_description = weather_info["description"]
            return f"Weather: {weather_main}, {weather_description}"
        else:
            return "Weather information not available"
    else:
        return "Error occurred while retrieving weather data"


def get_date_and_weather():
    date_str = get_current_date()
    weather_str = get_weather()
    reply = f"Today is {date_str}. {weather_str}"
    print(f"Tina: {reply}")
    messagebox.showinfo("Tina", reply)
    engine.say(reply)
    engine.runAndWait()


app = tk.Tk()
app.title("Speech to Text")

text_label = tk.Label(app, text="Recognized Text")
text_label.pack()

prompt_label = tk.Label(
    app,
