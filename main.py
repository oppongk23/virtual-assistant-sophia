
#Importing Dependencies and setting up environment the environment
import datetime
from email.message import EmailMessage
import pyttsx3
import speech_recognition as sr
import random
import wikipedia
import webbrowser
import os
import smtplib
from newsapi import NewsApiClient
from time import sleep
import pyaudio

from sendEmail import sendEmail

user = "Clifford"
assistant = "Sophia"


#Setting up the Sophia's speech 
engine = pyttsx3.init('nsss')
voices = engine.getProperty('voices') 
engine.setProperty("voice", "com.apple.speech.synthesis.voice.karen") 


#defining her speech function
def sophieSays(audio):
    engine.say(audio)
    engine.runAndWait() #this function blocks any other processes while it executes all the commands currently queued



#defining her greeting function
def greet():
    greeting = "Good Day"
    hour = int(datetime.datetime.now().hour)    #random.choice to randomuze the choice
    if (hour >= 0) and (hour<12):
        greeting = "Good morning"
    elif (hour >= 12) and (hour<17):
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    return greeting


#defining her listening function using the speech recognition library
def sophieListens():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #sophieSays("Go on, I'm listening")
        sophieSays("Go on, I'm listening")
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            print("Transcribing...")
            voice_data = r.recognize_google(audio, language="en-US")
            print(f"If I heard you right, you're saying {voice_data} \n")

            sophieSays(f"If I heard you right, you're saying {voice_data}, is that right? \n")
            if "yes" in voice_data.lower():
                return voice_data.lower()
            
            # elif "no" in voice_data.lower():
            #     return sophieListens()

        except "no" in voice_data.lower():
            sophieSays("Okay, please repeat what you said")
            return sophieListens()
        
        except sr.UnknownValueError:
            sophieSays(f"I'm sorry {user}, I didn't catch that quite well.")
            #sophieListens()
            return sophieListens()
        
        except sr.RequestError:
            sophieSays(f"Sorry {user}, I'm having trouble with the connection.")
            return None

        return voice_data.lower()



#definiing a function that processses the inputs 
def processQuery(query=None):
    """This part takes the query and analyzes the basic queries to perform simple functions.
    """
    # if query is None:
    #     sophieSays(f"There is nothing for me to say")
    # Searching on Wikipedia
    if 'wikipedia' in query:  
        sophieSays(f"I'm searching Wikipedia...")
        query = query.replace("wikipedia", "") #Removing wikipedia from the queries
        results = wikipedia.summary(query, sentences=5)
        print(results)
        sophieSays(f"According to Wikipedia, {results}")

    if "youtube" in query:
        webbrowser.open_new_tab("http://youtube.com")

    elif "google" in query:
        webbrowser.open_new_tab("http://google.com")

    elif "the time" in query:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        sophieSays(f"The time is {current_time} ")

    elif "email" in query:
        mail_package = {}
        sophieSays("Please type in the name of the recipient")
        mail_package["recipient_name"] = str(input())

        sophieSays("What is the subject of the email?")
        raw_subject = sophieListens()
        word_list = raw_subject.split(" ")
        word_list = [word.capitalize() for word in word_list]
        mail_package["Subject"] = " ".join(word_list)

        sophieSays("What do you want me to say?")
        mail_package["content"] = sophieListens()

        sophieSays("Okay, sending the email. I will let you know when it is done!")
        sophieSays(sendEmail(mail_package))




    

if __name__ == "__main__":
    greetme = greet()
    sophieSays(f"Hello {user}, {greetme}. my name is {assistant}. How can I help you today?")
    query = sophieListens()
    processQuery(query)




