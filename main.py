import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QVBoxLayout, QSplashScreen
from PyQt6.QtGui import QPainter, QPixmap, QColor, QIcon, QFont
from PyQt6.QtCore import QTimer, Qt, QPointF
from PyQt6 import QtWidgets
from Interface import Ui_Cesium_5071A
import requests
from io import StringIO
import pandas as pd
from datetime import datetime
from sqlalchemy import inspect
from API import flask_runner
import threading
from sqlalchemy.types import String
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime, timedelta
from frequencyShift import Shift_F
from model import app, db, Instrumentsdb, Shift
from sqlalchemy.exc import ProgrammingError
import math


class SplashScreen(QSplashScreen):
    def __init__(self):
        # Carga la imagen de fondo
        pixmap = QPixmap("img/fondo.png")
        
        # Ajusta el tamaño del pixmap al tamaño del splash screen
        self.pixmap = pixmap.scaled(800, 800, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        # Inicializa el splash screen con la imagen ajustada
        super().__init__(self.pixmap)
        
        # Configura las propiedades de la ventana
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setGeometry(500, 300, 800, 630)  # Ajusta el tamaño y la posición según tus necesidades

        # Inicializa el valor de progreso
        self.progress_value = 0
        self.dot_count = 8  # Número de puntos en el círculo de carga
        
        # Configura el temporizador
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.advance_loading)
        self.timer.start(100)  # Actualiza cada 100 ms

        # Establece la máscara para la imagen
        self.setMask(self.pixmap.mask())

    def advance_loading(self):
        self.progress_value += 1
        self.update()  # Redibuja el círculo de carga
        if self.progress_value >= 100:
            self.timer.stop()
            self.close()

    def draw_loading_circle(self, painter, center_x, center_y, radius):
        for i in range(self.dot_count):
            angle = (360 / self.dot_count) * i + self.progress_value * 10
            radian = math.radians(angle)
            dot_radius = 8  # Tamaño de los puntos
            dot_x = center_x + math.cos(radian) * radius
            dot_y = center_y + math.sin(radian) * radius
            color = QColor(129, 145, 166, int(255 * (i + 1) / self.dot_count))  # Gradiente de transparencia
            painter.setBrush(color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPointF(dot_x, dot_y), dot_radius, dot_radius)

    def paintEvent(self, event):
        super().paintEvent(event)
        
        painter = QPainter(self)
        # Ajusta la posición del círculo aquí
        center_x = self.rect().center().x() - 220
        center_y = self.rect().center().y() + 20  # Desplaza el círculo según sea necesario
        radius = 30  # Radio del círculo de carga
        
        # Dibuja el círculo de carga
        self.draw_loading_circle(painter, center_x, center_y, radius)

        text = "Loading..."
        font = QFont("DejaVu Sans Condensed", 10)
        painter.setFont(font)
        text_width = painter.fontMetrics().boundingRect(text).width()
        text_x = center_x - text_width // 2
        text_y = center_y + radius + 20  # Ajusta la posición vertical del texto
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(text_x, text_y, text)
    def mousePressEvent(self, event):
        pass


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('img/favicon.ico'))
        self.ui = Ui_Cesium_5071A()
        self.ui.setupUi(self)
        self.ui.start.clicked.connect(self.start_flask)
        #self.ui.stop.clicked.connect(self.stop_flask)
        #self.populate_combobox()
        self.ui.export_2.clicked.connect(self.export_data)
        # Configurar el temporizador para actualizar el gráfico periódicamente
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)  # Intervalo de tiempo en milisegundos
        self.warning_shown = {}
        self.last_warning_time = {}
        self.warning_interval = timedelta(minutes=10)  #
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
        self.ui.Graph.installEventFilter(self)

    def update_plot(self):
        param_name = self.ui.parameter.currentText().replace(' ', '_')
        if param_name == "Select_a_parameter...":
            return
        self.process_new_data()
        current_time = datetime.now()
        if self.last_clear_time is None or current_time - self.last_clear_time >= timedelta(days=1):
            self.ax.clear()
            self.last_clear_time = current_time
        with app.app_context():
            data = self.get_last_100_data(param_name)
        if data is None:
            return
        date_values = [item.date_created for item in data]
        values = [getattr(item, param_name) for item in data]
        for line in self.ax.lines:
            line.remove()
        self.ax.plot(date_values, values, label=param_name.replace('_', ' '), marker='o', linestyle='-')
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

        if param_name == "ECesium_oven_heater_voltage":
            self.ax.axhline(y=1000, color='red', linestyle='--', label='1000V threshold')
            self.ax.axhline(y=2553, color='red', linestyle='--', label='2553V threshold')
            if values[-1] < 1000 or values[-1] > 2553:
                self.check_and_show_warning(param_name, "Warning: Possible saturation in the electron multiplier", values[-1], 1000, 2553)
        elif param_name == "Cfield_current_setpoint":
            self.ax.axhline(y=0.0100, color='blue', linestyle='--', label='10.0 mA threshold')
            self.ax.axhline(y=0.01405, color='blue', linestyle='--', label='14.05 mA threshold')
            if values[-1] < 0.0100 or values[-1] > 0.01405:
                self.check_and_show_warning(param_name, "Warning: Cfield current setpoint is out of acceptable range", values[-1], 0.0100, 0.01405)
        elif param_name == "Signal_gain":
            self.ax.axhline(y=0.144, color='green', linestyle='--', label='14.4% threshold')
            self.ax.axhline(y=0.580, color='green', linestyle='--', label='58% threshold')
            if values[-1] < 0.144 or values[-1] > 0.580:
                self.check_and_show_warning(param_name, "Warning: Signal gain is out of acceptable range", values[-1], 0.144, 0.580)
        elif param_name == "Reference_oscillator_frequency":
            self.ax.axhline(y=-0.950, color='purple', linestyle='--', label='-95% threshold')
            self.ax.axhline(y=0.950, color='purple', linestyle='--', label='95% threshold')
            if values[-1] < -0.950 or values[-1] > 0.950:
                self.check_and_show_warning(param_name, "Warning: Reference oscillator frequency is out of acceptable range", values[-1], -0.950, 0.950)
        elif param_name == "Ion_pump_current":
            self.ax.axhline(y=0.0, color='orange', linestyle='--', label='0 µA threshold')
            self.ax.axhline(y=0.0000004, color='orange', linestyle='--', label='40 µA threshold')
            if values[-1] < 0.0 or values[-1] > 0.0000004:
                self.check_and_show_warning(param_name, "Warning: Ion pump current is out of acceptable range", values[-1], 0.0, 0.0000004)
        
        self.fig.tight_layout()
        self.canvas.draw()

    def check_and_show_warning(self, param_name, message, value, lower_bound, upper_bound):
        if param_name not in self.warning_shown or not self.warning_shown[param_name]:
            if value < lower_bound or value > upper_bound:
                # Mostrar el mensaje de advertencia si no se ha mostrado una advertencia recientemente
                last_warning = self.last_warning_time.get(param_name, datetime.min)
                if datetime.now() - last_warning > self.warning_interval:
                    self.show_warning(message)
                    self.last_warning_time[param_name] = datetime.now()
                    self.warning_shown[param_name] = True
        else:
            # Permitir mostrar advertencia nuevamente si el último valor está dentro del rango
            if value >= lower_bound and value <= upper_bound:
                self.warning_shown[param_name] = False

    def show_warning(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(message)
        msg.setWindowTitle("Warning")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def get_last_100_data(self, param_name):
        try:
            data = Instrumentsdb.query.with_entities(Instrumentsdb.date_created, getattr(Instrumentsdb, param_name)).order_by(Instrumentsdb.date_created.desc()).limit(1000).all()
            return data
        except AttributeError as e:
            return None
    
    def process_new_data(self, param_name1='Temperature', param_name2='Cfield_current_setpoint'):
        if not param_name1 and not param_name2:
            return

        with app.app_context():
            try:
                last_shift_entry = Shift.query.order_by(Shift.id.desc()).first()
                last_processed_time = last_shift_entry.date_created if last_shift_entry else datetime.min

                new_data = Instrumentsdb.query.with_entities(
                    Instrumentsdb.date_created,
                    getattr(Instrumentsdb, param_name1),
                    getattr(Instrumentsdb, param_name2)
                ).filter(Instrumentsdb.date_created > last_processed_time)\
                .order_by(Instrumentsdb.date_created.asc())\
                .limit(100).all()

                if not new_data:
                    return 
                if len(new_data) < 100:
                    return 

                last_processed_data_time = Shift.query.order_by(Shift.date_created.desc()).first().date_created if Shift.query.first() else datetime.min
                if new_data[0].date_created <= last_processed_data_time:
                    return  

                values1 = [getattr(item, param_name1) for item in new_data]
                values2 = [getattr(item, param_name2) for item in new_data]
                dv_bbr = Shift_F.D_BBR(values1)
                dv_zeeman_ac = Shift_F.ZeemanAC(values1)
                dv_stark = Shift_F.Stark(values1)
                dv_zeeman = Shift_F.Zeeman(values2)
                dv_gravitation = Shift_F.gravitation()
                total = dv_bbr + dv_gravitation + dv_stark + dv_zeeman + dv_zeeman_ac
                new_shift_entry = Shift(
                    date_created=new_data[-1].date_created,
                    DV_BBR=dv_bbr,
                    DV_Zeeman_AC=dv_zeeman_ac,
                    DV_Stark=dv_stark,
                    DV_Zeeman=dv_zeeman,
                    DV_Gavitational_effects=dv_gravitation,
                    DV_Total=total
                )
                db.session.add(new_shift_entry)
                db.session.commit()
                self.update_shift_table()
            except Exception as e:
                print(f"Error: {e}")

    def update_shift_table(self):
        with app.app_context():
            try:
                last_shift_entry = Shift.query.order_by(Shift.id.desc()).first()
                if last_shift_entry:
                    # Formatear cada valor a 5 cifras significativas
                    self.ui.table.setItem(0, 0, QtWidgets.QTableWidgetItem(f"{last_shift_entry.DV_Zeeman:.5g}"))
                    self.ui.table.setItem(1, 0, QtWidgets.QTableWidgetItem(f"{last_shift_entry.DV_Zeeman_AC:.5g}"))
                    self.ui.table.setItem(2, 0, QtWidgets.QTableWidgetItem(f"{last_shift_entry.DV_BBR:.5g}"))
                    self.ui.table.setItem(3, 0, QtWidgets.QTableWidgetItem(f"{last_shift_entry.DV_Gavitational_effects:.5g}"))
                    self.ui.table.setItem(4, 0, QtWidgets.QTableWidgetItem(f"{last_shift_entry.DV_Stark:.5g}"))
                    self.ui.table.setItem(5, 0, QtWidgets.QTableWidgetItem(f"{last_shift_entry.DV_Total:.5g}"))
                else:
                    # Imprimir mensaje en la tabla si no hay datos disponibles
                    self.ui.table.setItem(0, 0, QtWidgets.QTableWidgetItem("No data"))
                    self.ui.table.setItem(1, 0, QtWidgets.QTableWidgetItem("No data"))
                    self.ui.table.setItem(2, 0, QtWidgets.QTableWidgetItem("No data"))
                    self.ui.table.setItem(3, 0, QtWidgets.QTableWidgetItem("No data"))
                    self.ui.table.setItem(4, 0, QtWidgets.QTableWidgetItem("No data"))
                    self.ui.table.setItem(5, 0, QtWidgets.QTableWidgetItem("No data"))
            except ProgrammingError as e:
                print(f"Error de base de datos: {e}")

    def populate_combobox(self):
        # Limpiar el contenido actual del QComboBox
        self.ui.parameter.clear()
        self.ui.parameter.addItem("Select a parameter...")

        # Obtener las columnas de la tabla en la base de datos
        try:
            with app.app_context():  # Establecer el contexto de la aplicación
                inspector = inspect(db.engine)
                table_columns = inspector.get_columns('instrumentsdb')  # Reemplaza 'instrumentsdb' con el nombre real de tu tabla
                
                # Obtener los nombres de las columnas que no son de tipo str, ni son id, ni son date_created, ni son MJD
                param_names = [
                    column['name'] for column in table_columns
                    if not isinstance(column['type'], String) and column['name'] not in ["id", "date_created", "MJD"]
                ]
                # Agregar las claves al QComboBox
                param_names = [param.replace('_', ' ') for param in param_names]
                self.ui.parameter.addItems(param_names)
                
        except Exception as e:
            print("Error al obtener las columnas de la tabla:", e)


    def start_flask(self):
        flask_thread = threading.Thread(target=flask_runner)
        flask_thread.start()

        # Deshabilitar el botón para evitar múltiples clics
        self.ui.start.setEnabled(False)

        # Mostrar un mensaje de confirmación
        QMessageBox.information(self, "Server Started", "Flask server started successfully!")
        try:
            self.populate_combobox()
            self.update_shift_table()
        except Exception as e:
        # Manejar la excepción aquí
            print("Error:", e)

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
def main():
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    window = MainApp()
    QTimer.singleShot(10000, lambda: window.show()) 
    sys.exit(app.exec())

if __name__ == "__main__":
    main()