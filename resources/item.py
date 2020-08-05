import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
class Item(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True,help="This field cannot be left blank!")
    parser.add_argument('store_id',type=int,required=True,help="Every item needs a store id!")
    @jwt_required()
    def get(self,name):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()
        query="Select * from items where name=?"
        result=cursor.execute(query,(name,))
        row=result.fetchone()
        if row:
            return {'item':{'name':row[1],'price':row[2],'store_id':row[3]}}

        return {'message':'item not found'}

    def post(self,name):
        data=Item.parser.parse_args()
        item=ItemModel(name,**data)
        if ItemModel.find_by_name(name):
            return {'message':'The item already exists'},400
        try:
            item.save_to_db()
        except Exception as e:
            return "Unexpected Error",500
        else:
             return item.json(),201


    def delete(self,name):
        item=ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message':'Item successfully deleted.'}

    def put(self,name):
        data=Item.parser.parse_args()
        item=ItemModel.find_by_name(name)

        if item:
            item.price=data['price']
        else:
            item=ItemModel(name,**data)

        item.save_to_db()
        return item.json(),201


class Items(Resource):
    def get(self):
        return {'items':list(map(lambda x: x.json(),ItemModel.query.all()))}
