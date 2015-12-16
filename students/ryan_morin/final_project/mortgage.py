import datetime as dt
import pandas as pd

class Mortgage(object):
    """A mortgage from a financial institution. Mortgages have the following properties:

    Attributes:
        principal: A float representing the outstanding mortgage amount
        rate: A float representing the current interest rate
        dtadv: A string representing the date the mortgage was advanced
        freq: A string representing the frequency of the mortgage payment
        am: An int representing the time associated with the mortgage obligation
    """
    def __init__(self, principal, rate, dtadv, freq, am, dtmat):
        """Return a Mortgage object whose principal is *principal*, rate is *rate*, dtadv is *dtadv*,
        frequency is *freq* and amortization is *am*
        """
        self.principal = principal
        self.rate = rate
        self.dtadv = dtadv
        self.freq = freq.upper()
        self.am = am
        self.dtmat = dtmat

    def pmtrate(self):
        adjrate = self.rate / 100
        return adjrate

    def pmtfreq(self):
        if self.freq == 'MONTHLY':
            freq = 12
        elif self.freq == 'BIWEEKLY':
            freq = 26
        elif self.freq == 'WEEKLY':
            freq = 52
        else:
            freq = 12
        return freq

    def principal(self):
        return self.principal

    def dateadv(self):
        return pd.to_datetime(self.dtadv)

    def amort(self):
        return self.am

    def datemat(self):
        return pd.to_datetime(self.dtmat)