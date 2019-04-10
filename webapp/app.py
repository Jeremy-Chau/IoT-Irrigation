import RPi.GPIO as GPIO
import time
import datetime
import Adafruit_DHT
import watering
import psutil
import os
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

sensor = Adafruit_DHT.DHT11
pin = 23

GPIO.setup(8, GPIO.IN)

def template(title = "Raspberry Pi Control Center", msg = ""):
	now = datetime.datetime.now()
	timeString = now.strftime("%m/%d/%Y %H:%M")
	templateDate = {
	'title' : title,
	'time' : timeString,
	'msg' : msg
	}
	return templateDate

@app.route('/')
def hello():
	templateData = template()
	return render_template('main.html', **templateData)

@app.route("/soil")
def soil():
	if GPIO.input(8):
		msg = "Soil is in need of water"
	else:
		msg = "Your plant is fine"
	templateData = template(msg = msg)
	return render_template('main.html', **templateData)

@app.route("/water")
def water():
	watering.pumping()
	templateData = template(msg = "Plant has been manually watered.")
	return render_template('main.html', **templateData)

@app.route("/temp")
def temp():
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if humidity is not None and temperature is not None:
		msg = "Temp = {0:0.1f}*C Humidity={1:0.1f}%".format(temperature, humidity)
	else:
		msg = "Failed to get reading. Try again!"
	templateData = template(msg = msg)
	return render_template('main.html', **templateData)

@app.route("/last")
def last():
	templateData = template(msg = watering.last_watered())
	return render_template('main.html', **templateData)

@app.route("/auto/water/<toggle>")
def auto(toggle):
	run = False
	if toggle == "on":
            templateData = template(msg = "Auto Watering On")
            for process in psutil.process_iter():
                try:
                    if process.cmdline()[1] == 'auto_water.py':
                        templateData = template(msg = "Already running")
                    	run = True
	        except:
                    pass
            if not run:
                os.system("python auto_water.py&")
    	else:
            templateData = template(msg = "Auto Watering Off")
            os.system("pkill -f water.py")
	return render_template('main.html', **templateData)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
