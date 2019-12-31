from flask import Flask
from flask_restful import Api
from security import authenticate,identity
from flask_jwt import JWT
from resources.user import UserRegister
from resources.item import Item,ItemList
from resources.store import Store,StoreList
from _datetime import timedelta
from flask.json import jsonify
import os


app = Flask(__name__)
app.secret_key='email'
api = Api(app)



app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #turn off flask sqlalchemy modification, use sqlalchemy track
app.config['JWT_AUTH_URL_RULE']='/Login'  #change the default /auth to /Login
app.config['JWT_EXPIRATION_DELTA']=timedelta(seconds=1800)   #default is 5 mins
# app.config['JWT_AUTH_USERNAME_KEY']='email'  # config JWT auth key name to be 'email' instead of default 'username'

jwt=JWT(app,authenticate,identity)  #JWT create an endpoint /auth to return the jwt token

# customize JWT auth response, include user_id in response body
@jwt.auth_response_handler
def customized_response_handler(access_token,identity):
    return jsonify({
        'access_token':access_token.decode('utf-8'),
        'user_id':identity.id
    })


@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
        'message':error.description,
        'code':error.status_code
    }),error.status_code

api.add_resource(Item,'/Item/<string:name>')
api.add_resource(ItemList,'/Items')
api.add_resource(UserRegister,'/Register')
api.add_resource(Store,'/Store/<string:name>')
api.add_resource(StoreList,'/Stores')

if __name__ == '__main__':          #this is to prevent app to be run by any import
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)


