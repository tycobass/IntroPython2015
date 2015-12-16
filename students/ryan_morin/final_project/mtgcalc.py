__author__ = 'rmorin'

import pandas as pd
import numpy as np
import datetime as dt
import Mortgage as mc
import time as t


"""
VARIABLES
===================
"""

prepayment_rate = 0.05
default_rate = 0.015
total = 0
r0 = 0.04
r1 = 0.09
r2 = 0.08
r3 = 0.13
r4 = 0.25
r5 = 0.32
r6 = 0.30
r7 = 0.45
date = dt.datetime.today()
date = date.replace(hour=0, minute=0, second=0, microsecond=0)
yield_c = pd.DataFrame()
yield_c_up = pd.DataFrame()
yield_c_dn = pd.DataFrame()
mtgportfolio = np.array(pd.read_csv('C:/Users/ryan/Desktop/mtgs.csv', index_col=None, header=None, sep=','))
ycurve = np.array(pd.read_csv('C:/Users/ryan/Desktop/rates.csv', index_col=None, header=None, sep=','))

"""
COPY OF DATA FRAME
===================
"""

ycurve_up = ycurve.copy()
ycurve_up[2][0] = float(ycurve[2][0]) + r0
ycurve_up[2][1] = float(ycurve[2][1]) + r1
ycurve_up[2][2] = float(ycurve[2][2]) + r2
ycurve_up[2][3] = float(ycurve[2][3]) + r3
ycurve_up[2][4] = float(ycurve[2][4]) + r4
ycurve_up[2][5] = float(ycurve[2][5]) + r5
ycurve_up[2][6] = float(ycurve[2][6]) + r6
ycurve_up[2][7] = float(ycurve[2][7]) + r7

ycurve_dn = ycurve.copy()
ycurve_dn[2][0] = float(ycurve[2][0]) - r0
ycurve_dn[2][1] = float(ycurve[2][1]) - r1
ycurve_dn[2][2] = float(ycurve[2][2]) - r2
ycurve_dn[2][3] = float(ycurve[2][3]) - r3
ycurve_dn[2][4] = float(ycurve[2][4]) - r4
ycurve_dn[2][5] = float(ycurve[2][5]) - r5
ycurve_dn[2][6] = float(ycurve[2][6]) - r6
ycurve_dn[2][7] = float(ycurve[2][7]) - r7


"""
FUNCTIONS
===================
"""


def fvrate():
    rate = (1 + (test.pmtrate() / test.pmtfreq())) ** (test.amort() * test.pmtfreq())
    return rate


def pipmt():
    pmt = test.principal * ((test.pmtrate() / test.pmtfreq()) * fvrate()) / (fvrate() - 1)
    return pmt


def daysout():
    numdys = date - test.dateadv()
    return numdys


def num_tot_pmt():
    # Total number of payments
    term = ((test.datemat() - test.dateadv()) / 365) * test.pmtfreq()
    return int(term / np.timedelta64(1, 'D'))


def num_pmt_made():
    # Number of payments made
    pmade = (daysout() / 365) * test.pmtfreq()
    return int(pmade / np.timedelta64(1, 'D'))


def num_pmt_rem():
    # Number of remaining payments
    rem = num_tot_pmt() - num_pmt_made()
    return rem


def fut_pmt_date(num):
    if test.pmtfreq() == 52:
        pmtdate = test.dateadv() + pd.DateOffset(days=(7*num))
    elif test.pmtfreq() == 26:
        pmtdate = test.dateadv() + pd.DateOffset(days=(14*num))
    else:
        pmtdate = test.dateadv() + pd.DateOffset(months=(1*num))
    return pmtdate


def dframe_freq():
    if test.pmtfreq() == 52:
        freq = 'W'
    elif test.pmtfreq() == 26:
        freq = '2W'
    else:
        freq = 'MS'
    return freq


def mtg_bal_calc():
    temp = list()
    for futpmt in range(num_pmt_rem()):
        fvorig = test.principal * (1 + (test.pmtrate() / test.pmtfreq())) ** (num_pmt_made() + futpmt)
        fvannbal = pipmt() * (((1 + (test.pmtrate() / test.pmtfreq())) ** (num_pmt_made() + futpmt)) - 1)\
            / (test.pmtrate() / test.pmtfreq())
        total = fvorig - fvannbal
        temp.append(total)
    return temp


def yield_curve(end):
    """
    The function bootstraps the interest rates between two dates. It then calculates a discount factor (DF). The DF
    will be used to discount the mortgage cash flows.

    Output
    ==============
    Interest rates between two points
    Time weight (Date - today)/ 365.25
    Discount rate = (1 + (TmWght /200) ** 0.5) ** -Rates
    """
    dates = pd.date_range(ycurve[0][end-1], periods=(int(ycurve[1][end]) - int(ycurve[1][end-1])), freq = 'D')
    rates = np.linspace(float(ycurve[2][end-1]), float(ycurve[2][end]),
                        (int(ycurve[1][end]) - int(ycurve[1][end-1])))
    tmwght = np.linspace(int(ycurve[1][end-1]), int(ycurve[1][end]), (int(ycurve[1][end]) - int(ycurve[1][end-1])))
    df = pd.DataFrame(rates, columns=['Rates'], index=dates)
    df['TmWght'] = (tmwght / 365.25)
    df['DiscFctr'] = (1 + (df['TmWght'] / 200) ** 0.5) ** (df['Rates'] * -1)
    return df


