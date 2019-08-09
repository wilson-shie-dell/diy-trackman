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
	while True:
		start_distance = checkdist()
		#print 'Distance: %0.2f m' %checkdist()
		#print 'Distance: %0.2f m' %start_distance
		time.sleep(time_interval)
		end_distance = checkdist()
		speed = (start_distance - end_distance) / time_interval
                print "Start: %0.2f \t End: %0.2f \t  Speed: %0.2f m/s" % (start_distance, end_distance, speed)
                #print "Speed: %0.2f m/s" %speed
except KeyboardInterrupt:
	# GPIO clean up on exit
	GPIO.cleanup()


