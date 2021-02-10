import pyodbc
from flask import current_app as app, abort, jsonify, make_response
from flask_restful import Resource


class countries(Resource):
    def get(self, id=None):

        cnxn = None
        cursor = None

        try:
            cnxn = pyodbc.connect(app.config["CONNSTR"])
            cursor = cnxn.cursor()
            result = cursor.execute("{CALL get_countries (?)}", id).fetchall()
            columns = [e[0] for e in cursor.description]
            recordset = [dict(zip(columns, row)) for row in result]

            # return make_response(jsonify(recordset), 200)
            return jsonify({"countries": recordset})

        except Exception as e:
            if(cursor):
                cursor.close()
            if(cnxn):
                cnxn.close()
            abort(500, jsonify({'msg': str(e)}))
