import numpy as np
import pandas as pd

def ReadInGridDB(FileName):
    # Read in the model distributions database: 
    DB = {} 
    x = pd.read_csv(FileName, header = None)
    for row in range(len(x)):
        Pa = round(eval(x[0][row])[0],2)
        Pb = round(eval(x[0][row])[1],2)
        DB[(Pa, Pb)] = eval(x[1][row])

    return DB