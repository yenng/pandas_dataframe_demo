from ib_insync import *
#from IPython.display import display, clear_output
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import sys

def meanFreePath(v, f):
    global n

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

def moving_average(data_in, ma=100):
    data = data_in[-ma:]
    if len(data) < 100:
        return 0
    else:
        return np.mean(data)

if __name__ == "__main__":
    n = int(input("Number of dataset (default 200): ") or "200")

    # Initialize the moving average length. (Change the value here if you want different length for moving average.)
    ma_len = int(input("Moving Average (default 200):") or "200")

    fieldnames = ["count", "bids_m", "asks_m", "t_diff", "price_diff",
                  "bids_sum", "asks_sum", "bids_ma", "asks_ma",
                  "rate_of_change", "bids_vol_diff", "asks_vol_diff"]

    # Write header row.
    with open('data.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    try:
        delta_x = 0.01

        util.startLoop()

        ib = IB()
        ib.connect('127.0.0.1', 7496, clientId=1)
        contract = Future('CL', '202202', 'NYMEX')
        #contract = Crypto('BTC', 'PAXOS', 'USD')

        ib.qualifyContracts(contract)
        ticker = ib.reqMktDepth(contract)

        # Global variable that needed to be stored.
        vol_list = []
        price_list = []
        bids_sum = []
        asks_sum = []
        rate_list = []

        # Global variable for final result.
        bids_m_list = []
        asks_m_list = []

        # Global variable to store time info.
        t0 = time.time()
        t1 = None

        count = 0

        def onTickerUpdate(ticker):
            """ Main event handler function when a ticker update."""

            with open('data.csv', 'a') as csv_file:
                # Create dictionary writer to store data.
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                # Global value pass in here.
                global vol_list
                global price_list
                global count
                global bids_sum
                global asks_sum
                global rate_list

                global t0
                global t1

                # Final result.
                global bids_m_list
                global asks_m_list

                # Flag to determine is this data valid.
                valid_data = True

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

                # Get the current closing price.
                price = ticker.domBids[0][0]


                # Skip the first data. (first data is not valid.)
                if count > 0:
                    vol_list.append(current_vol)
                    price_list.append(price)

                    # Start storing data after 2 valid data.
                    if count >= 2:

                        # Check the price diff.
                        price_diff = price_list[1] - price_list[0]

                        if price_diff == 0:
                            # price not changing is invalid data.
                            valid_data = False

                        # Get the time taken and rate of change.
                        t1 = time.time()
                        try:
                            t_diff = t1-t0
                            rate_of_change = price_diff/(t_diff) # unit is usd/s
                        except ZeroDivisionError:
                            # Time changes too small, invalid data.
                            valid_data = False

                        if not valid_data:
                            price_list.pop(-1)
                            return

                        price_list.pop(0)

                        # Get the different of the data after 1 ticker.
                        vol_diff = vol_list[1] - vol_list[0]
                        vol_list.pop(0)

                        # Store the sum of bid and ask to a list.
                        bids_sum.append(vol_diff["volBids"].sum())
                        asks_sum.append(vol_diff["volAsks"].sum())

                        rate_list.append(rate_of_change)

                        t0 = t1

                        # Mask for every n valid data.
                        if len(bids_sum) > n:

                            # Get the mean free path.
                            bids_m = meanFreePath(rate_list, bids_sum)
                            asks_m = meanFreePath(rate_list, asks_sum)

                            # Append the result to a list.
                            bids_m_list.append(bids_m)
                            asks_m_list.append(asks_m)

                            # Save bids_m and asks_m into info.
                            info = {
                                "count": count-n,
                                "bids_m": bids_m,
                                "asks_m": asks_m,
                                "t_diff": t_diff,
                                "price_diff": price_diff,
                                "bids_sum": bids_sum,
                                "asks_sum": asks_sum,
                                "bids_ma": moving_average(bids_m_list, ma_len),
                                "asks_ma": moving_average(asks_m_list, ma_len),
                                "rate_of_change": rate_list,
                                "bids_vol_diff": vol_diff["volBids"].values.tolist(),
                                "asks_vol_diff": vol_diff["volAsks"].values.tolist()
                            }

                            # Append data to csv file.
                            csv_writer.writerow(info)

                            # Remove the first element from list.
                            bids_sum.pop(0)
                            asks_sum.pop(0)
                            rate_list.pop(0)

                count+=1



        # Call the event handler function.
        ticker.updateEvent += onTickerUpdate

        # Get the data within 20s.
        ib.sleep(100)
        #ib.run() # run forever.

        # stop and disconnect.
        ib.cancelMktDepth(contract)
        ib.disconnect()

    except KeyboardInterrupt:

        # Stop and disconnect when keyboard interrupt.
        ib.cancelMktDepth(contract)
        ib.disconnect()
