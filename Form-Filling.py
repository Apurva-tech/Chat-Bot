# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 16:38:59 2020

@author: apurva sharma
"""

def interpret(message):
    msg = message.lower()
    if 'order' in msg:
        return 'order'
    if 'kenyan' in msg or 'colombian' in msg:
        return 'specify_coffee'
    return 'none'

def respond(policy, state, message):
    (new_state, response) = policy[(state, interpret(message))]
    return new_state, response

def send_message(policy, state, message):
    print("USER : {}".format(message))
    new_state, response = respond(policy, state, message)
    print("BOT : {}".format(response))
    return new_state

# Define the INIT state
INIT = 0

# Define the CHOOSE_COFFEE state
CHOOSE_COFFEE = 1

# Define the ORDERED state
ORDERED = 2

# Define the policy rules
policy = {
    (INIT, "order"): (CHOOSE_COFFEE, "ok, Colombian or Kenyan?"),
    (INIT, "none"): (INIT, "I'm sorry - I'm not sure how to help you"),
    (CHOOSE_COFFEE, "specify_coffee"): (ORDERED, "perfect, the beans are on their way!"),
    (CHOOSE_COFFEE, "none"): (CHOOSE_COFFEE, "I'm sorry - would you like Colombian or Kenyan?"),
}

# Create the list of messages
messages = [
    #"I am Apurva",
    "I'd like to become a professional dancer",
    "well then I'd like to order some coffee",
    "my favourite animal is a zebra",
    "kenyan"
]

# Call send_message() for each message
state = INIT
for message in messages:    
    state = send_message(policy, state, message)
    
