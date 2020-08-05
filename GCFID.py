#! C:\Users\Magnu\Anaconda3\python
# GCFID.py - Processing of GCFID data

import sys
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import TKinterImport
import BaselineAndArea 
import glob
from scipy import stats
#import glob

Scale = 0.25
Dodecane = 50 #uL
nDodecane = 0.05218106#Dodecane*0.75/170.33

#List of start and end points of peaks
#Format: Name, Starting point for integration, End point for integration, Starting Point for Background, End Point for Background,Last end poitn for Integration
PeakList = {'MeOH' : [1.415, 1.46, 1.4, 1.51, 1.51 ],
    'Phenol' : [5.78, 5.92, 5.5, 6.2, 5.87],
    'PhenylFormate' : [5.92, 6.0, 5.831, 6.2, 6.2],
    'Dodecane' : [6.98, 7.05, 6.9, 7.15, 7.15],
    'Mystery': [1.34, 1.40, 1.3, 1.42, 1.42],
    'MethylFormate': [1.47, 1.50, 1.46, 1.507, 1.505]
    }

### File for storing calibration curve data
CCurve = r'C:\Users\Magnu\Nextcloud\PostDOC\ElectrochemicalHydrogenation\MS\CalibrationCurve.csv'
CC = pd.read_csv(CCurve)

### Data file Name
DataFile = r'C:\Users\Magnu\Nextcloud\PostDOC\ElectrochemicalHydrogenation\MS\Data.csv'

#Importing data with TKinter and make a regex to sort the filenames
fileRegex = re.compile(r'(.+\/)(.+)(\.CSV)')
files = TKinterImport.importData()


plt.figure(figsize=(7,4))
data=[]
for i in files:
    FileName = fileRegex.search(i).group(2)
    
    ### Read in Data
    df = BaselineAndArea.ReadFID(i)    
        
    ### Background and integration
    AreaList = [FileName]
    for keys in PeakList:
        AreaList.append(BaselineAndArea.FindArea(df,PeakList[keys]))
    
    ### Calculate ammount of each file and compound
    AreaList.append(nDodecane*(CC['a'][0]*AreaList[1]/AreaList[4]+CC['b'][0]))
    AreaList.append(nDodecane*(CC['a'][1]*AreaList[2]/AreaList[4]+CC['b'][1]))
    AreaList.append(nDodecane*(CC['a'][2]*AreaList[3]/AreaList[4]+CC['b'][2]))
                    
    AreaList.append(AreaList[7]/Scale)
    AreaList.append((Scale-AreaList[9])/Scale*100)

    
    data = data + [AreaList]
    
    #Plot
    plt.plot(df['rt'],df['y'])

    
data = pd.DataFrame(data)
data.columns=['Name','IMeOH','IPhenol','IPhenylFormate','IDodecane','iMystery','MethylFormate','nMeOH','nPhenol','nPhenylFormate','yMeOH','Conversion']
print(data)
plt.show()

a = input('Write "y" to store data: ')
          
if a == 'y':
    try:
        storedData = pd.read_csv(DataFile)
        storedData = storedData.append(data)
    except FileNotFoundError:
        storedData = data     
    storedData.to_csv(DataFile, index=False)
