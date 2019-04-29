#encoding:utf-8
import numpy as np

def Tanh(number):
    if type(number) == int or type(number) == float:
        return np.tanh(number)
    else:
        raise ValueError("Number need to be Integer or a Float")
    