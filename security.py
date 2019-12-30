from werkzeug.security import safe_str_cmp
from models.user import UserModel
#This is not needed after users are stored in db
# users = [
#     User(1,'bob','adsf')
# ]

# username_mapping = {
#     u.username: u for u in users
# }

# userid_mapping = {
#     u.id: u for u in users
# }


def authenticate(username,password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password,password):
        return user

def identity(payload):  #payload is the content of JWT token
    user_id = payload['identity']
    return UserModel.find_by_userid(user_id)

