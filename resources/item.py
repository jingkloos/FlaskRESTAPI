
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
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
    
    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.jason(), 200 
        return{'message':'item not found'},404 

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
            

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            try:
                item.delete()
                return {'message':'item got deleted'},200
            except:
                return {'message':'An error occurred while deleting the item.'},500 #internal server error
        return {'message':'item was not found'},404

class ItemList(Resource):
    def get(self):
        #use list comprehension
        return {'items':[item.jason() for item in ItemModel.query.all()]}

        #use lambda function
        #return {'items': list(map(lambda x:x.jason(),ItemModel.query.all()))}



#######use query to retrieve the list
        # items = []
        # conn=sqlite3.connect('data.db')
        # cursor = conn.cursor()
        # query = 'select name,price from items'

        # result = cursor.execute(query)  
        
        # for row in result:
        #     item = {'name':row[0],'price':row[1]}
        #     items.append(item)

        # conn.close()

        # return {'items':items}