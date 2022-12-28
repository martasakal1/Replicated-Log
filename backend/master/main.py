import requests
import asyncio
import os 
import aiohttp
from flask import Flask
from flask import request

app = Flask(__name__)

messages = []
secondaries = [ 'http://secondary1:8000', 'http://secondary2:8000' ]	

timeout = 20

@app.route('/get_message')
def get_message():
	return ''.join(str(messages)), 200

@app.post('/messages/new')
async def add_message():

	message = request.get_json()['message']

	w_k = request.get_json()['w_k']

	messages.append(message)

	w_k -= 1


	tasks = [asyncio.create_task(copy_message(secondary, message)) for secondary in secondaries ]

	if w_k == 0:

		await asyncio.gather(*tasks)

		return 'Message was successfully saved', 200

	for future in asyncio.as_completed(tasks):
		
		response =  await future
		
		if response == True: 

			w_k -= 1

	if  w_k <= 0:

		return 'Message was successfully saved', 200

	return 'Replication error', 400



async def copy_message(secondary, message):

	await post_secondary(secondary, message)

	return True

async def post_secondary(secondary, message):

	session = aiohttp.ClientSession()

	while not await session.post(url=secondary + '/messages', json=message):
		app.logger.error(f'Host is unreachable: {secondary}; Waiting for {timeout} seconds')
		time.sleep(1)
		timeout -= 1

	await session.close()

	return True

if __name__ == '__main__':
	app.run(host='0.0.0.0', port = 8080)
