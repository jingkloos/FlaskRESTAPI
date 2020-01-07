from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister,User,UserLogin,TokenRefresh,UserLogout
from resources.item import Item,ItemList
from resources.store import Store,StoreList
import os
from blacklist import BLACKLIST

app = Flask(__name__)
app.secret_key='email'   #app.config['JWT_SECRET_KEY'] = xxxx if you want to use a differenct SECRET key for login
api = Api(app)

#this is not needed when run the app on Heroku (aka. from run.py)
@app.before_first_request
def create_tables():
    db.create_all()


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #turn off flask sqlalchemy modification, use sqlalchemy track
app.config['PROPAGATE_EXCEPTIONS']=True  # let JWT return its error
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']

jwt=JWTManager(app)  #JWTmanager link the app with JWT

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: #instead of hard coding this, you should read it from config file or database
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

# customize call backs of jwt errors
@jwt.expired_token_loader
def expired_token_callback():
    return {
        'description':'Session expired.',
        'error': 'token_expired'
    },401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {
        'description':'Signature verification failed.',
        'error':'invalid_token'
    }, 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return {
        'description':'Request does not contain an access token.',
        'error':'authorization required.'
    }, 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return {
        'description':'The token is not fresh.',
        'error':'fresh token required.'
    }, 401
@jwt.revoked_token_loader
def revoked_token_callback():
    return {
        'description':'The token has been revoked.',
        'error':'token revoked.'
    }, 401



api.add_resource(Item,'/Item/<string:name>')
api.add_resource(ItemList,'/Items')
api.add_resource(UserRegister,'/Register')
api.add_resource(Store,'/Store/<string:name>')
api.add_resource(StoreList,'/Stores')
api.add_resource(User,'/User/<int:user_id>')
api.add_resource(UserLogin,'/Login')
api.add_resource(UserLogout,'/Logout')
api.add_resource(TokenRefresh,'/Refresh')

if __name__ == '__main__':          #this is to prevent app to be run by any import
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)


