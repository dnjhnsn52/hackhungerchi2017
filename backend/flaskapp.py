#!/usr/bin/env python

from flask import Flask, request
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
    my_uuid = uuid.uuid4().hex

    app.datastore[my_uuid] = {
        "uuid_datetime": str(datetime.datetime.now()),
        "uuid": my_uuid,
        "submission":request.json
    }

    # debug print
    print(json.dumps(app.datastore[my_uuid], indent=4, cls=JSONExtendedEncoder))

    response = app.response_class(
        response=json.dumps(app.datastore[my_uuid]),
        status=200,
        mimetype='application/json'
    )
    return response

# POST (truck) scanned data, and issue a printed receipt
@app.route("/visit", methods=["POST"])
def truckCollectData():
    return("blah +", uuid.uuid4().hex)

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