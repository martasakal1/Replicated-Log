import requests
import asyncio
import os 
import aiohttp
import time 
import random
import backoff
import logging

class Replicator:

	def __init__(self, logger):
		self.secondaries =  ['http://secondary1:8000', 'http://secondary2:8000']
		self.logger = logger


	async def add_message(self, msg_id, message, w_c):

		tasks = [asyncio.create_task(self.copy_message(secondary, message, msg_id)) for secondary in self.secondaries ]

		if w_c == 0:
			return 'Message was successfully saved', 200

		for future in asyncio.as_completed(tasks):
			response =  await future
			if response.status == 200: 
				w_c -= 1

				if  w_c <= 0:
					return True

		return False

	def backoff_hdlr(details):
		logging.info(f'Retry')

	@backoff.on_exception(backoff.expo,
						Exception,
						max_tries=3,
						on_backoff=backoff_hdlr)

	async def copy_message(self, secondary, message, msg_id):
		data = {}
		data[msg_id] = message
		async with aiohttp.ClientSession() as session:
			async with session.post(url=secondary + '/messages', json=data, timeout=10) as response:
				return response