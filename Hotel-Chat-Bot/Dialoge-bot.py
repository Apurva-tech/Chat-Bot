# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 17:57:36 2020

@author: apurva sharma
"""

import sqlite3

# Open connection to DB
conn = sqlite3.connect('hotels.db')

# Create a cursor
c = conn.cursor()

# Import necessary modules
from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer

# Create args dictionary
args = {"pipeline" : "spacy_sklearn"}

# Create a configuration and trainer
config = RasaNLUConfig(cmdline_args = args)
trainer = Trainer(config)

# Load the training data
training_data = load_data("./training_data.json")

# Create an interpreter by training the model
interpreter = trainer.train(training_data)

'''# Test the interpreter
print(interpreter.parse("I'm looking for a Mexican restaurant in the North of town"))'''

responses = ["I'm sorry :( I couldn't find anything like that",
 '{} is a great hotel!',
 '{} or {} would work!',
 '{} is one option, but I know others too :)']

def find_hotels(params, excluded):
    query = 'SELECT * FROM hotels'
    if len(params) > 0:
        filters = ["{}=?".format(k) for k in params] + ["name!='?'".format(k) for k in excluded] 
        query += " WHERE " + " and ".join(filters)
    t = tuple(params.values())
    
    # open connection to DB
    conn = sqlite3.connect('hotels.db')
    # create a cursor
    c = conn.cursor()
    c.execute(query, t)
    return c.fetchall()

def interpret(message):
    data = interpreter.parse(message)
    if 'no' in message:
        data["intent"]["name"] = "deny"
    return data

# Define respond()
def respond(message, params, prev_suggestions, excluded):
    # Interpret the message
    parse_data = interpret(message)
    # Extract the intent
    intent = parse_data["intent"]["name"]
    # Extract the entities
    entities = parse_data["entities"]
    # Add the suggestion to the excluded list if intent is "deny"
    if intent == "deny":
        excluded.extend(prev_suggestions)
    # Fill the dictionary with entities	
    for ent in entities:
        params[ent["entity"]] = str(ent["value"])
    # Find matching hotels
    results = [
        r 
        for r in find_hotels(params, excluded) 
        if r[0] not in excluded
    ]
    # Extract the suggestions
    names = [r[0] for r in results]
    n = min(len(results), 3)
    suggestions = names[:2]
    return responses[n].format(*names), params, suggestions, excluded

# Initialize the empty dictionary and lists
params, suggestions, excluded = {}, [], []

# Send the messages
for message in ["I want a mid range hotel", "no that doesn't work for me"]:
    print("USER: {}".format(message))
    response, params, suggestions, excluded = respond(message, params, suggestions, excluded)
    print("BOT: {}".format(response))