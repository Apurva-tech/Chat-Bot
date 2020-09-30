# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 21:27:18 2020

@author: apurva sharma
"""
import spacy

nlp = spacy.load('en_core_web_sm')

# Define included_entities
include_entities = ['DATE', 'ORG', 'PERSON']

# Define extract_entities()
def extract_entities(message):
    # Create a dict to hold the entities
    ents = dict.fromkeys(include_entities)
    # Create a spacy document
    doc = nlp(message)
    for ent in doc.ents:
        if ent.label_ in include_entities:
            # Save interesting entities
            ents[ent.label_] = ent.text
    return ents

print(extract_entities('she will graduate from VIT in 2023'))
print(extract_entities('people who graduated from MIT in 1999'))

### <--- Assigning roles using SpaCy Parser ---> ###

colors = ['black', 'red', 'blue']
items = ['shoes', 'handback', 'jacket', 'jeans']
def entity_type(word):
    _type = None
    if word.text in colors:
        _type = "color"
    elif word.text in items:
        _type = "item"
    return _type

# Create the document
doc = nlp("I want to wear blue jeans and sexy black shoes")

# Iterate over parents in parse tree until an item entity is found
def find_parent_item(word):
    # Iterate over the word's ancestors
    for parent in word.ancestors:
        # Check for an "item" entity
        if entity_type(parent) == "item":
            return parent.text
    return None

# For all color entities, find their parent item
def assign_colors(doc):
    # Iterate over the document
    for word in doc:
        # Check for "color" entities
        if entity_type(word) == "color":
            # Find the parent
            item =  find_parent_item(word)
            print("item: {0} has color : {1}".format(item, word))

# Assign the colors
assign_colors(doc)