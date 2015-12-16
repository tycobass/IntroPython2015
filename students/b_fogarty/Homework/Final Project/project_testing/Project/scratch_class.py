import requests
import json
import csv
import sqlite3
import pandas as pd
import numpy as np
from boto.s3.connection import S3Connection


#class intel_builder(object):

    #dest = dirname(abspath(__file__))

    #def __init__(self, state = 'Massachusetts', input_file = None):

        """
        Returns a class for building new database tables with transformed
        data of interest
        """
    #store parameters

    # build API call strings

    #def api_scrape(self, input_seq):
        """
        Executes get command against CFPB HMDA API, pulling table into memory
        (maybe csv?)
        """

        #api call
        base_url = 'https://api.consumerfinance.gov:443/data/hmda/'
        #action_table= requests.get('https://api.consumerfinance.gov:443/data/hmda/concept/action_taken.json')
        lar = requests.get(base_url + 'slice/hmda_lar.json')

        lar = requests.get('https://api.consumerfinance.gov/data/hmda/slice/hmda_lar.json?%24select=action_taken_name%2Capplicant_ethnicity_name%2Capplicant_income_000s%2Capplicant_race_name_1%2Capplicant_sex_name%2Cas_of_year%2Ccensus_tract_number%2Cdenial_reason_name_1%2Cdenial_reason_name_2%2Choepa_status_name%2Chud_median_family_income%2Clien_status_name%2C%09loan_amount_000s%2C%09msamd_name%2C%09number_of_1_to_4_family_units%2Cnumber_of_owner_occupied_units%2Cpopulation%2Cpreapproval_name%2Crespondent_id%2Csequence_number%2Cstate_abbr%2Cstate_name%2Ctract_to_msamd_income&%24where=loan_purpose_name%3D%27Home+purchase%27+AND+applicant_income_000s+%3C+100+AND+state_abbr+%3D+%27MA%27+AND+property_type_name+%3D+%27One-to-four+family+dwelling+%28other+than+manufactured+housing%29%27+AND+owner_occupancy_name+%3D+%27Owner-occupied+as+a+principal+dwelling%27+&%24group=&%24orderBy=&%24limit=1000&%24offset=0&%24format=json')

        #decoding contents of drequest into pythonic data type, here, a dict
        data = lar.json()

        #isolating the table of interest, by name of dict I want. Here, a list of 100 dicts
        dataset = data['results']
        fieldnames = list(dataset[1].keys())
        field_count = len(fieldnames)
        valuetypes = [type(i) for i in dataset[1].values()]
        # getting keys for DDL
        all_keys = list()
        for i in dataset:
            all_keys.append(i.keys())
        unique_keys = set(i for x in all_keys for i in x)

    def clean_data(self, dataset):
        """
        Cleans up the dataset to match desired shape of end user
        aggregations on geographic area, mainly...maybe the reformatting of some fields
        """
        frame = pd.DataFrame(dataset)
    #Calculating relative fields
        frame['income_to_median'] = (frame['applicant_income_000s']*1000)/frame['hud_median_family_income']
        frame['loan_to_income'] = frame['loan_amount_000s']/frame['applicant_income_000s']
    #mapping loan decision
        decision_map = {
            'Application approved but not accepted': 'Approved',
            'Loan originated': 'Approved',
            'Application withdrawn by applicant': 'Other',
            'Application denied by financial institution': 'Denied',
            'File closed for incompleteness': 'Other',
            'Loan purchased by the institution': 'Approved',
            'Preapproval request denied by financial institution': 'Denied'
        }
        frame['simplified_decision'] = frame['action_taken_name'].map(str.lower).map(decision_map)
    #mapping HOEPA
        hoepa_map = {
            'Not a HOEPA loan': 0
            'HOEPA loan': 1
        }
        frame['simplified_hoepa'] = frame['hoepa_status_name'].map(str.lower).map(decision_map)
    #binning two fileds into quintiles
        #1 income_to_median--ROUNDING!!!!S
        income_med = frame['income_to_median']
        scores = [1,2,3,4,5]
        cats1 = pd.qcut(income_med,5, labels=scores)
        income_score = {
            cats1[0] : 1,
            cats1[1] : 2,
            cats1[2] : 3,
            cats1[3] : 4,
            cats1[4] : 5
        }
        #arr1 = np.array(income_med)
        #bins1 = [np.percentile(arr1, 0).round(2),
        #        np.percentile(arr1, 20).round(2),
        #        np.percentile(arr1, 40).round(2),
        #        np.percentile(arr1, 60).round(2),
        #        np.percentile(arr1, 80).round(2),
        #        np.percentile(arr1, 100).round(2)
        #        ]
        # cats1 = pd.qcut(income_med,5)

        #2 loan_to_income
        loan_income = frame['loan_to_income']
        cats2 = pd.qcut(loan_income,5, labels=scores)
        #frame['loan_score'] = pd.qcut(frame['loan_to_income'],5, labels=scores)

        loan_score = {
            cats2[0] : 1,
            cats2[1] : 2,
            cats2[2] : 3,
            cats2[3] : 4,
            cats2[4] : 5
        }
        hdr = list(frame.columns.values)
        hdr.remove('loan_to_income')


        loan_frame = frame['loan_to_income'].groupby(frame['action_taken_name']).mean()

        income_frame = frame['income_to_median'].groupby(frame['action_taken_name']).mean()

        census_frame = frame['income_to_median'].groupby(frame['census_tract_number']).mean()



    #create 1-5 "risk scores" for:
        #1) loan to income originated 
        #2) lending to low income for MSA
        #4) loan characteritics --second lien or HOEPA
        #5) denials for women or minorities
        
  # create a risk score for each line item corresponding to ...
        # raw data to csv in s3
        conn = S3Connection('<aws access key>', '<aws secret key>')
        path = 
        frame.to_csv(path, sep=',',header=True, mode='w')

        #dataframe grouped on loan risk info



        #dataframe grouped on borrower risk info



    def sql_load(self, state, bd_headers):
        """
        Checks to see if table exists for state.
        If it does not, create a new table and copy data
        If a table does exist, truncate and insert data
        If inserted data is of the wrong shape (ddl error), return message
        """
        
        try:
            if not state:
              #create NEW sql_lite table with state name and bd_headers
                state = input('what state?')
                connection = sqlite3.connect(state+'.sqlite')
                cursor = connection.cursor()
                cursor.execute("""CREATE TABLE state1 
                               (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL
                                ,name TEXT NOT NULL)""")
                connection.commit()
                connection.close()
            else:
              #drop table and reload data
                connection = sqlite3.connect(state+'.sqlite')
                cursor = connection.cursor()
                #cursor.execute("""drop table state""")
                cursor.execute("""CREATE TABLE state 
                               (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL
                                ,name TEXT NOT NULL)""")
                connection.commit()
                connection.close()

    def run_risk_report(self, state):
        """
        defines the top 5 riskiest census tracts per state
        """









