#!/usr/bin/python

import time
import datetime
import json
from google.cloud import pubsub
from oauth2client.client import GoogleCredentials
from Adafruit_BME280 import *

# constants
SEND_INTERVAL = 60 #seconds
sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
credentials = GoogleCredentials.get_application_default()
project="brandonfreitag-sandbox"
topic = "weatherdata"
sensorID = "s-ChatfieldStatePark"
sensorZipCode = "80125"
sensorLat = "39.5297838"
sensorLong = "-105.05404240000001"

def publish_message(project_name, topic_name, data):
	pubsubClient = pubsub.Client(
		project=project_name
	)	
	topicObj = pubsubClient.topic(topic_name)
	topicObj.publish(data)
	print data

def read_sensor(weathersensor):
    tempF = weathersensor.read_temperature_f()
    # pascals = sensor.read_pressure()
    # hectopascals = pascals / 100
    pressureInches = weathersensor.read_pressure_inches()
    dewpoint = weathersensor.read_dewpoint_f()
    humidity = weathersensor.read_humidity()
    temp = '{0:0.2f}'.format(tempF)
    hum = '{0:0.2f}'.format(humidity)
    dew = '{0:0.2f}'.format(dewpoint)
    pres = '{0:0.2f}'.format(pressureInches)
    return (temp, hum, dew, pres)

def createJSON(id, timestamp, zip, lat, long, temperature, humidity, dewpoint, pressure):
    data = {
      'sensorID' : id,
      'time' : timestamp,
      'zipcode' : zip,
      'latitude' : lat,
      'longitude' : long,
      'temperature' : temperature,
      'humidity' : humidity,
      'dewpoint' : dewpoint,
      'pressure' : pressure
    }

    json_str = json.dumps(data)
    return json_str

def main():
  last_checked = 0
  while True:
    if time.time() - last_checked > SEND_INTERVAL:
      last_checked = time.time()
      temp, hum, dew, pres = read_sensor(sensor)
      currentTime = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
      s = ", "
      weatherJSON = createJSON(sensorID, currentTime, sensorZipCode, sensorLat, sensorLong, temp, hum, dew, pres)
      #weatherList = (sensorID, currentTime, sensorZipCode, sensorLat, sensorLong, temp, hum, dew, pres)
      #message = s.join(weatherList)
      #weatherData = message.encode("utf-8")
      publish_message(project, topic, weatherJSON)
    time.sleep(0.5)

if __name__ == '__main__':
	main()