## load the library and files

import nltk
from nltk.stem import WordNetLemmatizer
import json
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import random
import os
from keras.models import load_model

## load the model and other files 
current_path = os.getcwd()
model = load_model(os.path.join(current_path,"models","model.keras"))
intents = json.loads(open(os.path.join(current_path,"Data","data.json")).read())
words = pickle.load(open(os.path.join(current_path,"models","words.pkl"), 'rb'))
classes = pickle.load(open(os.path.join(current_path,"models","classes.pkl"), 'rb'))
# print(intents)
# print("words : ",words)

## initialize the lemmatizer which lammatize the out words
lemmatizer = WordNetLemmatizer()

def clean_up_sentence(sentence):
    """
    this functin is take the sentence and do preprocessig and return the list of words
    """
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def bow(sentence, words, show_details=True):
    """
    this function take the sentence and the words from word file
    """
    ## preprocess the sentence and taking the list of words
    sentence_words = clean_up_sentence(sentence)

    ## creating the bag of words
    bag = [0] * len(words)

    ## iterating to the list of the words and set 1 if it present in to the word file
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)

    ## return the list of words converted into numerical formate of 1 and 0.
    return np.array(bag) 


def predict_class(sentence, model):

    """
    this function is take sentence and preprocess it and pass it to the model 
    it predict the intent and return the intent 
    """
    
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    
    ## set the threshold for prediction intent
    ERROR_THRESHOLD = 0.60
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]    
    results.sort(key=lambda x: x[1], reverse=True)

    ## returning all the intent with there probability  
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
        
    ## return the intent list
    return return_list


def getResponse(ints, intents_json):
    """"
    take the intenst and return the random result as predicted output 
    """
    
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
        
    ## return the answer
    return result


def chatbot_response(msg):
    ## this is a function which is used by the other file it take the input questions and return the 
    ## genrated output
    
    ints = predict_class(msg, model)
    if len(ints) == 0 :
        res = "Sorry, i am still in learning face." 
    # print("ints : ", ints)
    res = getResponse(ints, intents)
    
    ## return the predicted output 
    return res
