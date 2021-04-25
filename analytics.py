import pandas as pd
import numpy as np

"""
Creates a new data table based on the average of the original songs playlist we created
and the values of the songs our comparitive playlist matches with 
"""
def dataTable(*args):
    result = dict()
    for dictionaries in args:
        result.update(dictionaries)
    return pd.DataFrame(data = result).transpose()


"""
Finds the average of a data table and return a dictionary of the 
averages and the table name
"""
def findAverage(table, tableName):
    temp = [0] * len(table.columns)
    total = 0
    for index, row in table.iterrows():
        total += 1
        for index, val in enumerate(row.values):
            temp[index] += val

    result = dict()
    for index, val in enumerate(table.columns):
        result[val] = temp[index] / total

    
    return {tableName : result}