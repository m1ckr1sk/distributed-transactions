# Distributed Transactions
A small project to explore patterns for distributed transactions in python.

## Overview
The app consists of three applications. 

#### Sender
The sender app starts the transaction by inserting a row in the transaction table and then making a rest call to the receiver app.

#### Receiver
The receiver app is a small flask app that replicates a simple api.  When the request is received it updates the transaction log to say that the request has been received.  It then kicks off the worker app.

#### Worker
The worker app simulates a long running operation.  Once complete it writes the final update into the transaction to let the original caller know that the transaction is complete.


## Run the tests
Start the receiver app:

```
python distributed_app\receiver.py
```

Now run the test from 

```
python -m pytest .\tests\
```