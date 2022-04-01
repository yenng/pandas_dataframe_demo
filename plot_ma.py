import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def main():
    plt.style.use('fivethirtyeight')

    fig2 = plt.figure()
    fig2.set_figheight(4)
    fig2.set_figwidth(8)

    def animate(i):
        data = pd.read_csv('data.csv')
        if len(data['bids_m']) > 200:
            x = np.array(range(200)).astype(float)
            y1 = np.array(data['bids_m'][-200:]).astype(float)
            y2 = np.array(data['asks_m'][-200:]).astype(float)
            y1_ma = np.array(data['bids_ma'][-200:]).astype(float)
            y2_ma = np.array(data['asks_ma'][-200:]).astype(float)
        else:
            x = np.array(range(len(data['bids_m']))).astype(float)
            y1 = np.array(data['bids_m']).astype(float)
            y2 = np.array(data['asks_m']).astype(float)
            y1_ma = np.array(data['bids_ma']).astype(float)
            y2_ma = np.array(data['asks_ma']).astype(float)

        fig2.clf()
        # Separate the value to pos and neg for y1_ma.
        pos_y1_ma = y1_ma.copy()
        pos_y1_ma[y1_ma <= 0] = np.nan
        pos_x1_ma = x.copy()
        pos_x1_ma[y1_ma <= 0] = np.nan
        
        neg_y1_ma = y1_ma.copy()
        neg_y1_ma[y1_ma > 0] = np.nan
        neg_x1_ma = x.copy()
        neg_x1_ma[y1_ma > 0] = np.nan

        # Separate the value to pos and neg for y2_ma.
        pos_y2_ma =  y2_ma.copy()
        pos_y2_ma[y2_ma  <= 0] = np.nan
        pos_x2_ma = x.copy()
        pos_x2_ma[y2_ma <= 0] = np.nan
        
        neg_y2_ma =  y2_ma.copy()
        neg_y2_ma[y2_ma > 0] = np.nan
        neg_x2_ma = x.copy()
        neg_x2_ma[y2_ma > 0] = np.nan
        
        # Adds subplot on position 2.
        ax_bids_ma = fig2.add_subplot(211)
        
        # Adds subplot on position 4.
        ax_asks_ma = fig2.add_subplot(212)

        # Set value to subplot pos 2.
        ax_bids_ma.plot(pos_x1_ma, pos_y1_ma, color='green', linewidth=1)
        ax_bids_ma.plot(x, y1, color='blue', linewidth=0.5)
        ax_bids_ma.plot(neg_x1_ma, neg_y1_ma, color='red', linewidth=1)
        ax_bids_ma.set_title("Bids mean free path moving average (100).",fontdict={'fontsize':12}) 
        
        # Set value to subplot pos 4.
        ax_asks_ma.plot(pos_x2_ma, pos_y2_ma, color='green', linewidth=1)
        ax_asks_ma.plot(x, y2, color='blue', linewidth=0.5)
        ax_asks_ma.plot(neg_x2_ma, neg_y2_ma, color='red', linewidth=1)
        ax_asks_ma.set_title("Asks mean free path moving average (100).",fontdict={'fontsize':12})

        # Set the y-axis range and ticks.
        #ax_bids_ma.set_ylim(-1,1)
        #ax_bids_ma.set_yticks(np.arange(-1, 1, step=0.25))
        
        #ax_asks_ma.set_ylim(-1,1)
        #ax_asks_ma.set_yticks(np.arange(-1, 1, step=0.25))

        plt.tight_layout()

    ani = FuncAnimation(fig2, animate, interval=0.00001)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()



    
