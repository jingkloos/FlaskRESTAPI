
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required,get_jwt_claims,jwt_optional,get_jwt_identity,fresh_jwt_required
from models.item import ItemModel
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='price can not be blank!'
        )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help='item must be in a store'
        )
    
    @jwt_required        #jwt token doesn't need to be fresh
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.jason(), 200 
        return{'message':'item not found'},404 

    @fresh_jwt_required      #jwt token has to be fresh (aka. just logged in )
    def post(self,name):
        
        if ItemModel.find_by_name(name):
            return {'message':'An item with name {} already exists.'.format(name)},400 #bad request
        data = Item.parser.parse_args()
        item = ItemModel(name,**data)
        item.save_to_db()
        return {'message':'Item created successfully'},201


    def put(self,name):
    
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        
        if item:
            try:
                item.price = data['price']
                item.store_id = data['store_id']
                item.save_to_db()
                return item.jason(), 200  #ok
            except:
                return {'message':'An error occurred while updating the item.'},500
        else:  
            try:
                item = ItemModel(name,**data)
                item.save_to_db()
                return item.jason(),200
            except:
                return {'message':'An error occurred inserting an item.'},500 #internal server error
            
    @jwt_required
    def delete(self,name):
        claims = get_jwt_claims()  #get all claims added for jwt
        if not claims['is_admin']:
            return {'message':'Admin privilege required.'},401

        item = ItemModel.find_by_name(name)
        if item:
            try:
                item.delete()
                return {'message':'item got deleted'},200
            except:
                return {'message':'An error occurred while deleting the item.'},500 #internal server error
        return {'message':'item was not found'},404

class ItemList(Resource):
    @jwt_optional
    def get(self):
        #use list comprehension
        user_id = get_jwt_identity()
        items = [item.jason() for item in ItemModel.find_all()]
        if user_id:
            return {'items':items}, 200
        return {'items':[item['name'] for item in items],
                'message':'More data available after log in.'},200





