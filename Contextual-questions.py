# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 17:01:08 2020

@author: apurva sharma
"""

### <--- Contextual Questions ---> ###

# Define the states
INIT=0 
CHOOSE_COFFEE=1
ORDERED=2

def interpret(message):
    msg = message.lower()
    if 'order' in msg:
        return 'order'
    if 'kenyan' in msg or 'colombian' in msg:
        return 'specify_coffee'
    if 'what' in msg:
        return 'ask_explanation'
    return 'none'

def respond(state, message):
    (new_state, response) = policy_rules[(state, interpret(message))]
    return new_state, response

# Define the policy rules dictionary
policy_rules = {
    (INIT, "ask_explanation"): (INIT, "I'm a bot to help you order coffee beans"),
    (INIT, "order"): (CHOOSE_COFFEE, "ok, Colombian or Kenyan?"),
    (CHOOSE_COFFEE, "specify_coffee"): (ORDERED, "perfect, the beans are on their way!"),
    (CHOOSE_COFFEE, "ask_explanation"): (CHOOSE_COFFEE, "We have two kinds of coffee beans - the Kenyan ones make a slightly sweeter coffee, and cost $6. The Brazilian beans make a nutty coffee and cost $5.")    
}
def send_message(state, message):
    print("USER : {}".format(message))
    new_state, response = respond(state, message)
    print("BOT : {}".format(response))
    return new_state
# Define send_messages()
def send_messages(messages):
    state = INIT
    for msg in messages:
        state = send_message(state, msg)

# Send the messages
send_messages([
    "can you help me?",
    "well then I'd like to order some coffee",
    "what do you mean by that?",
    "kenyan"
])