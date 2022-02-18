import warnings

def Warn(msg):
    warnings.warn(msg)

def Error(msg):
    print(msg)
    raise Exception