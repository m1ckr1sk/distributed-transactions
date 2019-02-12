import json
import datetime
import sqlite3
import requests
import time
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))


class Sender:
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(dir_path,'users.db'))

    def start_transaction(self):
        transaction_start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = self.conn.execute(
            "insert into transactions (created) values ('" +
            transaction_start_time + "')")
        self.conn.commit()
        return query.lastrowid

    def create_user(self, user_name):
        transaction_id = self.start_transaction()
        url = 'http://127.0.0.1:5002/users'
        data = {}
        data["transaction id"] = transaction_id
        user = {}
        user["name"] = user_name
        data["user"] = user
        data_json = json.dumps(data)
        print("Sending: " + data_json)

        response = requests.post(url, data_json)   
        print("Response: " + str(response.status_code))
        return transaction_id

    def is_user_created(self, transaction_id):
        cursor = self.conn.cursor()
        transaction_complete = False
        cursor.execute("select completed from transactions where id = " + str(transaction_id))
        rows = cursor.fetchall()
        if rows[0][0] is not None:
            transaction_complete = True
        return transaction_complete

     


