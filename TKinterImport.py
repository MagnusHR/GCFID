import pandas as pd
from tkinter import Tk
from tkinter import filedialog

def importData():
    '''
    must select at least one data file
    
    imports one or more files and outputs a list of filenames
    '''
    root = Tk()
    root.withdraw()
    files =filedialog.askopenfiles(
            mode='r',  # Permissions 'r': 'read only'
            title='Select file(s)',  # Title for promp window
            filetype=[("Text files", ".txt .csv"), ("All files", ".*")]  # Sorting options for promp window
            )
    
    directory=[]
    for f in files:
        filepath=f.name
        directory.append(filepath)
    
    if len(directory) == 0:
        raise TypeError('No data selected')
    return directory