from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from classCesium import CesiumInstrument
import pandas as pd
from collections import defaultdict
from sqlalchemy import inspect
from io import StringIO
from config import Config
import pyvisa
from apscheduler.schedulers.background import BackgroundScheduler

def query_to_dict(rset):
    result = defaultdict(list)
    for obj in rset:
        instance = inspect(obj)
        for key, x in instance.attrs.items():
            result[key].append(x.value if x.value is not None else None)
    return result

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

class Instrumentsdb(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    MJD = db.Column(db.Float)
    D01 = db.Column(db.String(255))
    D02 = db.Column(db.Float)
    D03 = db.Column(db.Float)
    D04 = db.Column(db.Float)
    D05 = db.Column(db.Float)
    D06a = db.Column(db.Float)
    D06b = db.Column(db.Float)
    D07 = db.Column(db.String(255))
    D08 = db.Column(db.Float)
    D09 = db.Column(db.Float)
    D10 = db.Column(db.Float)
    D11 = db.Column(db.Float)
    D12 = db.Column(db.Float)
    D13a = db.Column(db.Float)
    D13b = db.Column(db.Float)
    D13c = db.Column(db.Float)
    D13d = db.Column(db.Float)
    D14 = db.Column(db.Float)
    D15a = db.Column(db.Float)
    D15b = db.Column(db.Float)
    D15c = db.Column(db.Float)
    D16 = db.Column(db.Float)
    D17 = db.Column(db.Float)
    D18 = db.Column(db.Float)
    D19 = db.Column(db.Float)
    D20 = db.Column(db.Float)
    D21 = db.Column(db.Float)

@app.route("/api/savedbintruments")
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



@app.route("/api/exportInstrumentsdbcsv")
def export_csv():
    try:
        data=Instrumentsdb.query.all()
         # Convertir el resultado a un diccionario usando query_to_dict
        data_dict = query_to_dict(data)

        # Crear un DataFrame con los datos
        df = pd.DataFrame(data_dict)

        # Crear un objeto StringIO para escribir el CSV en memoria
        output = StringIO()

        # Especificar la codificación utf-8 al escribir el CSV
        df.to_csv(output, index=False, encoding='utf-8')

        # Crear una respuesta con el CSV en formato texto
        response = make_response(output.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=Instrumentsdb.csv'
        response.headers['Content-type'] = 'text/csv; charset=utf-8'  # Especificar la codificación utf-8

        return response

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_dataintrument, 'interval', minutes=0.5)
    scheduler.start()
    app.run(debug=True, use_reloader=False)

