def slc(dict_, mask):
    dict__ = dict_.copy()
    for k in dict_.keys():
        dict__[k] = dict__[k][mask]
    return dict__