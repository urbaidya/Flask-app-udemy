from db import db
from flask import Flask
from flask_restful import Api, reqparse
from flask_jwt import JWT

from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from security import authenticate, identity

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONA'] = False  ## 
app.secret_key='umesh'
api=Api(app)

@app.before_first_request
def create_tables():
	db.create_all()

jwt=JWT(app, authenticate, identity)  ##this creates a new endpoint '/auth'

api.add_resource(Item, '/item/<string:name>')  ## same as http://localhost:5000/item/<name>
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':  ## this IF condition is only true if we run the main py file, not when we import it,
						   ## this happens bcoz when we run it, python assigns the __name__ as __main__ not
						   ## in other cases.
	db.init_app(app)
	app.run(port=5000, debug=True)  ## debug = True gives nicer error message