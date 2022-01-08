from ib_insync import *
#from IPython.display import display, clear_output
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

delta_x = 0.01

util.startLoop()

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=5)
contract = Future('CL', '202202', 'NYMEX')
#contract = Crypto('BTC', 'PAXOS', 'USD')


ib.qualifyContracts(contract)
ticker = ib.reqMktDepth(contract)

vol_list = []
vol_diff_df = pd.DataFrame(index=range(10))
vol_diff_total = []

count = 0

def onTickerUpdate(ticker):
    """ Main event handler function when a ticker update."""

    # Global value pass in here.
    global vol_list
    global vol_diff_df
    global count
    global vol_diff_total

    # Initialize the dataframe for current volume.
    current_vol = pd.DataFrame(index=range(10),
                               columns='volBids volAsks'.split())

    # Get the bids volume.
    bids = ticker.domBids
    for i in range(10):
        current_vol.iloc[i, 0] = bids[i].size if i < len(bids) else 0

    # Get the asks volume.
    asks = ticker.domAsks
    for i in range(10):
        current_vol.iloc[i, 1] = asks[i].size if i < len(asks) else 0

    # Skip the first data. (first data is not valid.)
    if count > 0:
        s_bid = "volBids|t="+str(count)
        s_ask = "volAsks|t="+str(count)
        vol_list.append(current_vol)

        # Start storing data after 2 valid data.
        if count >= 2:

            # Get the different of the data after 1 ticker.
            vol_diff = vol_list[1] - vol_list[0]
            vol_list.pop(0)

            # Store the data into dataframe.
            vol_diff_df[s_bid] = vol_diff["volBids"]
            vol_diff_df[s_ask] = vol_diff["volAsks"]

            # Store the sum of bid and ask.
            bid_sum = vol_diff_df[s_bid].sum()
            ask_sum = vol_diff_df[s_ask].sum()

            # Append the bid and ask total to a tupple list.
            vol_diff_total.append(bid_sum, ask_sum)

            # Mask for every 200 valid data.
            if len(vol_diff_total) > 200:
                # ToDo: some algorithm here.

                # Remove the first element from list.
                vol_diff_total.pop(0)

    count+=1

# Call the event handler function.
ticker.updateEvent += onTickerUpdate

# Get the data within 20s.
ib.sleep(20)

ib.cancelMktDepth(contract)
ib.disconnect()

#print(vol_diff_df)

"""
def meanFreePath(v, f):

    mean_v = np.mean(v)
    mean_f = np.mean(f)

    numer = 0
    denom = 0

    for i in range(n):
        numer += (f[i] - mean_f)*(v[i] - mean_v)
        denom += (f[i] - mean_f)**2

    m = numer/denom

    return m

def knudsen(L):

    kn = L/10

    return kn
"""
