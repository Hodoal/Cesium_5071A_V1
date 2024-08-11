import numpy as np
class Shift_F(): 
    @staticmethod
    def D_BBR(data_list):
        data_list = [data + 273.15 for data in data_list]
        b = -1.70 * 10**(-14)
        T_0 = 300
        E = 0.013
        dv_list = [b * ((data / T_0)**4) * (1 + E * (data / T_0)**2) for data in data_list]
        return sum(dv_list) / len(dv_list)  # Retornar el valor promedio
    @staticmethod
    def ZeemanAC(data_list):
        data_list = [data + 273.15 for data in data_list]
        b = -1.30 * 10**(-17)
        T_0 = 300
        dv_list = [b * ((T / T_0)**2) for T in data_list]
        return sum(dv_list) / len(dv_list) if dv_list else 0


    @staticmethod
    def Stark(data_list):
        data_list = [data + 273.15 for data in data_list]
        ks = -2.45 * 10**(-20)
        T_0 = 300
        E_list = [831.9 * (data / T_0)**2 for data in data_list]
        dv_list = [ks * E**2 for E in E_list]
        return sum(dv_list) / len(dv_list)

    
    @staticmethod
    def Zeeman(data_list):
        Bc = 6e-6
        data_list = np.array(data_list, dtype=float)
        I = np.mean(data_list)
        B = (Bc / I) * data_list
        dv_list = ((427.45 * 10**8) * (B**2 + np.std(B)**2)) / 9192631770
        mean_dv = np.mean(dv_list)
        return mean_dv

    @staticmethod
    def gravitation():
        V_g = -(9.80665/(299792458)**2)*2553
        return V_g


    