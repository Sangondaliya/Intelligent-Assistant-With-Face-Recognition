## load the library and files
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import face_recognition


class setAndGetName:
    
    """
    this class is created for set and get the current person name.
    
    """
    
    def __init__(self):
        self.name = "NoPerson"
    
    ## this is used for get the current person on the frame
    @property
    def getName(self):
        # time.sleep(2)
        return self.name
    
    ## this is used for set the name of the person
    @getName.setter
    def setName(self,newName):
        self.name = newName
    
## created the one object 
ObjectName = setAndGetName()


def EncodeFaceData():
    
    """
    enocde face data which is used as training data set. 
    return face encoded data and person name.
    """


    ## Variables for known face encoder and there name 
    knowFaceEncoder = []
    knowFaceName = []

    ## take pata from the disk
    currentPath = os.getcwd()
    listpath = currentPath + "\FaceData"

    ## get the list of picture. it use as train data
    listOfPicture = os.listdir(listpath)

    ## taking name of person and there face data from the list of picture
    for i in range(len(listOfPicture)):
        name = listOfPicture[i].split(".")[0]
        knowFaceName.append(name)
        fileName = "FaceData/" + listOfPicture[i]
        img = face_recognition.load_image_file(fileName)
        faceEncoding = face_recognition.face_encodings(img)[0]
        knowFaceEncoder.append(faceEncoding)
        
    # print(knowFaceName)
    # print(knowFaceEncoder)
    
    ## return knowFaceName, and there Enoceding
    return (knowFaceName,knowFaceEncoder)

## this function just return the name of the person
def getName():
    return ObjectName.getName
