from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cesium_instruments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
    ECesium_oven_heater_voltage = db.Column(db.Float)
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
    date_created = db.Column(db.DateTime, nullable=False)
    DV_Zeeman = db.Column(db.Float)
    DV_Zeeman_AC = db.Column(db.Float, nullable=False)
    DV_Stark = db.Column(db.Float, nullable=False)
    DV_Gavitational_effects = db.Column(db.Float, nullable=False)
    DV_BBR = db.Column(db.Float, nullable=False)
    DV_Total = db.Column(db.Float)

def check_data_dbmodeltable(model):
    try:
        with app.app_context():
            num_records = model.query.count()
            return num_records > 0
    except Exception as e:
        print(f"Error checking data in {model.__name__}: {e}")
        return False
