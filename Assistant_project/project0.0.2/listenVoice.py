## load the library and files

import speech_recognition as sr
import requests
import whisper
import say
import time
## flag is ussed for check the internet is connected or not according to that we are going to 
## use the speech to text model.
flag = 0

global voice_listen
voice_listen=False

def is_connected():
    
    """
    this function used for checking the internet connectivity.
    in this function we are requesting to the google home page and if we get response then we return True 
    otherwise return False
    """
    
    try:
        response = requests.get("http://www.google.com", timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False

    except Exception as e:
        print(e)
        return False


def capture_voice_input(label):
    """
    this function is actuale going to do speech to text and return that text
    """
    flag = is_connected()

    # print("Internet checked at ", (time.time()-start))
    recognizer = sr.Recognizer()

    global voice_listen
    voice_listen=True

    with sr.Microphone() as source :
        ## set the label to show now we are listening
        label.config(text = "Listening...")
        audio = recognizer.listen(source,phrase_time_limit=4)

    try:
        if flag:
            
            text = recognizer.recognize_google(audio,language="english")
        else:
            # print("No internet connection.")
            text = recognizer.recognize_whisper(audio, model="base")

    except sr.UnknownValueError:
        # say.SpeakText("Sorry, I didn't understand that.")
        text = ""
    # print("Sorry, I didn't understand that.")
    
    except sr.RequestError as e:
        text = ""
        # print("Error; {0}".format(e))
    
    except Exception:
        text = ""

    ## return the text getting from person side
    return text