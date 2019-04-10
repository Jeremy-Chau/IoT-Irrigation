import RPi.GPIO as GPIO
import datetime
import time

pump = 7
soil = 8
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

def last_watered():
	try:
		f = open("Last_Watered.txt", "r")
		return f.readline()
	except:
		return "Hasn't Been Watered"

def init(pump, soil):
	GPIO.setup(pump, GPIO.OUT)
	GPIO.setup(soil, GPIO.IN)
	GPIO.output(pump, GPIO.LOW)

def auto_water():
	water_count = 0
	init(pump, soil)
	try:
	    while 1 and water_count < 5:
	        time.sleep(5)
		wet = GPIO.input(8) == 0
		if not wet:
		    if water_count < 5:
			pumping()
		    water_count += 1
		else:
		    water_count = 0
	except KeyboardInterrupt:
		GPIO.cleanup()

def pumping():
	init(pump, soil)
	f = open("Last_Watered.txt", "w")
	now = datetime.datetime.now()
	now = now.strftime("%m/%d/%Y %H:%M")
	f.write("Last Watered {}".format(now))
	f.close()
	GPIO.output(7, GPIO.HIGH)
	time.sleep(5)
	GPIO.output(7, GPIO.LOW)
