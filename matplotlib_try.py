import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

index = count()


def animate(i):
    data = pd.read_csv('data.csv')
    if len(data['bids_m']) > 200:
        x = list(range(200))
        y1 = data['bids_m'][-200:]
        y2 = data['asks_m'][-200:]
    else:
        x = list(range(len(data['bids_m'])))
        y1 = data['bids_m']
        y2 = data['asks_m']
    

    plt.subplot(2,1,1)
    plt.cla()
    plt.plot(x, y1, label='bids_m')
    plt.title("Bids mean free path.") 
    plt.legend(loc='upper left') 

    plt.subplot(2,1,2)  
    plt.cla()
    plt.plot(x, y2, label='asks_m')
    plt.title("Asks mean free path.") 
    plt.legend(loc='upper left') 

    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=0.00001)

plt.tight_layout()
plt.show()
