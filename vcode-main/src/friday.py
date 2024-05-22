import speech_recognition as sr
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import sys
import os
from os import listdir
from os.path import isfile, join
import wikipedia
from threading import Thread
import platform
import app
import pyttsx3  # Importing pyttsx3 for text-to-speech

# Importing date class from datetime module
from datetime import date

# Initialize the text-to-speech engine based on the platform
if platform.system() == "Windows":
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
    except Exception as e:
        print("Failed to initialize text-to-speech engine:", e)
        engine = None
else:
    # Initialize engine for other platforms or handle accordingly
    engine = None

# ----------------Variables------------------------
file_exp_status = False
files = []
path = ''
is_awake = True  # Bot status

# ------------------Functions----------------------

# Function to reply using text-to-speech
def reply(audio):
    if engine:
        # Assuming this is a function you define to reply using the text-to-speech engine
        print(audio)
        engine.say(audio)
        engine.runAndWait()
    else:
        print("Text-to-speech engine is not initialized.")

def wish():
    # Get today's date
    today = date.today()
    
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        reply("Good Morning Harsha!")
    elif 12 <= hour < 18:
        reply("Good Afternoon Harsha!")   
    else:
        reply("Good Evening Harsha!")  
        
    reply("I am Harsha's personal AI, What can I do for you!")

def record_audio():
    global sr
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.8
        voice_data = ''
        audio = r.listen(source, phrase_time_limit=5)

        try:
            voice_data = r.recognize_google(audio)
        except sr.RequestError:
            reply('Sorry, my service is down. Please check your Internet connection.')
        except sr.UnknownValueError:
            print('Cannot recognize speech')
        return voice_data.lower()

def respond(voice_data):
    global file_exp_status, files, is_awake, path

    # Implement your logic for responding to voice commands here
    # You can use platform-specific handling as needed

# ------------------Driver Code--------------------

# Assuming you have a ChatBot class or module in the app module
# Here you should replace 'ChatBot' with the correct name if it's different
# Also, you should ensure that the ChatBot class or module is imported correctly
# and is accessible within the app module
if hasattr(app, 'ChatBot'):
    t1 = Thread(target=app.ChatBot.start)
    t1.start()

    # Lock main thread until Chatbot has started
    while not app.ChatBot.started:
        time.sleep(0.5)

    wish()
    voice_data = None
    while True:
        if app.ChatBot.isUserInput():
            # Take input from GUI
            voice_data = app.ChatBot.popUserInput()
        else:
            # Take input from Voice
            voice_data = record_audio()

        # Process voice_data
        if 'bob' in voice_data:
            try:
                # Handle sys.exit()
                respond(voice_data)
            except SystemExit:
                reply("Exit Successful")
                break
            except:
                # Some other exception got raised
                print("EXCEPTION raised while closing.") 
                break
else:
    print("Error: ChatBot class or module not found in the app module.")
