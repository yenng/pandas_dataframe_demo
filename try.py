from ib_insync import *
#from IPython.display import display, clear_output
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random


x_list = []
x_final = pd.DataFrame(index=range(10))
sum_tupple = []
count = 0
for i in range(300):

    current_x = pd.DataFrame(index=range(10),columns='volBids volAsks'.split())
    
    for j in range(10):
        bids = round(random.randint(0,20))
        asks = round(random.randint(0,20))
        current_x.loc[j] = [bids, asks]

    #Skip the first data.
    if i > 0:        
        s_bid = "volBids|t="+str(i)
        s_ask = "volAsks|t="+str(i)
        x_list.append(current_x)

        #Get the subtraction for the third data onwards.
        if len(x_list)==2:
            x_diff = x_list[1] - x_list[0]
            x_list.pop(0)

            #Store the data into final data frame.
            x_final[s_bid] = x_diff["volBids"]
            x_final[s_ask] = x_diff["volAsks"]

            bid_sum = x_final[s_bid].sum()
            ask_sum = x_final[s_ask].sum()
            
            sum_tupple.append((bid_sum,ask_sum))
            if len(sum_tupple) > 200:
                #Do some alghorithm.
                sum_tupple.pop(0)
                count += 1
        
print(sum_tupple)
print(count)

x_final.to_csv('try.csv')
