import pyttsx3 

def SpeakText(command):
	
	"""
	this function is created to convert text into speech 
	
	"""
	engine = pyttsx3.init()
	engine.setProperty("rate",180)
	engine.say(command) 
	engine.runAndWait()