#!/usr/bin/env python

import os
import uuid
import time
import json
from flask import Flask
from flask import render_template
from pymongo import MongoClient
import pymongo

app = Flask(__name__)
my_uuid = str(uuid.uuid1())

# If running in PWS, use mlab
if 'VCAP_SERVICES' in os.environ:
    VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])
    MONCRED = VCAP_SERVICES["mlab"][0]["credentials"]
    client = MongoClient(MONCRED["uri"])
    DB_NAME = str(MONCRED["uri"].split("/")[-1])
    db = client[DB_NAME]

else:
    client = MongoClient('192.168.179.7:27017')
    db = client.rpi_trackman
    #print(db)


@app.route('/')
def mainmenu():

    uid = int(time.time())

    # Entry needed in DB
    # unique, time, speed,
    sample_entry = {
        "uid" : uid,
        "data" : [
            # { "time" : time.time(), "speed" : 1.5 },
            { "time" : 1566615167, "speed" : 1.5 },
            { "time" : 1566615168, "speed" : 1.3 },
            { "time" : 1566615169, "speed" : 1.1 },
            { "time" : 1566615170, "speed" : 0.9 },
        ]
    }

    # Insert entry
    # db.trackman.insert_one(sample_entry)

    # Retrieve all DB entries
    cursor = db.trackman.find()

    return render_template('index.html', title='Raspberry Pi Trackman', cursor=cursor)

if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))

