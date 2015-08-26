###################
# Colu Smart Door #
###################

### Uncomment when on RasPi
import RPi.GPIO as GPIO
import requests as request
import time
import json

class Door():
  def __init__(self):
    self.doorHost = 'http://smart-door.herokuapp.com/api/'
    self.gpioVersion = GPIO.VERSION
    self.bcmDoorPin = 23
    self.physicalDoorPin = 16
    self.wiringDoorPin = 4
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(self.physicalDoorPin, GPIO.OUT)
    GPIO.output(self.physicalDoorPin, False)

  def openDoor(self):
    GPIO.output(self.physicalDoorPin, True)
    time.sleep(5)
    GPIO.output(self.physicalDoorPin, False)

  def checkAvailable(self):
    while True:
      try:
        r = request.get(self.doorHost + 'status')
        if r.text == 'pending':
          self.openDoor()
        time.sleep(1)
      except ConnectionError, e:
        raise e
