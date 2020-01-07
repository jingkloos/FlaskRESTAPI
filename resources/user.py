
from flask_restful import Resource,reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,create_refresh_token,get_jwt_identity,jwt_refresh_token_required,jwt_required,get_raw_jwt
from blacklist import BLACKLIST
#resource is something client interact with. external representation of an object
#_vairable means private vaiable of the file
_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                            type=str,
                            required=True,
                            help='username can not be blank!'
                            )
_user_parser.add_argument('password',
                            type=str,
                            required=True,
                            help='password can not be blank!'
                            )
class UserRegister(Resource):
    
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message':'User already exist'},400
        else:
            user = UserModel(**data)  #   **data = (data['username'],data['password'])
            user.save_to_db()
            return {'message':'User created.','user':user.jason()},200

class User(Resource):
    def get(self,user_id):
        user = UserModel.find_by_userid(user_id)
        if user:
            return user.jason(),200
        return {'message':'User not found'},404


    def delete(self,user_id):
        user = UserModel.find_by_userid(user_id)
        if user:
            user.delete_from_db()
            return {'message':'User deleted'},200
        return {'message':'User not found'},404

class UserLogin(Resource):
    @classmethod
    def post(cls):
        #get data from parser
        data = _user_parser.parse_args()

        #find user in database
        user = UserModel.find_by_username(data['username'])

        #check password
        if user and safe_str_cmp(data['password'],user.password):
            access_token = create_access_token(identity = user.id,fresh = True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token':access_token,
                'refresh_token':refresh_token
            },200
        
        return {'message':'Invalid credentials.'},401  #unauthorized

#put the used token to blacklist to log user out
class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']  # jti is JWT unique identifier
        BLACKLIST.add(jti)
        return {'message':'Successfully logged out'}


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user,fresh = False)
        return {'access_token':new_token},200
