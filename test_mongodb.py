#! /usr/bin/python
import time
from pymongo import MongoClient
import pymongo

client = MongoClient('192.168.10.9:27017')
db = client.rpi_trackman
#print(db)

#exit()

t1 = int(time.time())

print(t1)

# Entry needed in DB
# unique, time, speed,
sample_entry = {
	"uid" : time.time(),
	"data" : [
		# { "time" : time.time(), "speed" : 1.5 },
		{ "time" : 1566615167, "speed" : 1.5 },
		{ "time" : 1566615168, "speed" : 1.3 },
		{ "time" : 1566615169, "speed" : 1.1 },
	]
}

print(sample_entry)

# db.trackman.insert_one(sample_entry)
