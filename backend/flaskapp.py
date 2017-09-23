#!/usr/bin/env python
from flask import Flask, request, render_template
import os
import json
import uuid
import argparse
import datetime

app = Flask(__name__, instance_relative_config=True)


# Silly JSON encoder to encode datetime strings
class JSONExtendedEncoder(json.JSONEncoder):
    def default(self,o):
        if type(o) == datetime:
            return str(o)
        else:
            return super(JSONExtendedEncoder,self).default(o)

# Standin (!) for a real database
app.datastore = {}

#@app.before_first_request
#def initialize():
#    nop()

# Hello World
@app.route("/", methods=["GET"])
def helloworld():
    return("Hello World {}".format(uuid.uuid4().hex))

# POST (hospital) survey data to backend and issue a QR code response
@app.route("/data", methods=["POST"])
def hospitalCollectData():
    # create user's id
    tid = uuid.uuid4().hex

    app.datastore[tid] = {
        "hvisit": str(datetime.datetime.now()),
        "tid": tid,
        "pid": request.form["pid"],
        "submission":request.form
    }

    # debug print
    print(json.dumps(app.datastore[tid], indent=4, cls=JSONExtendedEncoder))
    return render_template('ticket.htm', data=app.datastore[tid])

# POST (truck) scanned data, and issue a printed receipt
@app.route("/visit", methods=["POST"])
def truckCollectData():
    print(request.json)
    truckVisitJson = request.json
    tid = truckVisitJson['tid']
    truckid = truckVisitJson['truckid']

    try:
        transaction = app.datastore[tid]
        transaction['tvisit'] = str(datetime.datetime.now())
        transaction['truckid'] = truckVisitJson['truckid']

        response = app.response_class(
            response = "visit to " + truckid + " for transaction " + tid + " posted!",
            status=201
        )
    except KeyError:
        message = "invalid input, transaction id " + tid + " doesn't exist"
        response = app.response_class(
            response= message,
            status=400,
            mimetype='application/text'
        )

    # debug print
    print(json.dumps(app.datastore[tid], indent=4, cls=JSONExtendedEncoder))

    return response

# GET stored data, see how it matches up
@app.route("/summary", methods=["GET"])
def fetchLoopData():
    userId = request.args.get('id')

    response = app.response_class(
        response=json.dumps(app.datastore[userId]),
        status=200,
        mimetype='application/json'
    )
    return response

def main():
    parser = argparse.ArgumentParser(description='Start up test server')
    parser.add_argument('-c', '--config', default='beta', help='configuration to use')
    args = parser.parse_args()

    # configureApp(app, args.config)
    app.secret_key = os.urandom(24)
    app.run(host='0.0.0.0', port=5555, debug=False)

if __name__ == "__main__":
    main()