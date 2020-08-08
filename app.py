import os

from flask import Flask,request
from flask_restful import Api,reqparse
from flask_jwt import JWT
from resources.item import Item,Items
from resources.user import UserRegister
from security import authenticate,identity
from resources.store import Store,StoreList
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api=Api(app)



jwt = JWT(app,authenticate,identity) #auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items,'/items')
api.add_resource(UserRegister,'/register')
api.add_resource(StoreList, '/stores')

if __name__=='__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)
