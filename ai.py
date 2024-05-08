import tkinter as tk
import tkinter.messagebox as messagebox
import speech_recognition as sr
import requests
import pyttsx3
import openai

r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)

init_prompt = "Instructions - Your name is Tina \n\n"

openai.api_key = ''

batch_messages = []  # Initialize the batch_messages list

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

def speech_to_text():
    messages = [{"role": "user", "content": "You are an interactive friendly AI."}]
    
    with sr.Microphone() as source:
        print("I'm listening....")
        audio = r.listen(source)
        
        try:
            text = r.recognize_google(audio)
            print("You said:", text)
            
            if "tina" in text.lower():
                new_text = init_prompt + text
                messages.append({"role": "user", "content": new_text})
                batch_messages.extend(messages)  # Accumulate messages in batch_messages list
            else:
                print("Sorry, I didn't hear 'tina'.")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
        except sr.RequestError:
            print("Sorry, I couldn't connect to the speech recognition service.")

def send_batch_request(messages):
    if len(messages) > 0:
        # Make API request with batched messages
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        # Process the API response
        for message in chat.choices[0].message.content:
            reply = message.get("content", "")
            if reply:
                print(f"Tina: {reply}")
                engine.say(reply)
                engine.runAndWait()
                messages.append({"role": "assistant", "content": reply})
    
    return messages

def recognize_speech():
    text_label.config(text="Listening...", fg="blue")  
    button.config(state="disabled")  
    prompt_label.config(text="Listening...") 
    speech_to_text()
    
    if len(batch_messages) >= 3:  # Adjust the threshold as per your requirement
        batch_messages = send_batch_request(batch_messages)
        batch_messages = []  # Clear the batch_messages list
    
    text_label.config(text="Recognized Text", fg="black")  
    button.config(state="normal")  
    prompt_label.config(text="Say 'Hello' to start the conversation")

app = tk.Tk()
app.title("Speech to Text")

text_label = tk.Label(app, text="Recognized Text")
text_label.pack()

prompt_label = tk.Label(app, text="Say 'tina' to start the conversation")
prompt_label.pack()

button = tk.Button(app, text="Start Listening", command=recognize_speech)
button.pack()

app.mainloop()
