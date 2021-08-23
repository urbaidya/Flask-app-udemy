import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('username', 
		type=str, 
		required=True,
		help='This field cannot be blank!')
	parser.add_argument('password', 
		type=str, 
		required=True,
		help='This field cannot be blank!')

	def post(self):
		data=UserRegister.parser.parse_args()

		## this if checks if user already exists in the database
		if UserModel.find_by_username(data['username']) is not None:
			return {'message': 'User with username already exists.'}, 400

		user = UserModel(**data)
		user.save_to_db()

		return {'message': 'User created successfully.'}, 201


