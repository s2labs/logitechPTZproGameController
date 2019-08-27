from math import floor

def xscale(val):

    max_val = 33000
    min_val = 0
    sc_val = (val - min_val)/(max_val - min_val)
    return floor(sc_val * 5)

def zoom_scale(sarg, current_zoom):

    val = abs(sarg)
    max_val = 33000
    min_val = 0
    sc_val = (val - min_val)/(max_val - min_val)
    zoom_level = current_zoom
    if sarg > 0:
        zoom_level = zoom_level - floor(sc_val*100)
    else:
        zoom_level = zoom_level + floor(sc_val * 100)
    if zoom_level > 1000:
        zoom_level = 1000
    if zoom_level < 100:
        zoom_level = 100
    return zoom_level

