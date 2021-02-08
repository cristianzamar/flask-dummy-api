import os
# import pyodbc
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api

import main.controllers.Countries as Countries

app = Flask(__name__)
app.url_map.strict_slashes = False

load_dotenv(dotenv_path=Path('.') / 'dotenv/.env')
ENVIRONMENT = os.environ.get("ENVIRONMENT")
VERSION = os.environ.get("VERSION")
DEBUG = os.environ.get("DEBUG")
TESTING = os.environ.get("TESTING")
DRIVER = os.environ.get("DRIVER")
DATABASE = os.environ.get("DATABASE")
UID = os.environ.get("UID")
PASSWORD = os.environ.get("PASSWORD")
SERVER = os.environ.get("SERVER")
PORT = os.environ.get("PORT")
# CONNSTR = ('DRIVER={'+DRIVER+'};SERVER='+SERVER
#            + ';DATABASE='+DATABASE+';UID='+UID+';PWD='+PASSWORD)
CONNSTR = 'DRIVER={driver};DATABASE={database};UID={uid};PWD={pwd};\
SERVER={server};PORT={port};'.format(driver=DRIVER, database=DATABASE,
                                     uid=UID, pwd=PASSWORD, server=SERVER,
                                     port=PORT)
# 'DRIVER={CData ODBC Driver for PostgreSQL};User=postgres;Password=admin;Database=postgres;Server=127.0.0.1;Port=5432;'

app.config['CONNSTR'] = CONNSTR

api = Api(app)

api.add_resource(Countries.countries, '/countries/<int:id>',
                 '/countries', endpoint='countries')

# conn = pyodbc.connect(app.config["CONNSTR"])
# crsr = conn.execute("SELECT 123 AS n")
# row = crsr.fetchone()
# print(row)
# crsr.close()
# conn.close()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5003, threaded=True)
