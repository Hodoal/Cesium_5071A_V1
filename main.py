import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QVBoxLayout
from PyQt6.QtCore import QTimer
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
from config import Config
from sqlalchemy.types import String
import matplotlib 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime, timedelta
from frequencyShift import Shift

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Cesium_5071A()
        self.ui.setupUi(self)
        self.ui.start.clicked.connect(self.start_flask)
        #self.ui.stop.clicked.connect(self.stop_flask)
        self.populate_combobox()
        self.ui.export_2.clicked.connect(self.export_data)
        # Configurar el temporizador para actualizar el gráfico periódicamente
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)  # Intervalo de tiempo en milisegundos

        # Crear un lienzo para el gráfico y agregarlo al frame Graph
        self.graph_layout = QVBoxLayout()
        self.ui.Graph.setLayout(self.graph_layout)  # Establecer el layout en el QFrame Graph

        # Crear el lienzo del gráfico y agregarlo al layout
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.graph_layout.addWidget(self.toolbar)
        self.graph_layout.addWidget(self.canvas)
        self.last_clear_time = None
        self.legend = None

    def update_plot(self):
        param_name = self.ui.parameter.currentText().replace(' ', '_')
        if param_name == "Select_a_parameter...":
            return

        current_time = datetime.now()

        if self.last_clear_time is None or current_time - self.last_clear_time >= timedelta(days=1):
            self.ax.clear()
            self.last_clear_time = current_time

        # Obtener los últimos 100 datos del parámetro seleccionado de la base de datos
        with app.app_context():
            data = self.get_last_100_data(param_name)

        # Extraer los valores de los datos
        date_values = [item.date_created for item in data]
        values = [getattr(item, param_name) for item in data]

        # Remover las líneas anteriores del gráfico
        for line in self.ax.lines:
            line.remove()

        # Graficar los datos
        self.ax.plot(date_values, values, label=param_name.replace('_', ' '), marker='o', linestyle='-')

        # Configurar leyendas y etiquetas
        if self.legend:
            self.legend.remove()
        self.legend = self.ax.legend()
        self.ax.relim()
        self.ax.autoscale_view()
        self.ax.set_facecolor('none')
        self.ax.set_title("Variation of {} in time".format(param_name.replace('_', ' ')))
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel(param_name.replace('_', ' '))
        self.ax.grid(True, linestyle='--', color='gray', linewidth=0.5)
        # Actualizar el lienzo del gráfico
        self.canvas.draw()

    def get_last_100_data(self, param_name):
        # Obtener los últimos 100 datos del parámetro seleccionado de la base de datos
        data = Instrumentsdb.query.with_entities(Instrumentsdb.date_created, getattr(Instrumentsdb, param_name)).order_by(Instrumentsdb.date_created.desc()).limit(100).all()
        return data

    def populate_combobox(self):
        # Limpiar el contenido actual del QComboBox
        self.ui.parameter.clear()
        self.ui.parameter.addItem("Select a parameter...")
        # Obtener las columnas de la tabla en la base de datos
        try:
            with app.app_context():  # Establecer el contexto de la aplicación
                inspector = inspect(db.engine)
                table_columns = inspector.get_columns('instrumentsdb')  # Reemplaza 'instrumentsdb' con el nombre real de tu tabla
        except Exception as e:
            print("Error al obtener las columnas de la tabla:", e)
            

        # Obtener los nombres de las columnas que no son de tipo str, ni son id, ni son data_cread, ni son MJD
        param_names = [column['name'] for column in table_columns if not isinstance(column['type'], String) and column['name'] not in ["id", "date_created", "MJD"]]
        # Agregar las claves al QComboBox
        param_names = [param.replace('_', ' ') for param in param_names]
        self.ui.parameter.addItems(param_names)
    

    def start_flask(self):
        flask_thread = threading.Thread(target=flask_runner)
        flask_thread.start()

        # Deshabilitar el botón para evitar múltiples clics
        self.ui.start.setEnabled(False)

        # Mostrar un mensaje de confirmación
        QMessageBox.information(self, "Server Started", "Flask server started successfully!")
        self.populate_combobox()

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
        #calculate_and_update_shift()

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

class Instrumentsdb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    MJD = db.Column(db.Float)
    D01 = db.Column(db.String(255))
    Beam_current_setpoint = db.Column(db.Float)
    Cfield_current_setpoint = db.Column(db.Float)
    Ion_pump_current = db.Column(db.Float)
    Signal_gain = db.Column(db.Float)
    RF_Attenuator_setpoints_1 = db.Column(db.Float)
    RF_Attenuator_setpoints_2 = db.Column(db.Float)
    Power_supply_status = db.Column(db.String(255))
    Temperature = db.Column(db.Float)
    Cesium_oven_heater = db.Column(db.Float)
    ECesium_oven_heater_voltage= db.Column(db.Float)
    Hot_wire_ionizer_voltage = db.Column(db.Float)
    Mass_spectrometer_voltage = db.Column(db.Float)
    PLLoop_1 = db.Column(db.Float)
    PLLoop_2 = db.Column(db.Float)
    PLLoop_3 = db.Column(db.Float)
    PLLoop_4 = db.Column(db.Float)
    ROSCillator = db.Column(db.Float)
    Power_supplie_1 = db.Column(db.Float)
    Power_supplie_2 = db.Column(db.Float)
    Power_supplie_3 = db.Column(db.Float)
    Reference_oscillator_frequency = db.Column(db.Float)
    Fractional_frequency_offset = db.Column(db.Float)
    Programmed_frequency_at_specified = db.Column(db.Float)
    Oscillator_oven_voltage = db.Column(db.Float)
    Zeeman_Freq = db.Column(db.Float)
    CBT_Oven_Err = db.Column(db.Float)

class Shift(db.Model):
    __tablename__ = 'shift'
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.Integer, db.ForeignKey('instrumentsdb.id'))
    DV_Zeeman = db.Column(db.Float)
    DV_Zeman_AC = db.Column(db.Float)
    DV_Stark = db.Column(db.Float)
    DV_Gavitational_effects = db.Column(db.Float)
    DV_BBR = db.Column(db.Float)
    # Relación con la tabla de datos existente
    data = db.relationship("Instrumentsdb")

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