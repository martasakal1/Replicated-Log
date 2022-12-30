from flask import Flask
from flask import request
import time 

app = Flask(__name__)
from MessageStorage import MessageStorage

msg_storage = MessageStorage()

@app.route('/messages', methods = ['GET', 'POST'])
def return_message():
    
	if request.method == 'GET':

		return msg_storage.get_all(), 200

	if request.method == 'POST':

		data = request.get_json()
		msg_id, message = data.popitem()
		msg_storage.append(msg_id, message)

		return 'Message has been added', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8000)
