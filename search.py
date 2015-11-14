import sys
from app import db
from fuzzywuzzy import fuzz
from models import Make, Model, Engine, Type, Transmission

# Take in input concat into single string
inputs = ''
for x in range(1, len(sys.argv)):
  inputs += (' '+sys.argv[x].lower())

results = list() # of dictionaries with entry id, type, matched elements, and rank. 


# Function to actually calculate similarity of strings and add to results list. 
# May have to call in two rounds, one for AND and another for OR, where I would either
# throw in all the search terms and try and find matches where each word is matched to a 
# specific higher ratio, or let a match happen if at least one term is matched.
# We must then make sure the OR list is after the AND list
# To the resulting list I am appending the json of a matching row, the ratio number, the 
# name of the column that caused a match, and the database model type
def check_match(row, class_type):
  accepted = False
  result = dict()
  match = ''
  ratio = 0
  for entry in row:
    ratio = fuzz.token_set_ratio(inputs, row[entry])
    if (ratio > 50):
      column = entry # to be hilighted later
      accepted = True
      break
  if accepted:
    results.append({'type':class_type, 'ratio':ratio, 'column': column, 'row':row})


# Iterate over everything in every model of Models.py
for x in Make.query.all():
  row = x.json
  check_match(row, 'Make')

for x in Model.query.all():
  row = x.json
  check_match(row, 'Model')

for x in Engine.query.all():
  row = x.json
  check_match(row, 'Engine')

for x in Type.query.all():
  row = x.json
  check_match(row, 'Type')

for x in Transmission.query.all():
  row = x.json
  check_match(row, 'Transmission')


# Sort results
final_results = sorted(results, key = lambda k: k['ratio'], reverse=True)
for r in final_results:
  print('>>> :', r)
  print()

  
