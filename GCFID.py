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
PeakList = {'MeOH' : [1.415, 1.46, 1.4, 1.51, 1.47 ],
    'MethylFormate': [1.47, 1.50, 1.46, 1.507, 1.505],            
    'Phenol' : [5.78, 5.92, 5.5, 6.2, 5.87],    
    'Mystery': [1.34, 1.40, 1.3, 1.42, 1.42],
    'TFEFormate' : [1.509, 1.55, 1.502, 1.56, 1.56],
    'PhenylFormate' : [5.92, 6.0, 5.831, 6.2, 6.2],
    'iPrFormate' : [1.885, 1.95, 1.85, 2.0, 2.0],
    'Dodecane' : [6.98, 7.05, 6.9, 7.15, 7.15]
    }

### File for storing calibration curve data
CCurve = r'C:\Users\Magnu\Nextcloud\PostDOC\ElectrochemicalHydrogenation\MS\CalibrationCurve.csv'
CC = pd.read_csv(CCurve)

### Data file Name
DataFile = r'C:\Users\Magnu\Nextcloud\PostDOC\ElectrochemicalHydrogenation\MS\Data.csv'

#Importing data with TKinter and make a regex to sort the filenames
fileRegex = re.compile(r'(.+\/)(.+)(\.CSV)')
files = TKinterImport.importData()

b = input('What is the starting Ester?  "1" for TFEFormate, "2" for PhenylFormate, "3" for iPrFormate: ')
b = int(b)


plt.figure(figsize=(7,4))
data=[]
for i in files:
    FileName = fileRegex.search(i).group(2)
    
    ### Read in Data
    df = BaselineAndArea.ReadFID(i)    
        
    ### Background and integration
    AreaList = [FileName]
    intList = []
    for keys in PeakList:
        intList.append(BaselineAndArea.FindArea(df,PeakList[keys]))
    
    ### Calculate ammount of each file and compound
    AreaList.append(nDodecane*(CC['a'][0]*intList[0]/intList[-1]+CC['b'][0]))
    AreaList.append(nDodecane*(CC['a'][1]*intList[1]/intList[-1]+CC['b'][1]))
    AreaList.append(nDodecane*(CC['a'][3+b]*intList[3+b]/intList[-1]+CC['b'][3+b]))
      
    AreaList.append(intList[3]/intList[-1])
               
    AreaList.append(AreaList[1]/Scale)
    AreaList.append((Scale-AreaList[3])/Scale*100)

    
    data = data + [AreaList]
    
    #Plot
    plt.plot(df['rt'],df['y'])

    
data = pd.DataFrame(data)
data.columns=['Name','MeOH','MethylFormate','Ester','iMyster/iDodecane','yMeOH','Conversion']
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
