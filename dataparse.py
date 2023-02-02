import pandas as pd
import numpy as np
import math


avgtemp = pd.read_excel(r"temp_data/ann_avg_tempS.xlsx", header = 1)
amptemp = pd.read_excel(r"temp_data/ann_amp_tempS.xlsx", header = 1)
phitemp = pd.read_excel(r"temp_data/ann_phi_tempS.xlsx", header = 1)

avgtemp.name = "avgtemp"
amptemp.name = "amptemp"
phitemp.name = "phitemp"

coordrange = []
for i in range(-11, 1):
    for j in range(55, 63):
        coordrange.append((i,j))
        

def tempcalc (temprange: tuple, dataset):
    long = temprange[0]
    lat = temprange[1]
    range = dataset.loc[(dataset["Lats"] > lat) & (dataset["Lats"] <= lat + 1.05)]
    temptracker = np.array([])
    for col in range:
        if col == 'Lats':
            continue
        if (col <= long + 1.05 and col >= long):
            if dataset.name == "phitemp":
                columnsum = 0
                count = 0
                for value in range[[col]].values:
                    if not math.isnan(value):
                        columnsum += value
                        count += 1
                if count == 0:
                    temptracker = np.append(temptracker, np.nan)
                else:
                    temptracker = np.append(temptracker, columnsum/count)        
                continue
            temptracker = np.append(temptracker, range[[col]].mean(numeric_only = True)[0])
    return np.mean(temptracker)

cordavgtemp = {}
for pair in coordrange:
    avg = tempcalc(pair, avgtemp)
    newpair = (pair[0] + 11, pair[1] - 55)
    cordavgtemp[newpair] = avg
    
cordamptemp = {}
for pair in coordrange:
    avg = tempcalc(pair, amptemp)
    newpair = (pair[0] + 11, pair[1] - 55)
    cordamptemp[newpair] = avg
    

cordphitemp = {}
for pair in coordrange:
    avg = tempcalc(pair, phitemp)
    newpair = (pair[0] + 11, pair[1] - 55)
    cordphitemp[newpair] = avg



modelparams = {}
for pair in coordrange:
    newpair =(pair[0] + 11, pair[1] - 55)
    modelparams[newpair] = (cordavgtemp[newpair], cordamptemp[newpair], cordphitemp[newpair])
    # print(newpair, modelparams[newpair])
        


def predictedtemp(pair, time):
    y = 0.0018418*time -0.5415 + cordavgtemp[pair] + cordamptemp[pair] * np.sin(2*np.pi/12*time + cordphitemp[pair])
    return y





