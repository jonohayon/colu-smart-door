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
  
  def getApiAddress(self, endpoint):
    return self.doorHost + endpoint

  def handleHttpErr(self, code):
    if code == 404:
      return json.dumps({ 'error': 'Page not found', 'code': code })
    if code == 500:
      return json.dumps({ 'error': 'Server error', 'code': code })
    if code == 400:
      return json.dumps({ 'error': 'Wrong request', 'code': code })

  def getUsers(self):
    r = request.get(self.getApiAddress('get_users'))
    if r.status_code == 200:
      return json.loads(r.text)
    else:
      return self.handleHttpErr(r.status_code)

  def getAdminToken(self):
    payload = { 'username': self.adminUsername }
    headers = { 'content-type': 'application/json' }
    r = request.post(self.getApiAddress('adlog'), data=json.dumps(payload), headers=headers)
    print r.json()['message']
    if r.status_code == 200:
      token = json.loads(r.text)['token']
      return { 'token' : token }
    else:
      return self.handleHttpErr(r.status_code)

  def verifyUser(self, userName):
    headers = { 'content-type': 'application/json' }
    payload = { 'userName': userName }
    r = request.post(self.getApiAddress('login?token=' + self.adminToken), data=json.dumps(payload), headers=headers)
    if r.status_code == 200:
    	return r.json()
    else:
    	return None

  def openDoor(self, userName):
  	msg = self.verifyUser(userName)
  	if msg is None:
  		print 'Error'
  		return None
  	else:
  		GPIO.output(self.physicalDoorPin, True)
  		time.sleep(5)
  		GPIO.output(self.physicalDoorPin, False)
  		return msg
  		
  def openDoorMulti(self):
  	r = request.post(self.getApiAddress('verify_users?token=' + self.adminToken))
  	if r.status_code == 200:
  		GPIO.output(self.physicalDoorPin, True)
  		time.sleep(5)
  		GPIO.output(self.physicalDoorPin, False)
  		return r.json()
  	else:
  		return self.handleHttpErr(r.status_code)
  		
  def openDoorBtn(self):
  	while True:
  		input = GPIO.input(self.physicalBtnPin)
  		if ((not self.prevInput) and input):
  			print 'Button pressed'
  		self.prevInput = input
  		time.sleep(0.05)
  		
  def checkAvailable(self):
  	while True:
  		r = request.get(self.getApiAddress('getpending'))
  		if r.text != '':
  			answer = self.openDoor(r.text)
  			if answer is None:
  				return json.dumps({ 'message': 'Door didnt open'})
  			return json.dumps({ 'message': 'Door opened' })
  		time.sleep(1)
