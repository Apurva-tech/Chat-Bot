# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 12:47:50 2020

@author: apurva sharma
"""

# Import sqlite3
import sqlite3

# Open connection to DB
conn = sqlite3.connect('hotels.db')

# Create a cursor
c = conn.cursor()

# Define area and price
area, price = "south", "hi"
t = (area, price)

# Execute the query
c.execute('SELECT * FROM hotels WHERE area=? AND price=?', t)

# Print the results
print(c.fetchall())

# Define find_hotels()
def find_hotels(params):
    # Create the base query
    query = 'SELECT * FROM hotels'
    # Add filter clauses for each of the parameters
    if len(params) > 0:
        filters = ["{}=?".format(k) for k in params]
        query += " WHERE " + " and ".join(filters)
    # Create the tuple of values
    t = tuple(params.values())
    
    # Open connection to DB
    conn = sqlite3.connect("hotels.db")
    # Create a cursor
    c = conn.cursor()
    # Execute the query
    c.execute(query, t)

    # Return the results
    return c.fetchall()
print(find_hotels({"area": "south", "price":"lo"}))


# Create the dictionary of column names and values
params = {
    "area":"south",
    "price":"lo"
}

# Find the hotels that match the parameters
print(find_hotels(params))

### <--- Create SQL with natural language ---> ###

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
# Define respond()
def respond(message):
    # Extract the entities
    entities = interpreter.parse(message)["entities"]
    # Initialize an empty params dictionary
    params = {}
    # Fill the dictionary with entities
    for ent in entities:
        params[ent["entity"]] = str(ent["value"])

    # Find hotels that match the dictionary
    results = find_hotels(params)
    # Get the names of the hotels and index of the response
    names = [r[0] for r in results]
    n = min(len(results),3)
    # Select the nth element of the responses array
    return responses[n].format(*names)
print(respond("I want an expensive hotel in the south of town"))


### <--- Refining your search ---> ###


# Define a respond function, taking the message and existing params as input
def respond(message, params):
    # Extract the entities
    entities = interpreter.parse(message)["entities"]
    # Fill the dictionary with entities
    for ent in entities:
        params[ent["entity"]] = str(ent["value"])

    # Find the hotels
    results = find_hotels(params)
    names = [r[0] for r in results]
    n = min(len(results), 3)
    # Return the appropriate response
    return responses[n].format(*names), params

# Initialize params dictionary
params = {}

# Pass the messages to the bot
for message in ["I want an expensive hotel", "in the north of town"]:
    print("USER: {}".format(message))
    response, params = respond(message, params)
    print("BOT: {}".format(response))