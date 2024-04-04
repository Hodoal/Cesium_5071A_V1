
import numpy as np

class Shift_F(): 
    @staticmethod
    def D_BBR(data): #bien 
        data=data+273.15
        b = -1.70*10**(-14)
        T_0 = 300
        E = 0.013
        dv = -b*((data/T_0)**4)*(1 + E*(data/T_0)**2)
        return dv
    @staticmethod
    def ZeemanAC(T):
        dv = ((-1.30*10**(-17))*((T)/300)**2)
        return dv
    @staticmethod
    def stark(data): 
        ks=-2.45*10**(-20)
        data=data+273.15
        E = 831.9*(data/300)**2
        dv= ks*E**2
        return dv
    
    @staticmethod

    def Zeeman(data):
        Bc = 6e-6
        dv_list = []
        
        # Iterar sobre el rango de tamaño de muestra
        for i in range(1, len(data) + 1):
            # Calcular la media y la desviación estándar de la ventana actual
            window_mean = data.iloc[max(0, i - 50):i].mean()
            window_std = data.iloc[max(0, i - 50):i].std()
            
            # Calcular el campo magnético y la diferencia de frecuencia
            B = (Bc / window_mean) * data.iloc[i - 1]
            dv = ((427.45 * 10 ** (8) * (B ** 2 + window_std ** 2)) / 9192631770)
            
            # Agregar la diferencia de frecuencia a la lista
            dv_list.append(dv)
        
        return dv_list
    @staticmethod
    def gravitation():
        V_g = -(9.80665/(299792458)**2)*2553
        return V_g
    