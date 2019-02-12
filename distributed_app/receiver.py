from flask import Flask, request, Response
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import json
from flask import jsonify
import subprocess
import datetime
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

db_connect = create_engine("sqlite:///" + os.path.join(dir_path,'users.db'))
app = Flask(__name__)
api = Api(app)


class Users(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        # This line performs query and returns json result
        query = conn.execute("select * from users")
        # Fetches first column that is Employee ID
        return {'users': [i[0] for i in query.cursor.fetchall()]}

    def post(self):
        conn = db_connect.connect()
        user_info = json.loads(request.data)
        conn.execute(
            "insert into users (name) values ('%s')" % str(user_info['user']['name']))
        self.record_transaction(user_info, conn)

        command_success = ["python.exe", "worker.py", "{0}".format(
            user_info['transaction id'])]
        try:
            subprocess.Popen(
                command_success, shell=True)
        except subprocess.CalledProcessError as e:
            return "An error occurred while trying to fetch task status updates." + e.output
        return Response(status=201)

    def record_transaction(self, user_info, conn):
        transaction_id = user_info['transaction id']
        transaction_started_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute(
            "update transactions set started='" +
            transaction_started_time + "' where id = " +
            str(transaction_id))


class Users_Name(Resource):
    def get(self, user_id):
        conn = db_connect.connect()
        query = conn.execute(
            "select * from users where id =%d " % int(user_id))
        result = {'data': [dict(zip(tuple(query.keys()), i))
                           for i in query.cursor]}
        return jsonify(result)


api.add_resource(Users, '/users')  # Route_1
api.add_resource(Users_Name, '/users/<user_id>')  # Route_2


if __name__ == '__main__':
    app.run(port='5002')
