#! /usr/bin/python
import RPi.GPIO as GPIO
import time

# Global variables
time_interval = 0.1
start_distance = 0.0
end_distance = 0.0

# checkdisk function
def checkdist():
	GPIO.output(16, GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(16, GPIO.LOW)
	while not GPIO.input(18):
		pass
	t1 = time.time()
	while GPIO.input(18):
		pass
	t2 = time.time()
	return (t2-t1)*340/2

# GPIO setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(18,GPIO.IN)
time.sleep(2)

try:
        uid = 0
	start_distance = checkdist()
	while True:
		#print 'Distance: %0.2f m' %checkdist()
		#print 'Distance: %0.2f m' %start_distance
		time.sleep(time_interval)
		end_distance = checkdist()
                distance_difference = start_distance - end_distance
                if distance_difference < 0.01:
                    start_distance = end_distance
                    uid += 1
                    continue
                else:
		    speed = distance_difference / time_interval
                    print "ID: %2s \t Start: %0.3f \t End: %0.3f \t  Speed: %0.2f m/s" % (uid, start_distance, end_distance, speed)
                #print "Speed: %0.2f m/s" %speed
                start_distance = end_distance
                uid += 1
except KeyboardInterrupt:
	# GPIO clean up on exit
	GPIO.cleanup()


