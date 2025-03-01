import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import json
import re
import operator
import requests
from bs4 import BeautifulSoup

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Load or create app list
app_list_file = "app_list.json"
if os.path.exists(app_list_file):
    with open(app_list_file, "r") as file:
        app_list = json.load(file)
else:
    app_list = {"notepad": "notepad.exe", "calculator": "calc.exe"}


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand.")
        return ""
    except sr.RequestError:
        speak("Could not connect to the speech service.")
        return ""


def open_website(command):
    site = command.replace("open ", "").strip()
    url = f"https://www.{site}.com"
    webbrowser.open(url)
    speak(f"Opening {site}")


def open_app(command):
    app_name = command.replace("open ", "").strip()
    if app_name in app_list:
        os.system(app_list[app_name])
        speak(f"Opening {app_name}")
    else:
        speak("App not found in list. Say 'add app name as an app' to add it.")


def add_app(command):
    parts = command.split(" as an app")
    if len(parts) > 1:
        app_name = parts[0].replace("add ", "").strip()
        speak(f"Please enter the executable path for {app_name}")
        app_path = input(f"Enter path for {app_name}: ")
        app_list[app_name] = app_path
        with open(app_list_file, "w") as file:
            json.dump(app_list, file)
        speak(f"{app_name} added as an app.")


def calculate(command):
    command = command.replace("calculate ", "").strip()
    command = command.replace("plus", "+").replace("minus", "-")
    command = command.replace("multiply", "*").replace("divide", "/")
    command = command.replace("power", "**")

    try:
        result = eval(command)
        speak(f"The result is {result}")
        print("Result:", result)
    except Exception as e:
        speak("Invalid calculation format.")
        print("Error:", e)


def search_web(command):
    query = command.replace("search for ", "").strip()
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    result = soup.find("h3")
    if result:
        speak(f"Here is what I found for {query}")
        print("Top result:", result.text)
    else:
        speak("Sorry, I couldn't find relevant information.")
    webbrowser.open(url)


def main():
    speak("Hello! I am Darvis How can I help?")
    while True:
        command = listen()
        if "open" in command:
            if "as an app" in command:
                add_app(command)
            elif command.replace("open ", "").strip() in app_list:
                open_app(command)
            else:
                open_website(command)
        elif "calculate" in command:
            calculate(command)
        elif "search for" in command:
            search_web(command)
        elif "exit" in command:
            speak("Goodbye!")
            break


if __name__ == "__main__":
    main()
