import time
import datetime
import sqlite3
import sys
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

def record_transaction(transaction_id, conn):
        transaction_completion_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute(
            "update transactions set completed='" +
            transaction_completion_time + "' where id = " +
            str(transaction_id))
        conn.commit()

conn = sqlite3.connect(os.path.join(dir_path,'users.db'))

for i in range(10):
    time.sleep(1)
    print("Waiting:" + str(i))

print("Recording the transaction completion for :" + sys.argv[1])
record_transaction(sys.argv[1], conn)