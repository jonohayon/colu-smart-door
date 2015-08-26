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
    # self.doorHost = 'http://localhost:5000/api/'
    self.adminUsername = 'coluadmin'
    self.adminToken = '0e4a6178a3caf4a7b3c842589fb890d91196d920' # hardcoded admin token
    self.gpioVersion = GPIO.VERSION
    self.bcmDoorPin = 23
    self.physicalDoorPin = 16
    self.wiringDoorPin = 4
    self.bcmBtnPin = 24
    self.physicalBtnPin = 18
    self.wiringBtnPin = 5
    self.prevInput = 0
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(self.physicalDoorPin, GPIO.OUT)
    GPIO.output(self.physicalDoorPin, False)
    GPIO.setup(self.physicalBtnPin, GPIO.IN)

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

  def verifyUser(self, userName):
    headers = { 'content-type': 'application/json' }
    payload = { 'userName': userName }
    r = request.post(self.doorHost + 'login?token=' + self.adminToken, data=json.dumps(payload), headers=headers)
    if r.status_code == 200:
      if r.json() is None:
        print 'Error'
        return None
      return r.json()
    else:
      return None