__author__ = 'rmorin'

import datetime
import time
import calendar
import math

Rates = {'12/25/2014': 1.50, '01/25/2015': 1.55, '02/25/2015': 1.60, '03/25/2015': 1.65, '12/25/2015': 1.75,
         '12/31/2018': 6.00}

def Addsemimonth(sourcedate, per):
    if sourcedate.day == 15 and per % 2 != 0:
        day = sourcedate.day - 14
    elif sourcedate.day == 1 and per % 2 != 0:
        day = sourcedate.day + 14
    else:
        day = sourcedate.day
    month = sourcedate.month + per % 12
    if month > 12:
        month = month - 12
    year = sourcedate.year + (per / 24)
    return datetime.date(year, month, day)

def Addmonth(sourcedate, per):
    month = sourcedate.month - 1 + per
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)

def Addbiweekly(sourcedate, per):
    dt = sourcedate + (datetime.timedelta(days=14) * per)
    return datetime.date(dt.year, dt.month, dt.day)

def Addweekly(sourcedate, per):
    dt = sourcedate + (datetime.timedelta(days=7) * per)
    return datetime.date(dt.year, dt.month, dt.day)

def rate_date(reqdate, dict):
    dates = []
    BootstrpInput = []
    RevDict = {}
    posreqdate = 0
    for key, value in dict.items():
        TempDate = datetime.date(int(key[6:10]), int(key[0:2]), int(key[3:5]))
        TempDateNum = str([time.mktime(TempDate.timetuple())])
        RevDict[TempDateNum] = value
        dates.append(TempDateNum)
    ConvReqDate = reqdate
    DateNum = str([time.mktime(ConvReqDate.timetuple())])
    dates.append(DateNum)
    dates.sort()
    for i in [i for i, x in enumerate(dates) if x == DateNum]:
        posreqdate = i
    lower = dates[posreqdate - 1]
    upper = dates[posreqdate + 1]
    InvertDates = {value: key for key, value in Rates.items()}
    BootstrpInput = [InvertDates[RevDict[lower]], RevDict[lower], InvertDates[RevDict[upper]], RevDict[upper]]
    return BootstrpInput

def DiscRate(RateBookEnds, TargetDate):
    today = datetime.date.today()

    #Slicing the input table into component parts and assigning to a variable

    LowDateStr = RateBookEnds[0]
    LowRate = RateBookEnds[1]
    HighDateStr = RateBookEnds[2]
    HighRate = RateBookEnds[3]

    #Converting the strings into a datetime format

    LowDate = datetime.date(int(LowDateStr[6:10]), int(LowDateStr[0:2]), int(LowDateStr[3:5]))
    HighDate = datetime.date(int(HighDateStr[6:10]), int(HighDateStr[0:2]), int(HighDateStr[3:5]))
    IncDist = abs((TargetDate - LowDate).days)
    if IncDist == 0:
        IncDist == 1

    #Calulating the DiscountRate from the BootStrapRate and the YearDecimal

    BootStrapRate = LowRate + (((HighRate - LowRate)/(abs((HighDate - LowDate).days)-1)) * IncDist)
    YearDecimal = abs((TargetDate - today).days)/365.25
    DiscountRate = ((1 + BootStrapRate / 200) ** 2) ** (YearDecimal * -1)

    #Returning the DiscountRate for the respective TargetDateStr

    return DiscountRate

def TotalMtgCF(Am, PayFreq, Amt, Rate, MatDateStr, NxtPmtDtStr):
    today = datetime.date.today()
    balance = Amt
    MatDate = datetime.date(int(MatDateStr[6:10]), int(MatDateStr[0:2]), int(MatDateStr[3:5]))
    NxtPmt = datetime.date(int(NxtPmtDtStr[6:10]), int(NxtPmtDtStr[0:2]), int(NxtPmtDtStr[3:5]))
    pprate = 0.008
    totalcashflow = 0

# Determine the number of iterations of the loop

    if PayFreq == 'monthly':
            LoopIter = math.trunc((int((MatDate - NxtPmt).days) / 365.25) * 12)
    elif PayFreq == 'semimonthly':
            LoopIter = math.trunc((int((MatDate - NxtPmt).days) / 365.25) * 24)
    elif PayFreq == 'biweekly':
        while NxtPmt < MatDate:
            NxtPmt = NxtPmt + datetime.timedelta(days=14)
            LoopIter = LoopIter + 1
    elif PayFreq == 'weekly':
        while NxtPmt < MatDate:
            NxtPmt = NxtPmt + datetime.timedelta(days=7)
            LoopIter = LoopIter + 1

# Creating a variable called NumPer that holds that number of compounding periods

    if PayFreq == 'monthly':
        NumPer = 12
    elif PayFreq == 'semimonthly':
        NumPer = 24
    elif PayFreq == 'biweekly':
        NumPer = 26
    else:
        NumPer = 52

