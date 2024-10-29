from flask import jsonify, make_response, request
from sqlalchemy.exc import SQLAlchemyError
import pyvisa
from datetime import datetime
from classCesium import CesiumInstrument
from model import app, db, Instrumentsdb
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd 
from io import StringIO

def query_to_dict(query_result):
    """Convierte el resultado de una consulta a un diccionario, combinando fecha y hora."""
    data = []
    for row in query_result:
        item = {}
        for column in row.__table__.columns:
            value = getattr(row, column.name)
            if isinstance(value, datetime):
                # Convertir el valor datetime a formato string combinando fecha y hora
                item[column.name] = value.strftime("%Y-%m-%d %H:%M:%S.%f")
            else:
                item[column.name] = value
        data.append(item)
    return data
@app.route('/api/send_datainstrument', methods=['POST'])
def send_data():
    data = request.json
    try:
        if 'date_created' in data:
            data['date_created'] = datetime.fromisoformat(data['date_created'])
        instrument = Instrumentsdb(**data)
        db.session.add(instrument)
        db.session.commit()
        return jsonify({'message': 'Datos guardados correctamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Error al guardar los datos en la base de datos', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Error inesperado', 'details': str(e)}), 500


@app.route("/api/exportInstrumentsdbcsv")
def export_csv():
    try:
        data = Instrumentsdb.query.all()
        # Convertir el resultado a un diccionario usando query_to_dict
        data_dict = query_to_dict(data)

        # Crear un DataFrame con los datos
        df = pd.DataFrame(data_dict)

        # Asegurarse de que 'date_created' esté en el formato correcto
        df['date_created'] = pd.to_datetime(df['date_created'], errors='coerce')
        df['date_created'] = df['date_created'].dt.strftime('%Y-%m-%d %H:%M:%S.%f')


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

    
def send_dataintrument():
    try:
        with app.app_context():
            RM = pyvisa.ResourceManager()
            Instru = RM.open_resource('ASRL3::INSTR')
            instrumento = CesiumInstrument()
            datos = instrumento.read_data(Instru)
            instrumentdb = Instrumentsdb(**datos)
            db.session.add(instrumentdb)
            db.session.commit()
            Instru.close()
            RM.close()
    except Exception as e:
        print("Error:", e)

def dicts_to_modelos(lista_datos, model):
    try:
        with app.app_context():
            for datos in lista_datos:
                instrumentdb = model(**datos)
                db.session.add(instrumentdb)
            db.session.commit()
    except Exception as e:
        print("Error:", e)

def flask_runner():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_dataintrument, 'interval', minutes=0.5)
    scheduler.start()
    with app.app_context():
        db.create_all()
    app.run(debug=True, use_reloader=False)
