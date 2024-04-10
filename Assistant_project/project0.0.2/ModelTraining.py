## load the library and files
import nltk
from nltk.stem import WordNetLemmatizer
import json
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import os
import random
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

## taking the current path 
current_path = os.getcwd()

## lemmatizer for convert word into base word
lemmatizer = WordNetLemmatizer()

## unique words
words = []

## unique tags
classes = []

## pattern, tag
documents = []

## ignore words
ignore_words = ['?', '!']

## load data from file
data_file = open(os.path.join(current_path,"Data",'data.json')).read()
intents = json.loads(data_file)

for intent in intents['intents']:
    
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)    
        ## document contain the words of list and there tag
        documents.append((w, intent['tag']))
        if intent['tag'] not in classes:
            ## class is for all the unique tags
            classes.append(intent['tag'])

## preprocss the words 
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
## sort the words and class
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

## save unique words 

pickle.dump(words, open(os.path.join(current_path,"models","words.pkl"), 'wb'))
## save all tags
pickle.dump(classes, open(os.path.join(current_path,"models","classes.pkl"), 'wb'))

# create our training data
training = []
# create an empty array for our output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # lemmatize each word - create base word, in attempt to represent related words
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    # create our bag of words array with 1, if word match found in current pattern
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # output is a '0' for each tag and '1' for current tag (for each pattern)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])
 
## create the training data    
train_x = []
train_y = []

for i in training:
    train_x.append(i[0])
    train_y.append(i[1])
    
# Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
# equal to number of intents to predict output intent with softmax
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))
    
## Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

## fitting and saving the mode
hist = model.fit(np.array(train_x), np.array(train_y), epochs=150, batch_size=5, verbose=1)
## save the model
model.save(os.path.join(current_path,"models","model.keras"))