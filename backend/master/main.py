import requests
import asyncio
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
async def add_message():

	message = request.get_json()['message']

	w_k = request.get_json()['w_k']

	messages.append(message)

	w_k -= 1

	tasks = [copy_message(secondary, message) for secondary in secondaries ]

	if w_k == 0:
		asyncio.gather(*tasks)

		return 'Message was successfully saved', 200

	for future in asyncio.as_completed(tasks):
		
		response = await future
		
		if response == True: 

			w_k -= 1

		if  w_k <= 0:

			return 'Message was successfully saved', 200

	return 'Replication error', 400



async def copy_message(secondary, message):

	try: 
		response =  requests.post(url=secondary + '/messages', json=message)

	except:

		return False, message

	if response.status_code == 200:	

		return True

	else:

		return False, response.status_code 

if __name__ == '__main__':
	app.run(host='0.0.0.0', port = 8080)
