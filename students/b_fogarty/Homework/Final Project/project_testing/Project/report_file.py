#!/user/bin/env
from project_module import Intel_Builder

state = input(' > Type desired state abbreviation in caps >')

limit = input(' > How many records would you like? 0 will return all >')

# create instance of Intel_Builder object
ib = Intel_Builder(state,limit)

ib.hmda_api(state,limit)

#pulling full data to transform in query
dataframe = ib.frame

#data wrangling queries
ib.data_wrangle(dataframe)

#pulling fully reports aggregated on census tract to store
#income_risk = ib.risk
#redlining_risk = ib.redline

#ib.reports_to_sql(income_risk,'_loan_risk')
#ib.reports_to_sql(redlining_risk,'_redline')

#querying top 50 of income_risk report to test




