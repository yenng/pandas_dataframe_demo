import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def to_float_list(lst_in):
    """ Convert string list to float list."""
    lst_out = []
    for vol in lst_in:
        out = vol.strip('][').split(', ')
        out_1 = [float(i) for i in out]
        lst_out.append(out_1)

    return lst_out

def formula(rates, vols):
    """Formula:
                                        (      part a     )(    part b    )
    cor = 1/[std(rate)*std(vol)] * mean{[rate - mean(rate)][vol - mean(vol)]}
                                         ^n                  ^n
    """

    # Calculate standard deviation.
    std_rate = np.std(rates)

    # Calculate average.
    mean_rate = np.average(rates)
    
    mean_vol = []
    std_vol = []
    for vol in vols:
        std_vol.append(np.std(vol))
        mean_vol.append(np.average(vol))

    mean_ab = []
    result = []
    # Calculate the mean of formula.
    for j in range(len(vols)):
        ab_lst = []
        for i in range(len(rates)):
            a = rates[i] - mean_rate
            b = vols[j][i] - mean_vol[j]
            ab_lst.append(a*b)           # n = 300

        # Calculate mean of a*b.
        mean_ab.append(np.average(ab_lst))     # n = 10

        # Calculate the final formula.
        result.append(1/(std_rate*std_vol[j])*mean_ab[j])

    return result

def plot(data):
    """Plot data using matplotlib."""

    titles = ['Bids result', 'Asks result']
    x = list(range(len(data[0])))
    for i in range(len(data)):
        plt.subplot(len(data),1,i+1)
        plt.plot(x, data[i], marker='.')
        plt.title(titles[i])
        
        for j,coor in enumerate(data[i]):
            plt.text(j, coor, round(coor,3))
        
    plt.show()

def main():
    """Main function run here."""
    
    # Read data from data.csv
    data = pd.read_csv('data.csv')[-300:]

    rates = data['rate_of_change'].values.tolist()  # n = 300
    bids_d = data['bids_vol_diff'].values.tolist()  # n = 300
    asks_d = data['asks_vol_diff'].values.tolist()  # n = 300
    bids_d_trans = []
    asks_d_trans = []

    # Convert to float list.
    bids_d_list = to_float_list(bids_d)             # n = 300
    asks_d_list = to_float_list(asks_d)             # n = 300

    # Transpose vol_diffs_list.
    for i in range(10):
        bids_d_trans.append([item[i] for item in bids_d_list]) # n = 10
        asks_d_trans.append([item[i] for item in asks_d_list]) # n = 10

    result_bids = formula(rates, bids_d_trans)
    result_asks = formula(rates, asks_d_trans)
    plot([result_bids, result_asks])

if __name__ == "__main__":
    x = main()




    
