import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pyparsing import srange

import warnings
warnings.filterwarnings('ignore')

def filter_value(arr_in, threshold=0.1):
    """Filter the value that is 0.1 smaller than peak"""
    peak = max(arr_in)
    for i, val in enumerate(arr_in):
        if val == peak or val < threshold*peak:
            arr_in[i] = val
        else:
            arr_in[i] = 0
            
    return arr_in
      
def separate_values(x_in, y_in, separate_value=0):
    
    # Separate the value to pos and neg for val_in.
    y_large = y_in.copy()
    y_large[y_in <= separate_value] = np.nan
    x_large = x_in.copy()
    x_large[y_in <= separate_value] = np.nan
    
    y_small = y_in.copy()
    y_small[y_in > separate_value] = np.nan
    x_small = x_in.copy()
    x_small[y_in > separate_value] = np.nan
    
    return [(x_large, y_large),(x_small, y_small)]

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
            
            X_filtered = filter_value(np.abs(X))
            X1_filtered = filter_value(np.abs(X1))
            n = np.array(range(len(X))).astype(float)

            ax_bids_fft = fig.add_subplot(211)
            pos, neg = separate_values(np.array(range(sr)).astype(float), np.fft.irfft(X_filtered))
            ax_bids_fft.plot(pos[0], pos[1], color='green', linewidth=1)
            ax_bids_fft.plot(neg[0], neg[1], color='red', linewidth=1)
            #ax_bids_fft.plot(np.fft.irfft(X_filtered), color='green', linewidth=1)
            #ax_bids_fft.stem(n, X_filtered, 'b', markerfmt=" ", basefmt="-b")
            
            ax_asks_fft = fig.add_subplot(212)
            pos1, neg1 = separate_values(np.array(range(sr)).astype(float), np.fft.irfft(X1_filtered))
            ax_asks_fft.plot(pos1[0], pos1[1], color='green', linewidth=1)
            ax_asks_fft.plot(neg1[0], neg1[1], color='red', linewidth=1)
            #ax_asks_fft.plot(np.fft.irfft(X1_filtered), color='green', linewidth=1)
            #ax_asks_fft.stem(n, X1_filtered, 'b', markerfmt=" ", basefmt="-b")
    
    ani = FuncAnimation(fig, animate, interval=0.00001)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()