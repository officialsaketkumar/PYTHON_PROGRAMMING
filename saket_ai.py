import os
import pygame
import speech_recognition as sr
import asyncio
import edge_tts
import time
import webbrowser
from datetime import datetime

pygame.mixer.init()
WAKE_WORD = "saket"
SUPER_MODE = False
LAST_COMMAND = ""
recognizer = sr.Recognizer()
mic = sr.Microphone()



def normalize(text):
    fixes = {
        "you tube": "youtube",
        "u tube": "youtube",
        "insta gram": "instagram",
        "dot com": "",
        "open up": "open",
    }
    for k, v in fixes.items():
        text = text.replace(k, v)
    return text


def speak(text):
    print("🗣️ SPEAK:", text)
    filename = f"voice_{int(time.time()*1000)}.mp3"
    communicate = edge_tts.Communicate(text, "en-IN-NeerjaNeural")
    async def gen():
        await communicate.save(filename)
    asyncio.run(gen())
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove(filename)


def save_history(action):
    with open("history.txt", "a") as f:
        f.write(f"{datetime.now()} -> {action}\n")


def listen():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.4)
        print("🎤 Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio).lower()
        text = normalize(text)
        print("HEARD:", text)
        return text
    except:
        return ""



def open_site(site):
    site = site.replace(" ", "")
    speak(f"Opening {site}")
    webbrowser.open(f"https://{site}.com")
    save_history(f"Opened {site}")



def super_mode_command(query):
    print("🔥 SUPER MODE:", query)
    if "open" in query:
        site = query.replace("open", "").strip()
        open_site(site)
    elif "github" in query:
        q = query.replace("github", "").strip()
        speak(f"Searching GitHub for {q}")
        webbrowser.open(f"https://github.com/search?q={q}")
        save_history(f"GitHub search: {q}")
    else:
        speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        save_history(f"Google search: {query}")


def normal_command(cmd):
    print("🟢 NORMAL MODE:", cmd)
    if "youtube" in cmd:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
        save_history("Opened YouTube")
    elif "instagram" in cmd or "insta" in cmd:
        speak("Opening Instagram")
        webbrowser.open("https://instagram.com")
        save_history("Opened Instagram")
    elif "linkedin" in cmd:
        open_site("linkedin")
    elif "github" in cmd:
        open_site("github")
    elif "chrome" in cmd:
        speak("Opening Chrome")
        os.startfile("chrome")
        save_history("Opened Chrome")
    elif "notepad" in cmd:
        speak("Opening Notepad")
        os.startfile("notepad")
        save_history("Opened Notepad")
    elif "calculator" in cmd or "calc" in cmd:
        speak("Opening Calculator")
        os.startfile("calc")
        save_history("Opened Calculator")
    elif cmd.startswith("play"):
        song = cmd.replace("play", "").strip()
        speak(f"Playing {song}")
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
        save_history(f"Played song: {song}")
    elif "exit" in cmd or "quit" in cmd:
        speak("Goodbye bro")
        save_history("Assistant exited")
        exit()
    else:
        speak("Command not recognized")
speak("Saket AI assistant is online")
while True:
    text = listen()
    if not text:
        continue
    if "activate super saket" in text:
        SUPER_MODE = True
        speak("Super Saket activated")
        save_history("Super mode ON")
        continue
    if "deactivate super saket" in text:
        SUPER_MODE = False
        speak("Super Saket deactivated")
        save_history("Super mode OFF")
        continue
    if SUPER_MODE:
        super_mode_command(text)
        continue
    if WAKE_WORD in text:
        cmd = text.split(WAKE_WORD, 1)[1].strip()
        if cmd:
            normal_command(cmd)
