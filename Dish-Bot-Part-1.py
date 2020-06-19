# Description:- This is the DishBot program that gets the date, current time, responds to greetings and solves
# problems of customer.

# Using pyaudio
# Using SpeechRecognition
# Using gTTS
# Using wikipedia

# Importing libraries

import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import random
import wikipedia
import calendar


# Ignoring the warnings/warning messages that we get in the program
warnings.filterwarnings('ignore')


# Audio (user)
def recordAudio():

    # Record Audio

    r = sr.Recognizer()

    # Switch on microphone and start recording

    with sr.Microphone() as source :
        print('Say Something!')
        audio = r.listen(source)
    
    
    # Using gTTS

    data =  ''
    try:
        data = r.recognize_google(audio)
        print('You said : '+data)
    except sr.UnknownValueError:
        print('Google Speech Recognition could not understand the audio, unknown error')
    except sr.RequestError as e :
        print('Request results from Google Speech Recognition service error' + e)
        
    return data

# Response of DishBot
def assistantResponse(text):
    print(text)
    
    # Program to convert text into speech
    myobj = gTTS(text = text, lang = 'en', slow = False)
    
    # Save the converted Audio to a file 
    myobj.save('dishbot_response.mp3')
    
    # Play the converted file
    os.system('start dishbot_response.mp3')

# A function for wake word

def wakeword(text):
    WAKE_WORDS = ['hey dish', 'okay dish', 'dish']

    text = text.lower() #because the words are in lower case 
    
    #Check to see if the users command contains a wake word
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True
        
    return False  # If the wake word is not found in the group

# Get the current date
def getDate():
    
    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]
    monthNum = now.month
    dayNum = now.day
    
    # List of months
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                   'September', 'October', 'November', 'December']
    
    # List of numbers
    Numbers = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', 
               '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', 
               '28th', '29th', '30th', '31th' ]
    return 'Today is '+weekday+' '+ month_names[monthNum - 1]+' '+Numbers[dayNum - 1]+' '


# Greetings
def greeting(text):
    
    # Input
    Greeting_Input = ['hi', 'hello', 'hola', 'greetings', 'namaste', 'hey']
    
    # Response
    Greeting_Response = ['hello', 'namaste', 'hi there']
    
    # For greetings choose randomly
    
    for word in text.split():
        if word.lower() in Greeting_Input:
            return random.choice(Greeting_Response) + '!'
    
    # No greetings
    return ''

# Function to get first and last name  from text
def getPerson(text):
    
    wordList = text.split() # Splitting text into list of words
    
    for i in range(0, len(wordList)):
        if i + 3 <= len(wordList) - 1 and wordList[i].lower() == 'who' and wordList[i+1].lower() == 'is':
            return wordList[i+2] + ' ' + wordList[i + 3]
        
# For the constant run of DishBot        
while True:
    
    # Record audio
    text = recordAudio()
    response = ''
    
    # Check for wake word
    if (wakeword(text) == True):
        # Check for greetings
        response = response + greeting(text)
        
        # Check for if dates was asked
        if ('date' in text):
            get_date = getDate()
            response = response + ' ' + get_date
            
        # Check if user said time
        if('time' in text):
            now = datetime.datetime.now()
            meridian = ''
            if now.hour >=12:
                meridian = 'p.m'
                hour = now.hour - 12
            else:
                meridian = 'a.m'
                hour = now.hour
                
            # Convert minute into string
            if now.minute < 10:
                minute = '0' + str(now.minute)
            else:
                minute = str(now.minute)
            
            
            response = response +' '+'It is '+str(hour)+ ':' + minute + ' ' + meridian+' '
        
        # Check if user said 'who is'
        if ('who is' in text):
            person = getPerson(text)
            wiki = wikipedia.summary(person, sentences=2)
            response = response + ' ' + wiki
            
            
            
        # DishBot response with audio
        assistantResponse(response)
        