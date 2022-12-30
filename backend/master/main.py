import requests
import asyncio
import os 
import aiohttp
import time 
import random
import backoff

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

	app.logger.info(f'Future {tasks}')

	for future in asyncio.as_completed(tasks):
		
		response =  await future

		if response.status == 200: 

			w_k -= 1

		app.logger.info(f'Future {w_k <= 0}')

		if  w_k <= 0:

			return 'Message was successfully saved', 200

	return 'Replication error', 400

def backoff_hdlr(details):
    app.logger.info(f'Retry')

@backoff.on_exception(backoff.expo,
					Exception,
					max_tries=3,
					on_backoff=backoff_hdlr)

async def copy_message(secondary, message):

	async with aiohttp.ClientSession() as session:
			async with session.post(url=secondary + '/messages', json=message, timeout=10) as response:
					return response






if __name__ == '__main__':
	app.run(host='0.0.0.0', port = 8080)
