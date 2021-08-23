from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import request
from models.item import ItemModel

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price', 
		type=float, 
		required=True,
		help='This field cannot be blank!')

	parser.add_argument('store_id', 
		type=float, 
		required=True,
		help='Every item needs a store id.')

	@jwt_required()
	def get(self, name):
		item=ItemModel.find_by_name(name)
		if item:
			return item.json()
		return {'message': 'No item with this name found.'}, 404

	def post(self, name):
		if ItemModel.find_by_name(name):
			return {'message': f'An item with name {name} already exists.'}, 400
		request_data=Item.parser.parse_args()
		item=ItemModel(name, **request_data)
		try:
			item.save_to_db()
		except:
			return {'message':'An Error Occured inserting the item.'}, 500 #internal server error
		
		return item.json(), 201  ## here 201 is created, (202 is for accepted)

	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()
		return {'message': 'Item deleted.'}

	def put(self, name):
		request_data=Item.parser.parse_args()
		item=ItemModel.find_by_name(name)
		if item is None:
			item=ItemModel(name, **request_data)
		else:
			item.price = request_data['price']
		item.save_to_db()
		return item.json()


class ItemList(Resource):
	def get(self):
		return {'Items': list(map(lambda x:x.json(), 
								  ItemModel.query.all()))}  ##.all() gets all the items, 
		                                                    ## then use map to jsonify each selected item
