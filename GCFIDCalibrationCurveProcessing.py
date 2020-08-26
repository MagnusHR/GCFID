import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import TKinterImport
import BaselineAndArea 
import glob
from scipy import stats
#import glob

#List of start and end points of peaks
#Format: Name, Starting point for integration, End point for integration, Starting Point for Background, End Point for Background,Last end poitn for Integration
PeakList = {'MeOH' : [1.415, 1.5, 1.40, 1.51, 1.51 ],
    'Phenol' : [5.78, 5.84, 5.5, 6.2, 5.87],
    'PhenylFormate' : [5.84, 5.95, 5.831, 6.2, 6.2],
    'Dodecane' : [6.98, 7.05, 6.9, 7.15, 7.15]
    }

### mmol in Mother Solutions
Ammount = {'1' : [0.18164794, 0.130319149, 0.077874222],
           '2' : [0.191635456, 0.126702128, 0.078119882]
           }
### mmol of IS in each sample
AmmountIS = 0.05218106

### Dillution Factors
Dill = [0.9, 0.6, 0.3, 0.1, 0.05, 0.01]

folder = r'C:/Users/Magnu/Nextcloud/PostDOC/ElectrochemicalHydrogenation/MS/Ester Calibration//*.csv'
files = glob.glob(folder)
#files = TKinterImport.importData()

 
plt.figure(figsize=(7,4))
data=[]
for i in files:
    FileName = i.replace(folder[:-7],'')
    FileName = FileName[1:-4]
    
    ### Read in Data
    df = BaselineAndArea.ReadFID(i)    
        
    #Background and integration
    AreaList = [FileName]
    for keys in PeakList:
        AreaList.append(BaselineAndArea.FindArea(df,PeakList[keys]))
    
    ### Calculate Concentration of each file and compound
    AreaList.append(Dill[int(FileName[-1])-1]*Ammount[FileName[-2]][0])
    AreaList.append(Dill[int(FileName[-1])-1]*Ammount[FileName[-2]][1])
    AreaList.append(Dill[int(FileName[-1])-1]*Ammount[FileName[-2]][2])
    
    data = data + [AreaList]
    
    #Plot
    plt.plot(df['rt'],df['y'])

# plt.xlim(1.3,1.57)
# plt.ylim(-0.5,2)
# plt.title(FileName)
    
data = pd.DataFrame(data)
data.columns=['Name','IMeOH','IPhenol','IPhenylFormate','IDodecane','nMeOH','nPhenol','nPhenylFormate']

a = data.values

function = []
for i in range(len(PeakList.keys())-1):
    x = (a[:,i+1]/a[:,4]).astype(float)
    y = (a[:,i+5]/AmmountIS).astype(float)
    function.append(np.polyfit(x,y,1))
    
Regression = pd.DataFrame(function)
Name = pd.DataFrame(PeakList.keys())
Name = Name.iloc[0:len(PeakList.keys())-1:,]
Regression.insert(0,'Name',Name)

Regression.columns = ['Name','a','b']


     
Regression.to_csv(r'C:\Users\Magnu\Nextcloud\PostDOC\ElectrochemicalHydrogenation\MS\CalibrationCurve.csv', index = False)
data.to_csv(r'C:\Users\Magnu\Nextcloud\PostDOC\ElectrochemicalHydrogenation\MS\CalibrationData.csv', index = False)
