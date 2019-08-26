#!/usr/bin/env python

import os
import uuid
import time
import json
from flask import Flask, render_template
from pymongo import MongoClient
import pymongo
from flask_restful import Resource, Api

import random

app = Flask(__name__)
api = Api(app)

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

    # Retrieve all DB entries
    cursor = db.trackman.find()

    return render_template('index.html', title='Raspberry Pi Trackman', cursor=cursor)


@app.route('/view/<int:uid>')
def view(uid):

    # Retrieve single entry
    cursor = db.trackman.find({"uid":uid})

    return render_template('view.html', title='Raspberry Pi Trackman', cursor=cursor)


@app.route('/delete/<int:uid>')
def delete(uid):

    # Delete entry
    db.trackman.delete_one({"uid":uid})

    return render_template('delete.html', title='Raspberry Pi Trackman')


class NewEntry(Resource):
    def get(self):

        uid = int(time.time())

        # Temporary Random data generator
        initial_speed = round(random.uniform(1.0, 2.0), 2)
        test_data = []
        while initial_speed >= 0.0:
            test_data.append({"time":uid, "speed":initial_speed})
            uid += 1
            initial_speed = round(initial_speed - 0.2, 2)

        # Entry needed in DB
        # unique, time, speed,
        sample_entry = {
            "uid" : uid,
            # "data" : [
            #     # { "time" : time.time(), "speed" : 1.5 },
            #     { "time" : 1566615167, "speed" : 1.5 },
            #     { "time" : 1566615168, "speed" : 1.3 },
            #     { "time" : 1566615169, "speed" : 1.1 },
            #     { "time" : 1566615170, "speed" : 0.9 },
            # ]
            "data" : test_data,
        }

        # Insert entry
        db.trackman.insert_one(sample_entry)

        return {'status' : 'ok'}


# Register API
api.add_resource(NewEntry, '/NewEntry')


if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))

