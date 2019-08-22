from math import floor

def xscale(val):

    max_val = 33000
    min_val = 0
    sc_val = (val - min_val)/(max_val - min_val)
    return floor(sc_val * 3)