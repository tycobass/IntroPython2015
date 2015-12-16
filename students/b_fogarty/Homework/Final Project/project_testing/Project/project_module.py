#!/user/bin/env
import os
import requests
import json
import csv
import sqlite3 as sql
import pandas as pd
import numpy as np

class Intel_Builder(object):

#set destination location
#    dest = os.dirname(abspath(__file__))

    def __init__(self, state = 'WA', limit = 1000):
        self.state = state
        self.limit = limit

    """
    Returns a class for building new database tables with transformed
    data of interest
    """

    def hmda_api(self,state='WA',limit=1000):
        """
        Executes get command against CFPB HMDA API, pulling table into memory
        """
        lar = requests.get('https://api.consumerfinance.gov/data/hmda/slice/'+
                           'hmda_lar.json?%24select=action_taken_name%2Capplicant_ethnicity_name'+
                           '%2Capplicant_income_000s%2Capplicant_race_name_1%2Capplicant_sex_name'+
                           '%2Cas_of_year%2Ccensus_tract_number%2Cdenial_reason_name_1%2Cdenial_reason_name_2'+
                           '%2Choepa_status_name%2Chud_median_family_income%2Clien_status_name%2C%09loan_amount_000s'+
                           '%2C%09msamd_name%2C%09number_of_1_to_4_family_units%2Cnumber_of_owner_occupied_units%2Cpopulation'+
                           '%2Cpreapproval_name%2Crespondent_id%2Csequence_number%2Cstate_abbr%2Cstate_name'+
                           '%2Ctract_to_msamd_income&%24where=loan_purpose_name%3D%27Home+purchase%27+AND+applicant_income_000s+'+
                           '%3C+100+AND+state_abbr+%3D+%27' + state + '%27+AND+property_type_name+%3D+'+
                           '%27One-to-four+family+dwelling+%28other+than+manufactured+housing'+
                           '%29%27+AND+owner_occupancy_name+%3D+%27Owner-occupied+as+a+principal+dwelling%27+&'+
                           '%24group=&%24orderBy=&%24limit=' + limit + '&%24offset=0&%24format=json')

        #decoding contents of drequest into pythonic data type, here, a dict
        data = lar.json()
        dataset = data['results']
        #finshed dataframe
        self.frame = pd.DataFrame(dataset)

    def data_wrangle(self,frame):
        """
        Creates new columns (or modifies existing ones) corresponding to desired demographic and financial metrics 
        and adds them to dataframe
        """

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

        #applying loan decision map
        frame['simplified_decision'] = frame['action_taken_name'].replace(decision_map)

        #replacing HOEPA (very high cost loans) with binary flags
        frame['simplified_hoepa'] = frame['hoepa_status_name'].replace(['HOEPA loan','Not a HOEPA loan'],[1,0])


        #denial flags (multi-column data function)
        def denial_flag(row):
            if row['simplified_decision'] == 'Approved':
                return 0
            if row['simplified_decision'] == 'Denied':
                return 1
            if row['simplified_decision'] == 'Other':
                return np.nan

        frame['denial_flag'] = frame.apply(lambda row: denial_flag(row), axis = 1)

        #special risk score of income to median area income (proxy for relative risk place)
        frame['income_score'] = frame['income_to_median']
        frame['income_score'] = pd.qcut(frame['income_score'],5,labels=False)

        #special risk score of the loan to borrower income ratio 
        frame['loan_score']= frame['loan_to_income']
        frame['loan_score'] = pd.qcut(frame['loan_score'],5, labels=False)

        frame['income_risk_score'] = (frame['loan_score']*40)+(frame['income_score']*60)


        #minority flags (multi-column data function)
        def minority_logic(row):
            if row['applicant_ethnicity_name'] != 'Not Hispanic or Latino':
                return 1
            elif row['applicant_race_name_1'] != 'White':
                return 1
            return 0
        frame['minority_flag'] = frame.apply(lambda row: minority_logic(row), axis = 1)


        def redlining_logic(row):
            if row['minority_flag'] == 1 and row['denial_flag'] == 1:
                return 50
            elif row['minority_flag'] == 1 and row['simplified_hoepa']== 1:
                return 40
            elif row['minority_flag'] == 1 and row['simplified_decision'] == 'Other':
                return 30
            elif row['simplified_hoepa']== 1:
                return 20
            elif row['denial_flag'] == 1:
                return 10
            return 0
        frame['redlining_score'] = frame.apply(lambda row: redlining_logic(row), axis = 1)


        #dataframe grouped on loan risk info
        risk = frame.groupby(['state_name','census_tract_number'])
        risk_report = risk.agg({'income_to_median':'mean',
                            'loan_to_income':'mean',
                            'income_risk_score':'mean'})
        risk_report.sort('income_risk_score',ascending=False)
        risk_final = risk_report


        #dataframe grouped on redlining borrower risk info
        redline = frame.groupby(['state_name','census_tract_number'])
        redline_report = redline.agg({'minority_flag':'mean',
                           'simplified_hoepa':'mean',
                           'denial_flag':'mean',
                           'income_to_median':'mean',
                           'redlining_score':'median'})
        redline_report.sort('redlining_score',ascending=False)
        redline_final = redline_report

"""
    def reports_to_sql(self,report,alias='full_data'):
        """
        #Dumps dataframe to sqlite database to store it in a peristent file. 
        #DB tables are dropped and remade if they already exist.
        """
        state = (frame['state_name'][0])
        cnx = sql.connect(state + alias +'.sqlite')
        redlining_report.to_sql(state+alias,con=cnx,if_exists='replace')
        cnx.commit()
        cnx.close()
        #curs = cnx.cursor
        #cur.execute("SELECT * FROM Massachusetts")
        #df = pd.read_sql_query("SELECT top 50 * from Massachusettsredline", sql.connect('Massachusettsredline.sqlite'))
        #with sql.commit(sql.connect(state + alias +'.sqlite').cursor):
        #    redlining_report.to_sql(state+alias,con=cnx,if_exists='replace')











