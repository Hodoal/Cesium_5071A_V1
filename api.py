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

