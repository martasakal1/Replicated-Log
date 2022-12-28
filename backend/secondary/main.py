from flask import Flask
from flask import request
import time 

app = Flask(__name__)

messages = []

@app.route('/messages', methods = ['GET', 'POST'])
def return_message():
    
	if request.method == 'GET':

		return ''.join(str(messages)), 200

	if request.method == 'POST':


		time.sleep(10)

		message = request.get_json()
		messages.append(message)

		return 'Message has been added', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8000)
