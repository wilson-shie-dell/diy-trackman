#! /usr/bin/python
import os
import time
import json
from pymongo import MongoClient
import pymongo

# If running in PWS, use mlab
if 'VCAP_SERVICES' in os.environ:
	VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])
	MONCRED = VCAP_SERVICES["mlab"][0]["credentials"]
	client = MongoClient(MONCRED["uri"])
	DB_NAME = str(MONCRED["uri"].split("/")[-1])
	db = client[DB_NAME]

else:
	client = MongoClient('192.168.10.9:27017')
	db = client.rpi_trackman
	#print(db)

#exit()

uid = int(time.time())

print(uid)

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

print(sample_entry)

# Insert entry
db.trackman.insert_one(sample_entry)

# Retrieve all
cursor = db.trackman.find()
for each_entry in cursor:
	print(each_entry)
