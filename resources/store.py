from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self,name):
        store=StoreModel.find_by_name(name)
        if store:
            return store.json(),200
        else:
            return {'message':'Store not found'},404


    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message':'A store {} already exists.'.format(name)},400

        store=StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'message':'Unexpected error'},500

        return store.json(),201



    def delete(self,name):
        store=StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()
        else:
            return {'message':'Store does not exist'},404

        return {'message':'Store successfully deleted'},200




class StoreList(Resource):
    def get(self):
        return {'stores':[store.json() for store in StoreModel.query.all()]}
