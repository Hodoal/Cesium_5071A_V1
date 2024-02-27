
import numpy as np

class Shift(): 

    def D_BBR(T): #bien 
        b = -1.70*10**(-14)
        T_0 = 300
        E = 0.013
        dv = -b*((T/T_0)**4)*(1 + E*(T/T_0)**2)
        return dv
    
    def ZeemanAC(T):
        dv = ((-1.30*10**(-17))*(T/300)**2)
        return dv
    
    def stark(T): 
        ks=-2.45*10**(-20)
        E = 831.9*(T/300)**2
        dv= ks*E**2
        return dv
    
    def magnetiFild(data): 
        Bc = 6e-6
        I = np.mean(data/10000)
        return (Bc/I)*data
        

    def Zeeman(B): 
        dv = ((427.45*10**(8)*(B**2+np.std(B)**2))/9192631770)
        return dv
    
    