#!/user/bin/env
from project_moduledev import Intel_Builder
import pandas as pd
import sqlite3 as sql

state = input(' > Type desired state abbreviation in caps >')

year = input(' > Select a single year would you like between 2007 and 2014 >')

limit = input(' > How many records would you like? 0 will return all from year >')

# create instance of Intel_Builder object
ib = Intel_Builder(state,limit)

ib.hmda_api(state,limit)

#pulling full data to transform in query
dataframe = ib.frame

#data wrangling queries
ib.data_wrangle(dataframe)

#pulling fully reports aggregated on census tract to store
income_risk = ib.risk_final
income_risk_alias = '_loan_risk'
redlining_risk = ib.redline_final
redlining_risk_alias = '_redline'

#create summary report tables and save them to SQLITE
ib.reports_to_sql(dataframe,income_risk,income_risk_alias)
ib.reports_to_sql(dataframe,redlining_risk,redlining_risk_alias)

#querying top 50 of income_risk report to test
state = ib.state

rpt1 = pd.read_sql_query("SELECT * from {} ORDER BY income_risk_score DESC limit 50".format(state+income_risk_alias),
     sql.connect(state + income_risk_alias + '.sqlite'))

rpt2 = pd.read_sql_query("SELECT * from {} ORDER BY redlining_score DESC limit 50".format(state+redlining_risk_alias),
     sql.connect(state + redlining_risk_alias + '.sqlite'))

print(rpt1)
print(rpt2)





