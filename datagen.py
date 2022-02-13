import csv
import random
import time
from ib_insync import *
#from IPython.display import display, clear_output
import pandas as pd
import numpy as np
import random
from time import sleep, time
import sys
    
def meanFreePath(v, f):
    n = 3
    
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

mask=200
x_list = []
bid_sum = []
ask_sum = []
rate_list = []
bids_m_list = []
asks_m_list = []
t0 = time()
count = 0

fieldnames = ["count", "bids_m", "asks_m", "rate_of_change", "bids_vol_diff", "asks_vol_diff"]

with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:

    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        # Create a dummy situation where it have 300 events happened.
        # Random sleep for few millisecond.
        sleep(round(random.uniform(0.01,0.05),3))
        t1 = time()
        
        # Create a dummy data.
        current_x = pd.DataFrame(index=range(10),columns='volBids volAsks'.split())
        
        for j in range(10):
            bids = random.randint(0,5)
            asks = random.randint(0,5)
            current_x.loc[j] = [bids, asks]

        # Main function run here.
        #Skip the first data.
        if count > 0:
            x_list.append(current_x)

            #Get the subtraction for the third data onwards.
            if len(x_list)==2:
                
                x_diff = x_list[1] - x_list[0]

                x_list.pop(0)

                # Get the sum of the different.
                bid_sum.append(x_diff["volBids"].sum())
                ask_sum.append(x_diff["volAsks"].sum())

                # random a price different.
                price_diff = random.uniform(-2,2)
                time_taken = t1 - t0
                t0 = t1

                rate_of_change = price_diff/time_taken

                rate_list.append(rate_of_change)
                
                if len(ask_sum) > mask:
                    
                    # Get the mean free path for bids and asks.                    
                    bids_m = round(meanFreePath(rate_list, bid_sum),3)
                    asks_m = round(meanFreePath(rate_list, ask_sum),3)

                    bids_m_list.append(bids_m)
                    asks_m_list.append(asks_m)

                    # Remove the first element.
                    ask_sum.pop(0)
                    bid_sum.pop(0)
                    rate_list.pop(0)

                    info = {
                        "count": count-200,
                        "bids_m": bids_m,
                        "asks_m": asks_m,
                        "rate_of_change": rate_of_change,
                        "bids_vol_diff": x_diff["volBids"].values.tolist(),
                        "asks_vol_diff": x_diff["volAsks"].values.tolist()
                    }

                    csv_writer.writerow(info)

        count += 1

