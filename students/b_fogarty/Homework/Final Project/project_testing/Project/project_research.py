from os. path import abspath, dirname, join
import csv
import requests
import boto


#designate shape of dataset desired (slices)


#make api call
#dest = dirname(abspath(__file__))

req =requests.get('https://api.consumerfinance.gov:443/data/hmda/slice/hmda_lar?%24select=applicant_race_1%2Cavg(applicant_income_000s)&%24group=applicant_race_1&%24limit=10')
csv.register_dialect('commas',delimiter = ',')
read = csv.reader(req,dialect='commas')
for row in read:
    print(row)

# dialect still unknown
req =requests.get('https://api.consumerfinance.gov:443/data/hmda/slice/census_tracts')
read = csv.reader(req,'rb')
for row in read:
    print(row)


#https://api.consumerfinance.gov:443/data/hmda/concept/applicant_income_000s


#load data into memory


#transform data according to designations in step 1


#write data to csv's


#store in S3 file according to topic

"""
probably the end, but step 2 if i have time
"""

#load sheet from S3 into pandas dataframe and perform regression OLS analysis???