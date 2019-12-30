
from flask_restful import Resource,reqparse
from models.user import UserModel
#resource is something client interact with. external representation of an object

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help='username can not be blank!'
        )
    parser.add_argument('password',
        type=str,
        required=True,
        help='password can not be blank!'
        )
    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message':'User already exist'},400
        else:
            user = UserModel(**data)  #   **data = (data['username'],data['password'])
            user.save_to_db()
            return {'message':'User created.','user':user.jason()},200

            


        