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

    def post(self):
        data = json.loads(request.get_data())
        _nombre_es = data.get('nombre_es')
        _nombre_en = data.get('nombre_en')
        _iso_3 = data.get('iso_3')

        cnxn = None
        cursor = None

        try:
            cnxn = pyodbc.connect(app.config["CONNSTR"])
            cursor = cnxn.cursor()
            cursor.execute("{CALL new_country (?, ?, ?)}", [
                           _nombre_es,
                           _nombre_en,
                           _iso_3
                           ])

            result = cursor.fetchall()
            cnxn.commit()

            columns = [e[0] for e in cursor.description]
            recordset = [dict(zip(columns, row)) for row in result]
            # record = recordset[0]

            if(cursor):
                cursor.close()
            if(cnxn):
                cnxn.close()

        except Exception as e:
            if(cursor):
                cursor.close()
            if(cnxn):
                cnxn.close()
            abort(500, jsonify({'msg': str(e)}))

        else:

            # if (record['success'] == 1):
            # header = g.getHeader2(True, 200, record.get('message'))
            # body = { 'response': recordset }
            # footer = g.getFooter(len(recordset));
            # return jsonify({"header": header, "body": body, "footer":footer})
            # return make_response("OK", 200)
            return jsonify({"countries": recordset[0]})

            # if (record['success'] == 0):
            #     header = g.getHeader2(False, 409, record.get('message'))
            #     body = {'response': recordset}
            #     footer = g.getFooter(len(recordset))
            #     return jsonify({"header": header, "body": body, "footer": footer})

