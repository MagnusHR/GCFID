import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import peakutils

def ReadFID(Filename):
    '''
    

    Parameters
    ----------
    Filename : String with filename

    Returns
    -------
    Dataframe with the GC FID data

    '''
    df = pd.read_csv(Filename, header = 1)
    df.columns = ['point','rt','y']

    #Skip TCD data
    skipIndex = df[df['point'].str.contains('#"FID1')].index.values
    df = pd.read_csv(Filename, skiprows = int(skipIndex)+3)
    df.columns = ['point','rt','y']
    return df 

def FindArea(df,peak):
    """
    Function to determine area of a list of peaks with background subtraction based on several points prior to the peak 
    
    Parameters
    ----------
    df : pandas dataframe with retention time and y values
    peak : list with start and endpoint for a give peak

    Returns
    -------
    area : float with containing area of give peak

    """
    #Defines DataFrame containing points from the background
    PrePeak = df.loc[(df['rt'] > peak[2]) & (df['rt'] < peak[0])]
    PostPeak = df.loc[(df['rt'] > peak[1]) & (df['rt'] < peak[3])]
    Background = pd.concat([PrePeak,PostPeak])
    
    #Get a Baseline using peakutils
    baseline = peakutils.baseline(Background['y'])
    
    #Define baseline as a function
    f = interp1d(Background['rt'], baseline, kind='slinear')
    
    
    start= FindPeakStart(df,peak)
    end = FindPeakEnd(df,peak)
    
    a = df[start:end]
       
    
    #Get dataframe with data that should be integrated
    #a = df.loc[(df['rt'] > peak[0]) & (df['rt'] < peak[1])]
    #Subtract background
    try:
        a_bg_corrected = a['y'].sub(f(a['rt']))
    except ValueError:
        a=df[start:Background.index[-1]]
        a_bg_corrected = a['y'].sub(f(a['rt']))
        
    #Make a Trapez integration
    area = np.trapz(a_bg_corrected, a['rt'])
    ### Plotting background for visualization
    plt.plot(a['rt'],f(a['rt']))
    #plt.plot(Background['rt'],baseline)
    return area 

def FindPeakStart(df,peak):
    '''
    Parameters
    ----------
    df : pandas dataframe with retention time and y values
    peak : list with start and endpoint for a give peak 

    Returns
    -------
    Index of the starting point for the peak

    '''
    b = df.loc[(df['rt'] > peak[0]) & (df['rt'] < peak[3])]
    derivatives = np.diff(b['y'])/np.diff(b['rt'])
    ### Returns the index of the point 2 steps prior to the point resulting in a derivative exceeding 0.01
    for i in range(0,len(derivatives)):
        if derivatives[i] > 0.01:
            return i + df.loc[df['rt'] > peak[0]].index[0] - 1
    ### If no derivatives exceed 0.1 the index of the default starting value is returned
    return df.loc[df['rt'] > peak[0]].index[0]

def FindPeakEnd(df,peak):
    '''
    Parameters
    ----------
    df : pandas dataframe with retention time and y values
    peak : list with start and endpoint for a give peak 

    Returns
    -------
    Index of the starting point for the peak

    '''
    initialTime = df['rt']
    b = df.loc[(df['rt'] > peak[1]) & (df['rt'] < peak[4])]
    derivatives = np.diff(b['y'])/np.diff(b['rt'])
    ### Returns the index of the point 2 steps after to the point resulting in a derivative below -0.015, searching the derivatives in opposite direction
    for i in range(0,len(derivatives)):
        if derivatives[i] < -0.015:
            return i + df.loc[df['rt'] > peak[1]].index[0] + 2
    ### If no derivatives exceed 0.1 the index of the default starting value is returned
    return df.loc[df['rt'] > peak[1]].index[0]