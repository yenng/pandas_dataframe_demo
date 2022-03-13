import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def main():
    plt.style.use('fivethirtyeight')

    fig = plt.figure()
    fig.set_figheight(4)
    fig.set_figwidth(8)

    def animate(i):
        data = pd.read_csv('data.csv')

        if len(data['bids_m']) > 200:
            x = np.array(range(200)).astype(float)
            y1 = np.array(data['bids_m'][-200:]).astype(float)
            y2 = np.array(data['asks_m'][-200:]).astype(float)
            y1_ma = np.array(data['bids_ma'][-200:]).astype(float)
            y2_ma = np.array(data['asks_ma'][-200:]).astype(float)

            zero = [0]*200
        else:
            x = np.array(range(len(data['bids_m']))).astype(float)
            y1 = np.array(data['bids_m']).astype(float)
            y2 = np.array(data['asks_m']).astype(float)
            y1_ma = np.array(data['bids_ma']).astype(float)
            y2_ma = np.array(data['asks_ma']).astype(float)

            zero = [0]*len(data['bids_m'])
            
        fig.clf()
            
        # Separate the value to pos and neg for y1_ma.
        pos_y1 = y1.copy()
        pos_y1[y1 <= 0] = np.nan
        pos_x1 = x.copy()
        pos_x1[y1 <= 0] = np.nan
        
        neg_y1 = y1.copy()
        neg_y1[y1 > 0] = np.nan
        neg_x1 = x.copy()
        neg_x1[y1 > 0] = np.nan

        # Separate the value to pos and neg for y2_ma.
        pos_y2 =  y2.copy()
        pos_y2[y2  <= 0] = np.nan
        pos_x2 = x.copy()
        pos_x2[y2 <= 0] = np.nan
        
        neg_y2 =  y2.copy()
        neg_y2[y2 > 0] = np.nan
        neg_x2 = x.copy()
        neg_x2[y2 > 0] = np.nan
        
        # Adds subplot on position 2.
        ax_bids = fig.add_subplot(211)
        
        # Adds subplot on position 4.
        ax_asks = fig.add_subplot(212)

        # Set value to subplot pos 2.
        ax_bids.plot(pos_x1, pos_y1, color='green', linewidth=1)
        #ax_bids_ma.plot(x, zero, color='blue', linewidth=0.5)
        ax_bids.plot(neg_x1, neg_y1, color='red', linewidth=1)
        ax_bids.set_title("Bids mean free path).",fontdict={'fontsize':12}) 
        
        # Set value to subplot pos 4.
        ax_asks.plot(pos_x2, pos_y2, color='green', linewidth=1)
        #ax_asks_ma.plot(x, zero, color='blue', linewidth=0.5)
        ax_asks.plot(neg_x2, neg_y2, color='red', linewidth=1)
        ax_asks.set_title("Asks mean free path.",fontdict={'fontsize':12})

        # Set the y-axis range and ticks.
        ax_bids.set_ylim(-1,1)
        ax_bids.set_yticks(np.arange(-1, 1, step=0.25))
        
        ax_asks.set_ylim(-1,1)
        ax_asks.set_yticks(np.arange(-1, 1, step=0.25))

        plt.tight_layout()
    
    ani = FuncAnimation(fig, animate, interval=0.00001)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()


    
