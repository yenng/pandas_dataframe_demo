from ib_insync import *
#from IPython.display import display, clear_output
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
from time import sleep, time
import sys


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

    # Update the graph.
    plt.pause(0.0001)

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

def main(in_data=None, mask=200, loop=3000):
    x_list = []
    bid_sum = []
    ask_sum = []
    rate_list = []
    bids_m_list = []
    asks_m_list = []
    t0 = time()

    # Plot the graph.
    plt.plot()
    
    # Create a dummy situation where it have 300 events happened.
    for i in range(loop):

        # Random sleep for few millisecond.
        sleep(round(random.uniform(0.01,0.05),3))
        t1 = time()

        if in_data:
            current_x = in_data[i]
        else:
            # Create a dummy data.
            current_x = pd.DataFrame(index=range(10),columns='volBids volAsks'.split())
            
            for j in range(10):
                bids = random.randint(0,5)
                asks = random.randint(0,5)
                current_x.loc[j] = [bids, asks]

        print(str(i) + " =================================")
        print(current_x)

        # Main function run here.
        #Skip the first data.
        if i > 0:
            x_list.append(current_x)

            #Get the subtraction for the third data onwards.
            if len(x_list)==2:
                
                x_diff = x_list[1] - x_list[0]

                x_list.pop(0)

                # Get the sum of the different.
                bid_sum.append(x_diff["volBids"].sum())
                ask_sum.append(x_diff["volAsks"].sum())

                # random a price different.
                price_diff = random.uniform(-20,20)
                time_taken = t1 - t0
                t0 = t1

                rate_of_change = price_diff/time_taken

                rate_list.append(rate_of_change)
                if len(ask_sum) > mask:
                    import pdb
                    pdb.set_trace()
                    # Get the mean free path for bids and asks.                    
                    bids_m = round(meanFreePath(rate_list, bid_sum),3)
                    asks_m = round(meanFreePath(rate_list, ask_sum),3)

                    bids_m_list.append(bids_m)
                    asks_m_list.append(asks_m)

                    # Remove the first element.
                    ask_sum.pop(0)
                    bid_sum.pop(0)
                    rate_list.pop(0)
                    
                    plot_graph(bids_m_list, asks_m_list)
    
            
    #print(ask_sum)
    #print(bid_sum)
    #print(rate_list)
if __name__ == '__main__':
    try:
        main(None,3,7)
    except KeyboardInterrupt:
        sys.exit()
    

