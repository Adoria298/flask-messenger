from flask import Flask, render_template, request
from flask_restful import Api, Resource, reqparse
#from flask_login import LoginManager
from uuid import uuid4
import random
import requests

app = Flask(__name__)
api = Api(app)
#login_manager = for later

messages = []
users = []
HOST = '0.0.0.0'
PORT = '5000'


class Message(Resource):	
	
	def get(self):
		messages_reversed = messages.copy().reverse()
		return messages_reversed, 200
	
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("name")
		parser.add_argument("text")
		args = parser.parse_args()
		
		if args["name"] == None:
			name = "Unknown"
		else:
			name = args["name"]

		text = args["text"]
			
		new_message = {
			"text": text,
			"name": name,
			"id": str(uuid4())
		}
		
		messages.append(new_message)
		print(new_message)
		return new_message, 201
		
	def put(self):
		parser = reqparse.RequestParser()
		parser.add_argument("name")
		parser.add_argument("id")
		parser.add_argument("text")
		args = parser.parse_args()
		
		if args["name"] == None:
			name = "Unknown"
		else:
			name = args["name"]

		text = args["text"]
		
		for original_message in messages:
			if original_message["id"] == args["id"]: #if the user wants to update a message
				original_message["text"] = text
				original_message["name"] = args["name"]
				return original_message, 201
			
		new_message = {
			"text": text,
			"name": name,
			"id": str(uuid4())
		}
		
		messages.append(new_message)
		print(new_message)
		return new_message, 201
		
	def delete(self):
		parser = reqparse.RequestParser()
		parser.add_argument("id")
		args = parser.parse_args()
		
		if args["id"] == "all":
			for message in messages:
				messages.pop(message)
			return "Deleted all messages", 200
		else:
			for index, message in enumerate(self.messages):
				if message["id"] == args["id"]:
					messages.pop(index)
					return "Deleted message {0}".format(message["id"]), 200
				
		
	
@app.route('/')
def index():
	return render_template('view.html', messages=messages)
	
@app.route('/handle_data', methods=['POST'])
def handle_data():
	text = request.form["text"]
	name = request.form["name"]
	
	requests.post(url='http://'+HOST+':'+PORT+'/api/messages', data={"name": name, "text": text})
	
	return index()
	
@app.route('/handle_refresh', methods=['POST'])
def handle_refresh():
	return index()
				
api.add_resource(Message, "/api/messages")

if __name__ == '__main__':
	app.run(debug=True, host=HOST, port=PORT)
				
		
