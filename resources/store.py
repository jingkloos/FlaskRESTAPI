
from flask_restful import Resource
from flask_jwt import jwt_required
from models.store import StoreModel
class Store(Resource):

    @jwt_required()
    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.jason(), 200 
        return{'message':'store not found'},404 

    def post(self,name):
        
        if StoreModel.find_by_name(name):
            return {'message':'A store with name {} already exists.'.format(name)},400 #bad request
        
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message':'An error occurred while creating the store.'},500
        return {'message':'store created successfully'},201


    def put(self,name):
        store = StoreModel.find_by_name(name)
        
        if store:
            try:
                store.name = name
                store.save_to_db()
                return store.jason(), 200  #ok
            except:
                return {'message':'An error occurred while updating the store.'},500
        else:  
            try:
                store = StoreModel(name)
                store.save_to_db()
                return store.jason(),200
            except:
                return {'message':'An error occurred inserting an store.'},500 #internal server error
            

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete()
                return {'message':'store got deleted'},200
            except:
                return {'message':'An error occurred while deleting the store.'},500 #internal server error
        return {'message':'store was not found'},404

class StoreList(Resource):
    def get(self):
        #use list comprehension
        return {'stores':[store.jason() for store in StoreModel.query.all()]}

        