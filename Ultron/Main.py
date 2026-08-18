from gtts import gTTS
from openai import OpenAI
import speech_recognition, datetime, webbrowser, pyttsx3, WebLink, requests, pygame, os

engine = pyttsx3.init() 
engine.setProperty("rate", 175)

recognizer = speech_recognition.Recognizer()
microphone = speech_recognition.Microphone()

newsapi = "1cb38688b83b4ce69c2bdf948a9eee10"
openai_api_key = "<Your OpenAI API Key>"

def aiprocess(command):
    client = OpenAI(api_key=openai_api_key)
    completion = client.chat.completions.create(
      model="gpt-5.5",
      messages=[
        {"role": "system", "content": "You are a virtual assistant named Ultron skilled in general tasks like Alexa and Google Cloud"},
        {"role": "user", "content": command}
      ]
    )
    return completion.choices[0].message.content

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def openWebsite(site):
    try:
        link = WebLink.website[site]
        speak(f"opening {site}")
        webbrowser.open(link)

    except Exception as e:
        print(e)

def playSong(song):
    try:
        link = WebLink.music[song]
        speak(f"playing song {song}")
        webbrowser.open(link)

    except Exception as e:
        print(e)

def processCommand(c):

    if c.lower().startswith("open"):

        if (c.lower().split(" ")[0] == "open" and len(c.lower().split(" ")) == 1):

            for site in WebLink.website:
                print(f"{site}: {WebLink.website[site]}")

            print("Please enter the website name:")
            speak("Please enter the website name")
            site = input()
            openWebsite(site)

        site = c.lower().split(" ")[1]
        openWebsite(site)

    elif c.lower().startswith("play song"):

        if (c.lower().split(" ")[0] == "play" and c.lower().split(" ")[1] == "song" and len(c.lower().split(" ")) == 2):

            for song in WebLink.music:
                print(f"{song}: {WebLink.music[song]}")

            print("Please enter the song number:")
            speak("Please enter the song number")
            song = input()
            playSong(song)

        song = c.lower().split(" ")[2]
        playSong(song)

    elif c.lower().startswith("search"):
        query = c.lower().split(" ")[1:]
        speak(f"Searching {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif c.lower().startswith("notepad"):
        speak("Opening Notepad")
        os.system("notepad")

    elif c.lower().startswith("current time"):
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")

    elif c.lower().startswith("today's news"):
        r = requests.get(f"https://newsapi.org/v2/everything?q=tesla&from=2026-07-05&sortBy=publishedAt&apiKey={newsapi}")

        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            speak("Here are the top 5 news articles:")
            for article in articles[:5]:

                try:
                    speak(article['title'])

                except Exception as e:
                    print(e)

    elif c.lower().startswith("exit") or c.lower().startswith("stop"):
        speak("Goodbye!")
        exit()

    else:
        try:
            response = aiprocess(c)
            speak(response)

        except Exception as e:
            print(e)
            speak("I heard you, but I don't know that command yet.")            

if __name__ == "__main__":
    print("Initializing Ultron")
    speak("Initializing Ultron")

    while True:
        try:

            with microphone as source:
                    print("Listening for activation word [Ultron]")
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source)
                    word = recognizer.recognize_google(audio)
                    print("You said:", word)

            if(word.lower() == "ultron"):
                speak("Ya")

                with microphone as source:
                            print("Ultron Active")
                            recognizer.adjust_for_ambient_noise(source, duration=1)
                            speak("Speak Now")
                            audio = recognizer.listen(source)
                            command = recognizer.recognize_google(audio)
                            print("You said:", command)
                            processCommand(command)
        
        except Exception as e:
            print(e)