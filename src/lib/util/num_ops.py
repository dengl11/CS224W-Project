############################################################
###############  Toolkit for Numeric Operations  ###########
############################################################
import numpy as np
from collections import Counter
import statistics 

def mode(arr):
    """return mode of the array
    Args:
        arr: 

    Return: 
    """
    try:
        return statistics.mode(arr)
    except:
        c = Counter(arr)
        return c.most_common(1)[0][0]
