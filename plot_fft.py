import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pyparsing import srange

import warnings
warnings.filterwarnings('ignore')

def main():
    """Main function run here."""
    
    # Initialize the plot figure.
    plt.style.use('fivethirtyeight')

    fig = plt.figure()
    fig.set_figheight(4)
    fig.set_figwidth(8)
    
    # Read data from data.csv
    def animate(i):
        # Set sampling rate.
        sr = 500
        # Clear previous values.
        fig.clf()
        
        if (len(pd.read_csv('data.csv')) > sr):
            data = pd.read_csv('data.csv')[-sr:]
            bids_m = data['bids_m'].to_numpy()
            asks_m = data['asks_m'].to_numpy()
            
            X = np.fft.rfft(bids_m)
            X1 = np.fft.rfft(asks_m)
            n = np.array(range(len(X))).astype(float)
            
            ax_bids_fft = fig.add_subplot(211)
            ax_bids_fft.stem(n, np.abs(X), 'b', markerfmt=" ", basefmt="-b")
            
            ax_asks_fft = fig.add_subplot(212)
            ax_asks_fft.stem(n, np.abs(X1), 'b', markerfmt=" ", basefmt="-b")
    
    ani = FuncAnimation(fig, animate, interval=0.00001)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()