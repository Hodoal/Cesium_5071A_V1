#Lectura con libreria pyvisa.
from ssl import SSL_ERROR_EOF
#import serial
from datetime import datetime,time
import time

#***********************************************
class CesiumInstrument():
    def __init__(self):
        pass

    def read_data(self, Instru):
        #Lectura de datos
        Instru.write('*csl')
        #-----------------------------------------
        Instru.write('*idn?')
        print(Instru.read())
        print(Instru.read())
        #Datos.write(Instru.read())
        Iden = Instru.read()
        #-----------------------------------------
        Instru.write('DIAGnostic:CBTSerial?')
        print(Instru.read())
        D01 = Instru.read()
        #-----------------------------------------
        Instru.write('DIAGnostic:CURRent:BEAM?')
        print(Instru.read())
        D02 = Instru.read()
        #-----------------------------------------
        Instru.write('DIAGnostic:CURRent:CFIeld?')
        print(Instru.read())
        D03 = Instru.read()
        #-----------------------------------------
        Instru.write('DIAGnostic:CURRent:PUMP?')
        print(Instru.read())
        D04 = Instru.read()
        #-----------------------------------------
        Instru.write('DIAGnostic:GAIN?')
        print(Instru.read())
        D05 = Instru.read()
        #-----------------------------------------
        Instru.write('DIAGnostic:RFAMplitude?')
        print(Instru.read())
        D06 = Instru.read()
        #print(D06)
        #-----------------------------------------
        Instru.write('DIAGnostic:STATus:SUPPly?')
        print(Instru.read())
        D07 = Instru.read()
        #-----------------------------------------
        Instru.write('DIAGnostic:TEMPerature?')
        print(Instru.read())
        D08 = Instru.read()
        #-----------------------------------------
        Instru.write('DIAGnostic:VOLTage:COVen?')
        print(Instru.read())
        D09 = Instru.read()
        #-----------------------------------------
        Instru.write('DIAGnostic:VOLTage:EMULtiplier?')
        print(Instru.read())
        D10 = Instru.read()
        #-----------------------------------------
        Instru.write('DIAGnostic:VOLTage:HWIonizer?')
        print(Instru.read())
        D11 = Instru.read()
        #-----------------------------------------
        Instru.write('DIAGnostic:VOLTage:MSPec?')
        print(Instru.read())
        D12 = Instru.read()
        #-----------------------------------------
        Instru.write('DIAGnostic:VOLTage:PLLoop?')
        print(Instru.read())
        D13 = Instru.read()
        #-----------------------------------------
        Instru.write('DIAGnostic:VOLTage:ROSCillator?')
        print(Instru.read())
        D14 = Instru.read()
        #-----------------------------------------
        Instru.write('DIAGnostic:VOLTage:SUPPly?')
        print(Instru.read())
        D15 = Instru.read()
        #-----------------------------------------
        Instru.write('SOURce:ROSCillator:CONTrol?')
        print(Instru.read())
        D16 = Instru.read()
        #-----------------------------------------
        Instru.write('SOURce:ROSCillator:STEer?')
        print(Instru.read())
        D17 = Instru.read()
        #-----------------------------------------
        Instru.write('SOURce:ROSCillator:FREQuency?')
        print(Instru.read())
        D18 = Instru.read()
        #-----------------------------------------
        Instru.write('SOURce:ROSCillator:MVOLtage?')
        print(Instru.read())
        D19 = Instru.read()
        #-----------------------------------------
        #Busqueda exhaustiva de:
        #     Zeeman freq
        #     CBT Oven Err
        #Porque no tienen comandos específicos
        Instru.write('SYST:PRINT?')
        print(Instru.read())
        Instru.read()
        Instru.read()
        Instru.read()
        Instru.read()
        Instru.read()
        Instru.read()
        Instru.read()
        Instru.read()
        Instru.read()
        D20 = Instru.read()
        Instru.read()
        Instru.read()
        D21 = Instru.read()
        Instru.read()
        Instru.read()
        Instru.read()
        Instru.read()
        Instru.read()
        Instru.read()
        Instru.read()
        Instru.read()
        print(D20)
        print(D21)
        #-----------------------------------------
        #***********************************************
        #Escritura de datos
        #Datos.write(Iden)
        #-----------------------------------------
        #Detalle para obtener la hora UTC-5 y MJD
        UTCmenos5 = datetime.now()
        RefeMJD = 57595
        RefeUnix = 1469491200
        MJD = RefeMJD + (time.time()-RefeUnix)/24/60/60
        UTCmenos5 = str(UTCmenos5)
        MJD = str(MJD)
        #-----------------------------------------
        #Ajuste de datos:
        D01 = str(D01).rstrip()
        D02 = str(D02).rstrip()
        D03 = str(D03).rstrip()
        D04 = str(D04).rstrip()
        D05 = str(D05).rstrip()
        D06 = str(D06).rstrip()
        D06a = D06[0:10]
        D06b = D06[11:22]
        D07 = str(D07).rstrip()
        D08 = str(D08).rstrip()
        D09 = str(D09).rstrip()
        D10 = str(D10).rstrip()
        D11 = str(D11).rstrip()
        D12 = str(D12).rstrip()
        D13 = str(D13).rstrip()
        D13a = D13[0:7]
        D13b = D13[8:15]
        D13c = D13[16:25]
        D13d = D13[26:35]
        D14 = str(D14).rstrip()
        D15 = str(D15).rstrip()
        D15a = D15[0:9]
        D15b = D15[10:20]
        D15c = D15[21:31]
        D16 = str(D16).rstrip()
        D17 = str(D17).rstrip()
        D18 = str(D18).rstrip()
        D19 = str(D19).rstrip()
        D20 = str(D20).rstrip()
        D20 = D20[18:23]
        D21 = str(D21).rstrip()
        D21 = D21[48:52]

        
        #-----------------------------------------
        data = {
            'MJD': MJD,
            'D01': D01,
            'Beam_current_setpoint': D02,
            'Cfield_current_setpoint': D03,
            'Ion_pump_current': D04,
            'Signal_gain': D05,
            'RF_Attenuator_setpoints_1': D06a,
            'RF_Attenuator_setpoints_2': D06b,
            'Power_supply_status': D07,
            'Temperature': D08,
            'Cesium_oven_heater': D09,
            'ECesium_oven_heater_voltage': D10,
            'Hot_wire_ionizer_voltage': D11,
            'Mass_spectrometer_voltage': D12,
            'PLLoop_1': D13a,
            'PLLoop_2': D13b,
            'PLLoop_3': D13c,
            'PLLoop_4': D13d,
            'ROSCillator': D14,
            'Power_supplie_1': D15a,
            'Power_supplie_2': D15b,
            'Power_supplie_3': D15c,
            'Reference_oscillator_frequency': D16,
            'Fractional_frequency_offset': D17,
            'Programmed_frequency_at_specified': D18,
            'Oscillator_oven_voltage': D19,
            'Zeeman_Freq': D20,
            'CBT_Oven_Err': D21,
        }
        return data