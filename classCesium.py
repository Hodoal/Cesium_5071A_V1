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
            'D02': D02,
            'D03': D03,
            'D04': D04,
            'D05': D05,
            'D06a': D06a,
            'D06b': D06b,
            'D07': D07,
            'D08': D08,
            'D09': D09,
            'D10': D10,
            'D11': D11,
            'D12': D12,
            'D13a': D13a,
            'D13b': D13b,
            'D13c': D13c,
            'D13d': D13d,
            'D14': D14,
            'D15a': D15a,
            'D15b': D15b,
            'D15c': D15c,
            'D16': D16,
            'D17': D17,
            'D18': D18,
            'D19': D19,
            'D20': D20,
            'D21': D21,
        }
        return data
    
    def create_table(conn):
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prueba (
                id INT AUTO_INCREMENT PRIMARY KEY,
                UTC_menos_5 DATETIME,
                MJD VARCHAR(255),
                D01 VARCHAR(255),
                D02 VARCHAR(255),
                D03 VARCHAR(255),
                D04 VARCHAR(255),
                D05 VARCHAR(255),
                D06a VARCHAR(255),
                D06b VARCHAR(255),
                D07 VARCHAR(255),
                D08 VARCHAR(255),
                D09 VARCHAR(255),
                D10 VARCHAR(255),
                D11 VARCHAR(255),
                D12 VARCHAR(255),
                D13a VARCHAR(255),
                D13b VARCHAR(255),
                D13c VARCHAR(255),
                D13d VARCHAR(255),
                D14 VARCHAR(255),
                D15a VARCHAR(255),
                D15b VARCHAR(255),
                D15c VARCHAR(255),
                D16 VARCHAR(255),
                D17 VARCHAR(255),
                D18 VARCHAR(255),
                D19 VARCHAR(255),
                D20 VARCHAR(255),
                D21 VARCHAR(255)
            )
        ''')
        conn.commit()
        cursor.close()

    # Función para insertar datos en la base de datos
    def insertar_datos(conexion, datos):
        cursor = conexion.cursor()

        # Consulta SQL para insertar datos
        consulta = '''
            INSERT INTO prueba (
                UTC_menos_5, MJD, D01, D02, D03, D04, D05, D06a, D06b, D07, D08, D09, D10, D11, D12,
                D13a, D13b, D13c, D13d, D14, D15a, D15b, D15c, D16, D17, D18, D19, D20, D21
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''

        # Formatear los datos
        datos_formateados = (
            datos['UTC_menos_5'], datos['MJD'], datos['D01'], datos['D02'], datos['D03'],
            datos['D04'], datos['D05'], datos['D06a'], datos['D06b'], datos['D07'], datos['D08'],
            datos['D09'], datos['D10'], datos['D11'], datos['D12'], datos['D13a'], datos['D13b'],
            datos['D13c'], datos['D13d'], datos['D14'], datos['D15a'], datos['D15b'], datos['D15c'],
            datos['D16'], datos['D17'], datos['D18'], datos['D19'], datos['D20'], datos['D21']
        )
        # Ejecutar la consulta
        cursor.execute(consulta, datos_formateados)
        # Confirmar los cambios
        conexion.commit()
        # Cerrar el cursor
        cursor.close()  
    
