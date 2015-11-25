import csv


with open('donations.csv', mode = 'r') as into:
    reader = csv.reader(into)
    with open('donations_new.csv', mode = 'w') as out:
        writer = csv.writer(out)
        d = {rows[0]:rows[1] for rows in reader}

while True:
    q1 = input('Do you want to: 1) Send a Thank You, 2) Create a Report, or 3) Quit? > ')
    if q1 == 'Thank You':
        print(d)
    elif q1 == 'Report':
        print(d)
    elif q1 == 'Quit' or q1 == 'Exit':
        break
    else:
        continue
