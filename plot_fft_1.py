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
    
    # Set sampling rate.
    sr = 500
    if (len(pd.read_csv('data.csv')) > sr):
        data = pd.read_csv('data.csv')[-sr:]
        bids_m = data['bids_m'].to_numpy()
        asks_m = data['asks_m'].to_numpy()
        
        X = np.fft.rfft(bids_m)
        X1 = np.fft.rfft(asks_m)
        n = np.array(range(len(X))).astype(float)
        
        ax_bids_fft = fig.add_subplot(211)
        ax_bids_fft.stem(n, np.abs(X), 'b', markerfmt=" ", basefmt="-b")
        ax_bids_fft.set_title("Bids mean fast fourier transform.",fontdict={'fontsize':12}) 
        
        ax_asks_fft = fig.add_subplot(212)
        ax_asks_fft.stem(n, np.abs(X1), 'b', markerfmt=" ", basefmt="-b")
        ax_asks_fft.set_title("Asks mean fast fourier transform.",fontdict={'fontsize':12}) 

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()