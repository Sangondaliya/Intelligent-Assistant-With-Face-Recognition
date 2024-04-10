## import library and files 
import threading
import FaceDetection
import voice
import time 
import sys
import collections
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk 
import cv2
import face_recognition
import os


## initializeing the haarcascade for face detection
current_path = os.getcwd()
face_cascade = cv2.CascadeClassifier(os.path.join(current_path,"models","haarcascade_frontalface_alt.xml"))

## taking the encoded face data 
(knowFaceName,knowFaceEncoder) = FaceDetection.EncodeFaceData()

## variable to track the face gone.
counter = 0


def FaceRecognition(label): 
    
    """
    this function is created to recognition the face.
    in this function we also get and set the face name.
    """
        
    global knowFaceEncoder, knowFaceName, face_cascade, counter

    
    ## initialize the haarcascade for face detection 
    
    ## take input from laptop camera
    cap = cv2.VideoCapture(0)



    ## created loop for continuous recognition 
    while 1 :
        
        ## check frame exist or not and do some preprocessing
        
        hasFrame, frame = cap.read()
        frame = cv2.flip(frame,1)
        frame2 = frame.copy()
        
        if hasFrame :
            
            ## Convert frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            ## detect faces from frame
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=11)


            ## check we have detect the face 
            if len(faces) >= 1:
                
                ## taking the first face form faces
                faces = faces[0]
                
                # taking the rectangle points 
                x,y,w,h = faces
                
                # print("dimentions are ",x,y,w,h)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # taking the face part from the frame  
                img = frame2[x-100 : x+w+100 , y - 100 : y+h+100 , :]
            
                try :
                    ## converting the BGR img to RGB Image
                    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                except Exception:
                    pass
                
                # Encode the image of face
                encodeImg = face_recognition.face_encodings(img)
                
                try :
                    encodeImg = encodeImg[0]
                
                except Exception:
                    pass
                
                matchs = []
                
                ## Compare encoded image to known encoded image 
                for knowImg in knowFaceEncoder:
                    # print("Start to compares faces")
                    try :
                        match = face_recognition.compare_faces([knowImg],encodeImg,tolerance=0.4)
                        matchs.extend(match)
                    
                    except Exception :
                        pass

                ## Check if we get match or not.
                try :
                    # collecting the true match
                    index = matchs.index(True)
                    # the index of the image and the the known name of the person
                    nameOfPerson = knowFaceName[index]
                    
                    # set the detected face name 
                    FaceDetection.ObjectName.setName =  nameOfPerson
                    
                    
                except Exception :
                    ## we dont recognize the person then we just set name as human
                    nameOfPerson = "Human"
                    FaceDetection.ObjectName.setName = nameOfPerson
                    
                
                ## put text on the frame
                cv2.putText(frame,nameOfPerson,(x-10, y-10),fontFace=cv2.FONT_HERSHEY_COMPLEX,fontScale=1,color=(0,255,0),thickness=2)
            
            else :
                ## if we dont get any faces then we just set the name as person gone                
                counter = counter + 1
                if counter > 3 :
                    FaceDetection.ObjectName.setName ="PersonGone"
                    counter = counter + 1
                
  
        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

        # Capture the latest frame and transform to image 
        captured_image = Image.fromarray(opencv_image) 
        captured_image = captured_image.resize((300,150))
        # Convert captured image to photoimage 
        photo_image = ImageTk.PhotoImage(image=captured_image) 
        # Configure image in the label 
        label.place(relx=0.65,rely=0.152,anchor='n')
        label.config(image=photo_image) 
        label.image = photo_image


## this flag is set to see the face recognition process start or not 
flag = False

