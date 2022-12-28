import requests
import asyncio
import os 
import aiohttp
import time 

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

	app.logger.info(f'Logssss')


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
	while True:
		try:
			return await asyncio.wait_for(post_secondary(secondary, message), timeout=5)

		except asyncio.TimeoutError:
			time.sleep(1)		
			app.logger.info(f'Retry 1')


	return True

async def post_secondary(secondary, message):

	session = aiohttp.ClientSession()

	try:
		return await session.post(url=secondary + '/messages', json=message)
		app.logger.info(f'Finished post')

	finally:
		await session.close()


if __name__ == '__main__':
	app.run(host='0.0.0.0', port = 8080)
