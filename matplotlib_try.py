import random
from itertools import count
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def main():
    plt.style.use('fivethirtyeight')

    fig = plt.figure()

    fig.set_figheight(8)
    fig.set_figwidth(15)
    x_vals = []
    y_vals = []

    index = count()

    def animate(i):
        data = pd.read_csv('data.csv')
        if len(data['bids_m']) > 200:
            x = list(range(200))
            y1 = data['bids_m'][-200:]
            y2 = data['asks_m'][-200:]
            y1_ma = data['bids_ma'][-200:]
            y2_ma = data['asks_ma'][-200:]
        else:
            x = list(range(len(data['bids_m'])))
            y1 = data['bids_m']
            y2 = data['asks_m']
            y1_ma = data['bids_ma']
            y2_ma = data['asks_ma']
        
        fig.clf()
        # Adds subplot on position 1.
        ax_bids = fig.add_subplot(411)
        
        # Adds subplot on position 2.
        ax_bids_ma = fig.add_subplot(412)
        
        # Adds subplot on position 3.
        ax_asks = fig.add_subplot(413)
        
        # Adds subplot on position 4.
        ax_asks_ma = fig.add_subplot(414)

        # Set value to subplot pos 1.
        ax_bids.plot(x, y1, label='bids_m', color='blue')
        ax_bids.set_title("Bids mean free path.") 
        ax_bids.legend(loc='upper left')

        # Set value to subplot pos 2.
        ax_bids_ma.plot(x, y1_ma, label='ma100', color='green')
        ax_bids_ma.set_title("Bids mean free path moving average (100).") 
        ax_bids_ma.legend(loc='upper left')
        
        # Set value to subplot pos 3.
        ax_asks.plot(x, y2, label='asks_m', color='blue')
        ax_asks.set_title("Asks mean free path.") 
        ax_asks.legend(loc='upper left')

        # Set value to subplot pos 4.
        ax_asks_ma.plot(x, y2_ma, label='ma100', color='green')
        ax_asks_ma.set_title("Asks mean free path moving average (100).") 
        ax_asks_ma.legend(loc='upper left')

        plt.tight_layout()

    ani = FuncAnimation(fig, animate, interval=0.00001)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()



    