def nameAndCommnunication(label):
    
    """
    this function is created for communication it take the konwn persone name and start communication
    the person.
    
    """
    
    ## taking the global parameters in use 
    global knowFaceName, flag
    
    print("Know face is : ",knowFaceName)
    
    ## this counter is used for reduce the false detection by puting the condition.
    counter = 0
    
    ## list of the faces detected
    faces = []
    
    ## loop for continuous match the face and communicate with the human
    while 1 :
        
        ## here we use the flag and we wait unitl the face process start and flag set to True
        if flag: 
            
            ## set the text to the user in main screen
            label.config(text = 'Waiting for you')
            time.sleep(1)
            
            ## getting the detected face and for some threshold we lopping here and after the 
            ## conformation the model start to communicate with the user  
            

            faceName = FaceDetection.getName()
            # print("face name is ",faceName) 
            if faceName == "NoPerson" or faceName =="PersonGone":
                continue
            else :
                faces.append(faceName)
                counter += 1
                       
            if (faceName in knowFaceName or faceName == "Human") and counter > 5 :
                # print(faces)
                faceName = collections.Counter(faces).most_common()[0][0]
                message = "communication start with " +faceName
                label.config(text = message)
                
                ## created the thread and start it for communicate with the user
                voiceThread = threading.Thread(target=voice.voiceMain,argss=(faceName,label))
                voiceThread.start()
                voiceThread.join()
                
                message = "communication Ends with " +faceName
                label.config(text = message)
                # voice2.voiceMain(faceName)
                counter = 0 
                faces = []
                
            else :
                pass
            
        else :
            break
        
        
## 
class Gif(tk.Label):
    
    """
    this class is created for the gui perpouse    
    
    """
    
    def __init__(self, master, path, delay=50):
        
        ## setting the path and other importante parameters
        
        self.path = path
        self.frames = []
        self.current_frame = 0
        self.delay = delay
        self.load_frames()
        first_frame = self.frames[0]
        self.image = first_frame
        super().__init__(master, image=self.image)
        self.pack()
        self.animate()


    def load_frames(self):
        """
        this function is used for loadding the frame.         
        """
        
        gif = Image.open(self.path)
        try:
            while True:
                gif.seek(len(self.frames))
                rezie_frame=gif.copy().resize((1000,750))
                rezie_frame=ImageTk.PhotoImage(rezie_frame)
                self.frames.append(rezie_frame)
        except EOFError:
            pass

    def animate(self):
        self.config(image=self.frames[self.current_frame])
        self.current_frame += 1
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.after(self.delay, self.animate)   
        
def main():
    """
   this is a main function which run face process and communication process
   in this function we declare the gui.  
    
    """
    ## the we use the flag variable which is declare above and when the face process start it set to 
    ## True otherwise it set the False.
    
    global flag
    
    ## initialize the window 
    window = Tk()
    
    ## set the title 
    window.title("Intelligent Assistant With Face Recognition")

    ## set the whole window size
    width= window.winfo_screenwidth()               
    height= window.winfo_screenheight()               
    window.geometry("%dx%d" % (width, height))
   

    # Path to your GIF files
    gif_path = os.path.join(current_path,"images","giphy.gif")
    animated_gif = Gif(window,gif_path)
    animated_gif.place(relx=0.6, rely=0.55, anchor=tk.CENTER)
    animated_gif.config(bg='black')
    
    face_frame = Label(window)
    face_frame.pack()
    
    ## set the college image in the window
    college_image = Image.open(os.path.join(current_path,"images","GITLOGO2.png"))
    college_image = ImageTk.PhotoImage(college_image)
    college_label=tk.Label(window,image=college_image)
    college_label.pack(anchor='nw',pady=10,padx=10)    
    
    ## set the kody image logo in the frame
    kody_image = Image.open(os.path.join(current_path,"images","kody.png"))
    kody_image=kody_image.resize((150,120))
    kody_image = ImageTk.PhotoImage(kody_image)
    kody_label=tk.Label(window,image=kody_image)
    kody_label.place(relx=0.64,rely=0.52,anchor='n')
    
    ## place communication label to show text in the screen 
    communication_label = Label(text="Communication")
    communication_label.place(relx=0.05,rely=0.6)
    communication_label.config(font=20,background='black',fg='white',justify='center',wraplength=300)
    
    ## created the two thread for our main two process one is face process and other one is communication 
    faceProcess = threading.Thread(target=FaceRecognition,args=(face_frame,))
    faceCommunication = threading.Thread(target=nameAndCommnunication,args=(communication_label,))

    ## start the face process and communication process
    faceProcess.start()
    if not faceProcess.is_alive():
        flag = False
        sys.exit()
    else :
        flag = True
    faceCommunication.start()
    
    
    window.config(bg='black')
    try : 
        window.mainloop()
        faceProcess.join()
    except Exception :
        sys.exit()
        
            
if __name__ =="__main__":
    ## function calling is done here
    main()