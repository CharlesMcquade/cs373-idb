import sys
from app import db
from fuzzywuzzy import fuzz
from models import Make, Model, Engine, Type, Transmission

# Take in input concat into single string
inputs = list()
throw_away = ['and','or']
for x in range(1, len(sys.argv)):
  if sys.argv[x].lower() not in throw_away:
    inputs.append(' '+sys.argv[x].lower())

and_results = list() # of dictionaries with type, matched elements, and rank. 
or_results = list()

# Function to actually calculate similarity of strings and add to results list. 
# May have to call in two rounds, one for AND and another for OR, where I would either
# throw in all the search terms and try and find matches where each word is matched to a 
# specific higher ratio, or let a match happen if at least one term is matched.
# We must then make sure the OR list is after the AND list
# To the resulting list I am appending the json of a matching row, the ratio number, the 
# name of the column that caused a match, and the database model type
def check_match(row, class_type):
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
and_results = sorted(and_results, key = lambda k: k['ratio'], reverse=True)
or_results = sorted(or_results, key = lambda k: k['ratio'], reverse=True)

print('AND RESULTS')
for r in and_results:
  print('>>> :', r)
  print()

print('--------------------')
print('OR RESULTS')
for r in or_results:
  print('>>> :', r)
  print()

  
