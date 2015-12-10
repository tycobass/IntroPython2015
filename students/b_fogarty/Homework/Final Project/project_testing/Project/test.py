import requests
import json
import csv

#api call
action_table= requests.get('https://api.consumerfinance.gov:443/data/hmda/concept/action_taken.json')

lar = requests.get('https://api.consumerfinance.gov:443/data/hmda/slice/hmda_lar.json')
#decoding contents of drequest into pythonic data type, here, a dict

data = lar.json()

#isolating the table of interest, by name of dict I want. Here, a list of 100 dicts
dataset = data['results']

fieldnames = list(dataset[1].keys())
#writer = csv.DictWriter(dataset,delimiter=',',fieldnames=fieldnames)
#writer.writeheader()


#easy filters
filtered = []
for app in dataset:
    if app['agency_name'] == 'Consumer Financial Protection Bureau':
        filtered.append(app.values())

tocsv = dataset
keys = tocsv[0].keys()
with open('lar.csv','wb') as output:
    dict_writer = csv.DictWriter(output, keys)
    dict_writer.writeheader()
    dict_writer.writerows(tocsv)

with open(dataset,'rb') as f:
    reader = csv.writer(f,delimiter=' ',)
    reader.writerow()


writer = csv.writer(dataset)
writer.writerows()


for app in dataset:
    csv.DictWriter.writerow(app,dict)






#need to turn list of dicts into list of tuples, where each tuple is the value of a unique lar entry
[tuple(k.values()) for k in dataset]


import sqlite3
# open a connection to a db file:
conn = sqlite3.connect('example.db')
# create a cursor
c = conn.cursor()
c.execute("'CREATE TABLE tester {}'").format(fieldnames)
data_loader = [tuple(k.values()) for k in dataset]
q_string = '?,'*field_count
c.executemany('INSERT INTO stocks VALUES {}'.format(q_string), data_loader)
conn.commit()
# Close the cursor if we are done with it
c.close()
