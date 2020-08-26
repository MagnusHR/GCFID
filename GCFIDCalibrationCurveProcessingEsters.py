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
PeakList = {'MethylFormate' : [1.466, 1.505, 1.45, 1.51, 1.51 ],
    'TFEFormate' : [1.509, 1.55, 1.502, 1.56, 1.56],
    'iPrFormate' : [1.885, 1.95, 1.85, 2.0, 2.0],
    'Dodecane' : [6.98, 7.05, 6.9, 7.15, 7.15]
    }

### mmol in Mother Solutions
Ammount = {'1' : [0.097, 0.09578125, 0.099080695],
           '2' : [0.117666667, 0.103046875, 0.096810805]
           }
### mmol of IS in each sample
AmmountIS = 0.051828803

###Store Data pathways
DataFile = r'C:\Users\Magnu\Nextcloud\PostDOC\ElectrochemicalHydrogenation\MS\CalibrationData.csv'
RegressionFile = r'C:\Users\Magnu\Nextcloud\PostDOC\ElectrochemicalHydrogenation\MS\CalibrationCurve.csv'

### Dillution Factors
Dill = [0.9, 0.6, 0.3, 0.1, 0.05, 0.01]

folder = r'C:/Users/Magnu/Nextcloud/PostDOC/ElectrochemicalHydrogenation/MS/Ester Calibration/AdditionalEsters//*.csv'
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
data.columns=['Name','IMethylFormate','ITFEFormate','IiPrFormate','IDodecane','nMethylFormate','nTFEFormate','niPrFormate']

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

try:
    storedData = pd.read_csv(DataFile)
    storedData = storedData.append(data)
    storedRegression = pd.read_csv(RegressionFile)
    storedRegression = storedRegression.append(Regression)
except FileNotFoundError:
    storedData = data
    storedRegression = Regression

storedData.to_csv(DataFile, index = False)
storedRegression.to_csv(RegressionFile, index = False)
        
