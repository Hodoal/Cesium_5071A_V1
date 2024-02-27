import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from Interface import Ui_Cesium_5071A
import requests
from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from classCesium import CesiumInstrument
import pandas as pd
from collections import defaultdict
from sqlalchemy import inspect
from io import StringIO
from apscheduler.schedulers.background import BackgroundScheduler
import pyvisa
import threading
from model import Instrumentsdb
from config import Config
from nameP import  Name_parameter

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Cesium_5071A()
        self.ui.setupUi(self)
        self.ui.star.clicked.connect(self.start_flask)
        #self.ui.stop.clicked.connect(self.stop_flask)
        self.ui.export_2.clicked.connect(self.export_data)
        self.populate_combobox()  # Llenar el QComboBox al inicializar la aplicación

    def populate_combobox(self):
        # Limpiar el contenido actual del QComboBox
        self.ui.parameter.clear()
        # Obtener las claves del diccionario database_params
        self.ui.parameter.addItem("Select a parameter...")
        param_names = Name_parameter.database_params.keys()
        # Agregar las claves al QComboBox
        self.ui.parameter.addItems(param_names)

    def start_flask(self):
        flask_thread = threading.Thread(target=flask_runner)
        flask_thread.start()

        # Deshabilitar el botón para evitar múltiples clics
        self.ui.star.setEnabled(False)
        # Mostrar un mensaje de confirmación
        QMessageBox.information(self, "Server Started", "Flask server started successfully!")

    def export_data(self):
        try:
            # Realizar una solicitud GET al endpoint /api/exportInstrumentsdbcsv del servicio Flask
            response = requests.get("http://127.0.0.1:5000/api/exportInstrumentsdbcsv")

            # Verificar el estado de la respuesta
            if response.status_code == 200:
                # Obtener la ruta del archivo desde el usuario
                file_path, _ = QFileDialog.getSaveFileName(self, "Guardar archivo", "Instrumentsdb.csv", "CSV Files (*.csv)")

                # Verificar si se seleccionó un archivo
                if file_path:
                    # Crear un objeto StringIO para leer el contenido del archivo CSV
                    csv_content = StringIO(response.content.decode('utf-8'))

                    # Crear un DataFrame con los datos del archivo CSV
                    df = pd.read_csv(csv_content)

                    # Guardar el archivo CSV en el disco
                    df.to_csv(file_path, index=False, encoding='utf-8')

                    # Mostrar un mensaje de éxito
                    QMessageBox.information(self, "Success", "Data exported successfully!")
            else:
                # Mostrar un mensaje de error si la solicitud falla
                QMessageBox.critical(self, "Error", "Failed to export data: " + response.text)
        except Exception as e:
            # Mostrar un mensaje de error si ocurre alguna excepción
            QMessageBox.critical(self, "Error", "Failed to export data: " + str(e))



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

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


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

def query_to_dict(rset):
    result = defaultdict(list)
    for obj in rset:
        instance = inspect(obj)
        for key, x in instance.attrs.items():
            result[key].append(x.value if x.value is not None else None)
    return result

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

def main():
    # Iniciar la aplicación PyQt
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