def yield_curve_up(end):
    """
    RATE UP - The function bootstraps the interest rates between two dates. It then calculates a discount factor (DF).
    The DF will be used to discount the mortgage cash flows.

    Output
    ==============
    Interest rates between two points
    Time weight (Date - today)/ 365.25
    Discount rate = (1 + (TmWght /200) ** 0.5) ** -Rates
    """
    dates = pd.date_range(ycurve_up[0][end-1], periods=(int(ycurve_up[1][end]) - int(ycurve_up[1][end-1])), freq = 'D')
    rates = np.linspace(float(ycurve_up[2][end-1]), float(ycurve_up[2][end]),
                        (int(ycurve_up[1][end]) - int(ycurve_up[1][end-1])))
    tmwght = np.linspace(int(ycurve_up[1][end-1]), int(ycurve_up[1][end]),
                         (int(ycurve_up[1][end]) - int(ycurve_up[1][end-1])))
    df_up = pd.DataFrame(rates, columns=['Rates'], index=dates)
    df_up['TmWght'] = (tmwght / 365.25)
    df_up['DiscFctr'] = (1 + (df_up['TmWght'] / 200) ** 0.5) ** (df_up['Rates'] * -1)
    return df_up


def yield_curve_dn(end):
    """
    RATE DOWN - The function bootstraps the interest rates between two dates. It then calculates a discount factor (DF).
    The DF will be used to discount the mortgage cash flows.

    Output
    ==============
    Interest rates between two points
    Time weight (Date - today)/ 365.25
    Discount rate = (1 + (TmWght /200) ** 0.5) ** -Rates
    """
    dates = pd.date_range(ycurve_dn[0][end-1], periods=(int(ycurve_dn[1][end]) - int(ycurve_dn[1][end-1])), freq = 'D')
    rates = np.linspace(float(ycurve_dn[2][end-1]), float(ycurve_dn[2][end]),
                        (int(ycurve_dn[1][end]) - int(ycurve_dn[1][end-1])))
    tmwght = np.linspace(int(ycurve_dn[1][end-1]), int(ycurve_dn[1][end]),
                         (int(ycurve_dn[1][end]) - int(ycurve_dn[1][end-1])))
    df_dn = pd.DataFrame(rates, columns=['Rates'], index=dates)
    df_dn['TmWght'] = (tmwght / 365.25)
    df_dn['DiscFctr'] = (1 + (df_dn['TmWght'] / 200) ** 0.5) ** (df_dn['Rates'] * -1)
    return df_dn


"""
PROGRAM
===================
"""

for end in range(1, 8):
    yield_c = yield_c.append(yield_curve(end))
    yield_c_up = yield_c_up.append(yield_curve_up(end))
    yield_c_dn = yield_c_dn.append(yield_curve_dn(end))

for mtg in range(1, len(mtgportfolio)):
    test = mc.Mortgage(float(mtgportfolio[mtg][0]), float(mtgportfolio[mtg][1]), mtgportfolio[mtg][2],
            mtgportfolio[mtg][3], int(mtgportfolio[mtg][4]), mtgportfolio[mtg][5])

    # Below is the set up of the DataFrame

    pmtdates = pd.date_range(fut_pmt_date(num_pmt_made()), periods=int(num_pmt_rem()), freq=dframe_freq())
    df = pd.DataFrame(mtg_bal_calc(), columns=['EndBalance'], index=pmtdates)
    df['PIPmt'] = df['EndBalance'] * ((test.pmtrate() / test.pmtfreq()) * fvrate()) / (fvrate() - 1)
    df['ETI'] = df['EndBalance'] * (test.pmtrate() / test.pmtfreq())
    df['ETP'] = df['PIPmt'] - df['ETI']
    df['PPmt'] = df['EndBalance'] * (1 - (1 - prepayment_rate) ** (1.0 / 12.0))
    df['DefAmt'] = (df['EndBalance'] - df['ETP'] - df['PPmt']) * (1 - (1 - default_rate) ** (1 / 12.0))
    df['Balloon'] = np.where(np.round((df['EndBalance'] - (df.loc[df.idxmin()]['EndBalance']).mean()), 0) == 0,
                             df['EndBalance'], 0)
    df['CshFlw'] = df['PIPmt'] + df['PPmt'] + df['DefAmt'] + df['Balloon']

    temp_tbl = df.join(yield_c)
    temp_tbl_up = df.join(yield_c_up)
    temp_tbl_dn = df.join(yield_c_dn)

    disc_tbl = pd.DataFrame(temp_tbl['CshFlw'] * temp_tbl['DiscFctr'], columns=['DiscCF'])
    disc_tbl_up = pd.DataFrame(temp_tbl_up['CshFlw'] * temp_tbl_up['DiscFctr'], columns=['DiscCF_UP'])
    disc_tbl_dn = pd.DataFrame(temp_tbl_dn['CshFlw'] * temp_tbl_dn['DiscFctr'], columns=['DiscCF_DOWN'])

    e_dur_tbl = pd.concat([disc_tbl, disc_tbl_up, disc_tbl_dn], axis=1)
    e_dur_tbl['EDur'] = (e_dur_tbl['DiscCF_DOWN'] - e_dur_tbl['DiscCF_UP']) / (2 * e_dur_tbl['DiscCF'])
    print (e_dur_tbl.sum())
