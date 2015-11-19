import sys
from app import db
from fuzzywuzzy import fuzz
from models import Make, Model, Engine, Type, Transmission

# Global
inputs = list()

# Function to actually calculate similarity of strings and add to results list. 
# May have to call in two rounds, one for AND and another for OR, where I would either
# throw in all the search terms and try and find matches where each word is matched to a 
# specific higher ratio, or let a match happen if at least one term is matched.
# We must then make sure the OR list is after the AND list
# To the resulting list I am appending the json of a matching row, the ratio number, the 
# name of the column that caused a match, and the database model type
def check_match(row, class_type, and_results, or_results):
  and_accepted = True
  or_accepted = False
  columns = list()
  ratio = 0
  max_ratio = 0
  total_ratio = 0
  count = 0

  for entry in row:
    for word in inputs:
      ratio = fuzz.token_set_ratio(word, row[entry])
      if (ratio > 50):
        columns.append(entry) # to be hilighted later
        or_accepted = True
        total_ratio += ratio
        count += 1
        if ratio > max_ratio:
          max_ratio = ratio 
  if count != len(inputs):
    and_accepted = False
       
  if and_accepted:
    and_results.append({'type':class_type, 'ratio':total_ratio//count, 'columns': columns, 'row':row})
  elif or_accepted:
    or_results.append({'type':class_type, 'ratio':max_ratio, 'columns': columns, 'row':row})


# Sort results
def finalize_results(and_results, or_results):
  and_results = sorted(and_results, key = lambda k: k['ratio'], reverse=True)
  or_results = sorted(or_results, key = lambda k: k['ratio'], reverse=True)
  and_results[:0] = [(len(and_results))]
  for o in or_results:
    and_results.append(o)
  return and_results


# Print results
def print_results(results, model_type):
  print()
  print(model_type,'AND RESULTS')
  for r in range(1,results[0]+1):
    print('>>> :', results[r])
    print()

  print('--------------------')
  print(model_type,'OR RESULTS')
  for r in range(results[0]+1, len(results)):
    print('>>> :', results[r])
    print()


# Iterate over everything in every model of Models.py
def query(user_input):
  # Take in input concat into single string
  user_input = user_input.split()
  throw_away = ['and','or']
  for x in range(0, len(user_input)):
    if user_input[x].lower() not in throw_away:
      inputs.append(user_input[x].lower())

  make_and_results = list() 
  make_or_results = list()
  model_and_results = list() 
  model_or_results = list()
  engine_and_results = list() 
  engine_or_results = list()
  type_and_results = list() 
  type_or_results = list()
  transmission_and_results = list() 
  transmission_or_results = list()

  for x in Make.query.all():
    row = x.json
    check_match(row, 'Make', make_and_results, make_or_results)
  make_results = finalize_results(make_and_results, make_or_results)
  #print_results(make_results, 'Make')

  for x in Model.query.all():
    row = x.json
    check_match(row, 'Model', model_and_results, model_or_results)
  model_results = finalize_results(model_and_results, model_or_results)
  #print_results(model_results, 'Model')

  for x in Engine.query.all():
    row = x.json
    check_match(row, 'Engine', engine_and_results, engine_or_results)
  engine_results = finalize_results(engine_and_results, engine_or_results)
  #print_results(engine_results, 'Engine')

  for x in Type.query.all():
    row = x.json
    check_match(row, 'Type', type_and_results, type_or_results)
  type_results = finalize_results(type_and_results, type_or_results)
  #print_results(type_results, 'Type')

  for x in Transmission.query.all():
    row = x.json
    check_match(row, 'Transmission', transmission_and_results, transmission_or_results)
  transmission_results = finalize_results(transmission_and_results, transmission_or_results)
  #print_results(transmission_results, 'Transmission')

  return {'Make':make_results, 'Model':model_results, 'Engine':engine_results, 'Type':type_results, 'Transmission':transmission_results}


  
