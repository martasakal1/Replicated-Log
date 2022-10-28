import requests
import os 
from flask import Flask
from flask import request

app = Flask(__name__)

messages = []
secondaries = [ 'http://secondary1:8000', 'http://secondary2:8000' ]	

@app.route('/get_message')
def get_message():
	return ''.join(str(messages)), 200

@app.post('/messages/new')
def add_message():

	message = request.get_json()

	messages.append(message)

	if replicate(message):
		return 'New message successfully added', 200
	else:
		return 'Unsuccessfull attempt', 400

def replicate(message):

	try: 
		for secondary in secondaries:
				requests.post(url=secondary + '/messages', json=message)
		return True

	except:

		return False 

if __name__ == '__main__':
	app.run(host='0.0.0.0', port = 8080)