# Interest rate and Am adjusted for payment frequency is calculated

    AdjAm = Am * NumPer
    AdjRate = (1 + Rate/200) ** (1.0 / 6.0) - 1

# Loop through mortgage calc balance outstnd and CF

    for item in range(LoopIter):
        eti = balance * AdjRate
        etp = (balance * (AdjRate * ((1 + AdjRate) ** AdjAm)) / ((1 + AdjRate) ** AdjAm - 1)) - eti
        ppyamt = balance * (1 - ((1 - pprate) ** (1.0 / 12.0)))
        balance = balance - etp - ppyamt
        cashflow = etp + eti + ppyamt
        if PayFreq == 'monthly':
            discCF = (etp + eti + ppyamt) * DiscRate(rate_date(Addmonth(NxtPmt, item), Rates),
                                                     Addweekly(NxtPmt, item))
        elif PayFreq == 'semimonthly':
            discCF = (etp + eti + ppyamt) * DiscRate(rate_date(Addsemimonth(NxtPmt, item), Rates),
                                                     Addsemimonth(NxtPmt, item))
        elif PayFreq == 'biweekly':
            discCF = (etp + eti + ppyamt) * DiscRate(rate_date(Addbiweekly(NxtPmt, item), Rates),
                                                     Addbiweekly(NxtPmt, item))
        else:
            discCF = (etp + eti + ppyamt) * DiscRate(rate_date(Addweekly(NxtPmt, item), Rates),
                                                     Addweekly(NxtPmt, item))
        totalcashflow = totalcashflow + discCF
    balance = balance * DiscRate(rate_date(MatDate, Rates), MatDate)
    return totalcashflow + balance

def MtgPV(Am, PayFreq, Amt, Rate, MatDateStr, NxtPmtDtStr):
    today = datetime.date.today()
    balance = Amt
    MatDate = datetime.date(int(MatDateStr[6:10]), int(MatDateStr[0:2]), int(MatDateStr[3:5]))
    NxtPmt = datetime.date(int(NxtPmtDtStr[6:10]), int(NxtPmtDtStr[0:2]), int(NxtPmtDtStr[3:5]))
    pprate = 0.008
    totalcashflow = 0

# Determine the number of iterations of the loop

    if PayFreq == 'monthly':
            LoopIter = math.trunc((int((MatDate - NxtPmt).days) / 365.25) * 12)
    elif PayFreq == 'semimonthly':
            LoopIter = math.trunc((int((MatDate - NxtPmt).days) / 365.25) * 24)
    elif PayFreq == 'biweekly':
        while NxtPmt < MatDate:
            NxtPmt = NxtPmt + datetime.timedelta(days=14)
            LoopIter = LoopIter + 1
    elif PayFreq == 'weekly':
        while NxtPmt < MatDate:
            NxtPmt = NxtPmt + datetime.timedelta(days=7)
            LoopIter = LoopIter + 1

# Creating a variable called NumPer that holds that number of compounding periods

    if PayFreq == 'monthly':
        NumPer = 12
    elif PayFreq == 'semimonthly':
        NumPer = 24
    elif PayFreq == 'biweekly':
        NumPer = 26
    else:
        NumPer = 52

# Interest rate and Am adjusted for payment frequency is calculated

    AdjAm = Am * NumPer
    AdjRate = (1 + Rate/200) ** (1.0 / 6.0) - 1

# Loop through mortgage calc balance outstnd and CF

    for item in range(LoopIter):
        eti = balance * AdjRate
        etp = (balance * (AdjRate * ((1 + AdjRate) ** AdjAm)) / ((1 + AdjRate) ** AdjAm - 1)) - eti
        ppyamt = balance * (1 - ((1 - pprate) ** (1.0 / 12.0)))
        balance = balance - etp - ppyamt
        cashflow = etp + eti + ppyamt
        if PayFreq == 'monthly':
            discCF = (etp + eti + ppyamt) * DiscRate(rate_date(Addmonth(NxtPmt, item), Rates), Addweekly(NxtPmt, item))
        elif PayFreq == 'semimonthly':
            discCF = (etp + eti + ppyamt) * DiscRate(rate_date(Addsemimonth(NxtPmt, item), Rates),
                                                     Addsemimonth(NxtPmt, item))
        elif PayFreq == 'biweekly':
            discCF = (etp + eti + ppyamt) * DiscRate(rate_date(Addbiweekly(NxtPmt, item), Rates),
                                                     Addbiweekly(NxtPmt, item))
        else:
            discCF = (etp + eti + ppyamt) * DiscRate(rate_date(Addweekly(NxtPmt, item), Rates),
                                                     Addweekly(NxtPmt, item))
        return TotalMtgCF(Am, PayFreq, Amt, Rate, MatDateStr, NxtPmtDtStr)

print (MtgPV(10,'monthly', 100000, 5.25, '12/31/2016', '12/30/2014'))