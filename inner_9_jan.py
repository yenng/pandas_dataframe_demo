from ib_insync import *
#from IPython.display import display, clear_output
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time


def meanFreePath(v, f):
    n = 200
    
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


def plot_graph(data0, data1):
    """ Function to plot 2 graph."""

    # Plot the first graph for bids.
    plt.subplot(2,1,1)
    plt.plot(data0)
    plt.title("Bids mean free path.")

    # Plot the second graph for asks.
    plt.subplot(2,1,2)
    plt.plot(data1)
    plt.title("Asks mean free path.")

    # Update the graph when new value add in.
    plt.pause(0.0001)

if __name__ == "__main__":
    try:
        delta_x = 0.01

        util.startLoop()

        ib = IB()
        ib.connect('127.0.0.1', 7496, clientId=5)
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
            price = ticker.close

            # Skip the first data. (first data is not valid.)
            if count > 0:
                vol_list.append(current_vol)
                price_list.append(price)

                # Start storing data after 2 valid data.
                if count >= 2:

                    # Get the different of the data after 1 ticker.
                    vol_diff = vol_list[1] - vol_list[0]
                    vol_list.pop(0)

                    price_diff = price_list[1] - price_list[0]
                    price_list.pop(0)

                    # Store the sum of bid and ask to a list.
                    bids_sum.append(vol_diff["volBids"])
                    asks_sum.append(vol_diff["volAsks"])

                    # Get the time taken and rate of change.
                    t1 = time.time()
                    rate = price_diff/(t1-t0) # unit is usd/s
                    rate_list.append(rate)
                    
                    t0 = t1
                
                    # Mask for every 200 valid data.
                    if len(bids_sum) > 200:
                        # Get the mean free path.
                        bids_m = meanFreePath(rate_list, bids_sum)
                        asks_m = meanFreePath(rate_list, asks_sum)

                        # Append the result to a list.
                        bids_m_list.append(bids_m)
                        asks_m_list.append(asks_m)

                        # Remove the first element from list.
                        bids_sum.pop(0)
                        asks_sum.pop(0)
                        rate_list.pop(0)

                        # Plot the graph when value add in.
                        plot_graph(bids_m_list, asks_m_list)

            count+=1

        # Plot the graph.
        plt.plot()
        
        # Call the event handler function.
        ticker.updateEvent += onTickerUpdate
        
        # Get the data within 20s.
        ib.sleep(20)
        #ib.run() # run forever.

        # stop and disconnect.        
        ib.cancelMktDepth(contract)
        ib.disconnect()

        #print(vol_diff_df)

    except KeyboardInterrupt:

        # Stop and disconnect when keyboard interrupt.
        ib.cancelMktDepth(contract)
        ib.disconnect()
        

