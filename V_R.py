import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import webbrowser


def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.setProperty('rate', 100)  # Speed percent (can go over 100)
    speak_engine.setProperty('volume', 4.0)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="en-GB").lower()
        print("[log] You might say: "+voice)

        if voice.startswith(opts["alias"]):
            cmd = voice

            for x in opts["alias"]:
                cmd = cmd.replace(x, "").strip()
            for x in opts["tbr"]:
                cmd = cmd.replace(x, "").strip()

            cmd = recognizer_cmd(cmd)
            execute_cmd(cmd['cmd'])
    except sr.UnknownValueError:
        print("Your voice wasn't be recognised")
    except sr.RequestError as e:
        print("Check out your Internet connection!")


def recognizer_cmd(cmd):
    RC = {"cmd": "", "percent": 0}
    for c, v in opts["cmds"].items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC["percent"]:
                RC["cmd"] = c
                RC["percent"] = vrt
    return RC


def execute_cmd(cmd):
    if cmd == "timee":
        #due to time
        now = datetime.datetime.now()
        speak("Now " + str(now.hour) + " : " + str(now.minute))
    elif cmd == "music":
        webbrowser.open("https://music.youtube.com/watch?v=yuJxfA9mtS0&list=PLYQU-aDokMXeXsYte-JJg7WEQd10GVT-l")
    elif cmd == "kek":
        speak("Now, I don't know any of keks")
    elif cmd == "google":
        webbrowser.open("https://www.google.com.ua")
    else:
        speak("I don't know this command")


opts = {
    "alias": ("george", "kek", "my lover", "dude", " YAY", "gay", "okay", "okc", "hey siri", "siri"),
    "tbr": ("tell", "say", "speak", "describe", "what", "how", "what's"),
    "cmds": {
        "timee": ("current time", " our time", "time", ' what time is it', "say time", "daytime"),
        "music": ("turn on music", " turn the music", " on the music", "turn on the radio"),
        "kek": ("say bad joke", "say cool joke", "tell me please the joke", "kek me please"),
        "google": ("open the Google", "Find in Google", "Look through google")
    }

}

r = sr.Recognizer()
m = sr.Microphone(device_index=1)
with m as source:
     r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

voices = speak_engine.getProperty("voices")
speak_engine.setProperty('voice', voices[2].id)

speak("Hello my Queen")
speak("Your kek is listening")

stop_listening = r.listen_in_background(m, callback)
while True:
    time.sleep(0.1)
