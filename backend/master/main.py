import asyncio
import os
import aiohttp
import backoff

from flask import Flask
from flask import request

from Replicator import Replicator
from MessageStorage import MessageStorage


app = Flask(__name__)
msg_storage = MessageStorage()
replicator = Replicator(app.logger)

secondaries = [ 'http://secondary1:8000', 'http://secondary2:8000' ]
GID = 0

def get_gid():
	global GID
	GID = GID + 1
	return GID


@app.route('/get_message')
def get_message():
	return msg_storage.get_all(), 200

@app.post('/messages/new')
async def save_message():

	try:
		message = request.get_json()['message']
	except:
		app.logger.error(f'Message fiels was not found in reuqest data')
		return 'The field "message" was not found in JSON', 400

	msg_id = get_gid()

	try:
		w_c = request.get_json()['w_c']
	except:
		app.logger.error(f'Write concern field was not found in reuqest data')

	msg_storage.append(msg_id, message)

	w_c -= 1

	if await replicator.add_message(msg_id, message, w_c):
			return 'Message was successsfuly saved', 200

	return 'Replication Error', 400



if __name__ == '__main__':
	app.run(host='0.0.0.0', port = 8080)
