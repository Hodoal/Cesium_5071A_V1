import os

class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))
    # Set up the App SECRET_KEY
    # SECRET_KEY = config('SECRET_KEY'  , default='S#perS3crEt_007')
    SECRET_KEY = os.getenv('SECRET_KEY', 'S#perS3crEt_007')

    # This will create a file in <app> FOLDER
    #SQLALCHEMY_DATABASE_URI = 'sql:///' + os.path.join(basedir, 'db.sql')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(

        os.getenv('DB_ENGINE'   , 'mysql'),
        os.getenv('DB_USERNAME' , 'root'),
        os.getenv('DB_PASS'     , 'J4viquantum!'),
        os.getenv('DB_HOST'     , 'localhost'),
        os.getenv('DB_PORT'     , 3306),
        os.getenv('DB_NAME'     , 'pruebas')
    )