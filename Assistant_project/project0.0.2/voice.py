## load the library and files
import listenVoice
import ModelPrediction
import say
import whisper
import FaceDetection

## Load the whisper base model for offline communication.
whisper.load_model("base")

## Created dict for remember user 
face_lifetime={}

## Core Voice communication function
def voiceMain(nameOfPerson,label):
    label = label
    """
    this function is created for communication with user.
    it take input face name and label
    here label is used for show the communication step in the main window
    """

    ## set the face name 
    faceName = nameOfPerson
    
    ## this counter is used for track if user is not speeck 2 time then it terminate
    counter  = 0
    counterForPerson = 0 
    great = True
    
    ## looping for constant communication and track the person
    while(1):
        
        ## this name is taken for just verify the user is same or not
        name = FaceDetection.getName()
        # print("the name detected is ",name)
        # print("the name we gat is ",faceName)
        
        ## write some logic for set greet and say bye to the person
        
        if faceName != name :
            counterForPerson += 1
            pass
        
        else :
            counterForPerson = 0
            
        if counterForPerson >= 2 :
            say.SpeakText('Come back soon! ' + faceName)
            great = True
            break


        if great  and faceName != "Human":
            
            if faceName not in face_lifetime.keys():
                face_lifetime[faceName] = 0
                say.SpeakText('welcome ' + faceName)
                great = False 
                
            elif faceName in face_lifetime.keys():
                
                say.SpeakText('welcome back' + faceName)
                great = False 
                    
        elif  great  and faceName == "Human" :
            say.SpeakText('Welcome Human')
            great = False 
        
        
        ## this variable used for model generated output 
        ans = ""
        

        ## capturing the person input        
        text = listenVoice.capture_voice_input(label)
        ## show the person text in the screen
        label.config(text = "User : " + text)

        ## pass text to the model and made some logic if text is getting blank
        
        if text =="":
            counter = counter + 1
            if counter > 5 :
                say.SpeakText("i dont get anything now i am turning off.")
                break
            else :
                say.SpeakText(f"speack something {faceName}.")
                continue        
        
        if text.lower() in ["good morning","good night","good afternoon","good evening"]:
            if text.lower() != "good night":
                say.SpeakText(text + " "+ faceName)
                continue
            else :
                say.SpeakText(text + " "+ faceName)
                break
       
        
        ## getting the model output
        ans = ModelPrediction.chatbot_response(text)
        counter = 0
        # print("model output ",ans)
        
        ## pass the model output to the model which convert this text into speech.
        say.SpeakText(ans)
        if ans in  ["Sad to see you go :(","Talk to you later","Goodbye!","Come back soon!"]:
            break

