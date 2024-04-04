# api/api.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import pyvisa
from model import Instrumentsdb
from classCesium import CesiumInstrument
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

def flask_runner():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_dataintrument, 'interval', minutes=0.5)
    scheduler.start()

    # Crear todas las tablas de la base de datos dentro del contexto de la aplicación Flask
    with app.app_context():
        db.create_all()

    app.run(debug=True, use_reloader=False)


def send_dataintrument():
    try:
        with app.app_context():
            RM = pyvisa.ResourceManager()
            Instru = RM.open_resource('ASRL3::INSTR')

            # Crear una instancia del instrumento
            instrumento = CesiumInstrument()

            # Leer datos del instrumento pasando la conexión como argumento
            datos = instrumento.read_data(Instru)

            # Crear una instancia del modelo con los datos del instrumento
            instrumentdb = Instrumentsdb(**datos)

            # Agregar la instancia a la base de datos
            db.session.add(instrumentdb)
            db.session.commit()
            
            # Cerrar la conexión con el instrumento
            Instru.close()
            RM.close()

    except Exception as e:
        print("Error:", e)




@app.route('/api/send_datainstrument', methods=['POST'])
def send_data():
    data = request.json  # Espera que los datos se envíen como JSON en el cuerpo de la solicitud
    try:
        
        if not check_data_dbmodeltable(Instrumentsdb) and not check_data_dbmodeltable(Shift):
                data0=Instrumentsdb.query.all()
                # Convertir el resultado a un diccionario usando query_to_dict
                data_dict = query_to_dict(data0)
                # Convertir el resultado a un diccionario usando query_to_dict
                
                df=pd.DataFrame(data_dict)
                df1=pd.DataFrame()                
                #df1['DV_Zeeman']                =         Shift_F.Zeeman(df['Cfield_current_setpoint'])
                df1['DV_Zeman_AC']              =         Shift_F.ZeemanAC(df['Temperature'])
                df1['DV_Stark ']                =         Shift_F.stark(df['Temperature'])
                df1['DV_Gavitational_effects']  =         Shift_F.gravitation()
                df1["DV_BBR"]                   =         Shift_F.D_BBR(df['Temperature'])
                # Guarda los datos en la base de datos
                df1.to_sql('Shift', con=db.engine, if_exists='append', index=False)

       


        instrument = Instrumentsdb(**data)
        # Consulta los últimos 49 registros ordenados por id de forma descendente
        last_49_records = Instrumentsdb.query.order_by(Instrumentsdb.id.desc()).limit(49).all()
        
        df0=pd.DataFrame(query_to_dict(last_49_records))
        df01=pd.DataFrame(data)
        df = pd.concat([df0, df01], ignore_index=True)
        df1=pd.DataFrame()                
        #df1['DV_Zeeman']                =         Shift_F.Zeeman(df['Cfield_current_setpoint'])
        df1['DV_Zeman_AC']              =         Shift_F.ZeemanAC(df['Temperature'])
        df1['DV_Stark ']                =         Shift_F.stark(df['Temperature'])
        df1['DV_Gavitational_effects']  =         Shift_F.gravitation()
        df1["DV_BBR"]                   =         Shift_F.D_BBR(df['Temperature'])

        Shiftdb = Shift(**df1.iloc[len(df1)-1].to_dict())

        # Agregar la instancia a la base de datos
        db.session.add(Shiftdb)
        db.session.commit()
        db.session.add(instrument)
        db.session.commit()
        return jsonify({'message': 'Datos guardados correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500