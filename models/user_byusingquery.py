import sqlite3
from db import db
#model is something used internally. internal representation of an object
class UserModel(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))



    def __init__(self,_id,username,password):
        self.id = _id
        self.username=username
        self.password = password

    @classmethod
    def find_by_username(cls,username):
        conn=sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = 'select id,username,password from users where username = ?'

        result = cursor.execute(query,(username,))  #parameter must be a tuple
        row = result.fetchone()
        if row:
            user = cls(*row)   #*row = row[0],row[1],row[2]
        else:
            user = None

        conn.close()
        return user

    @classmethod
    def find_by_userid(cls,_id):
        conn=sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = 'select id,username,password from users where id = ?'

        result = cursor.execute(query,(_id,))  #parameter must be a tuple
        row = result.fetchone()
        if row:
            user = cls(*row)   #*row = row[0],row[1],row[2]
        else:
            user = None

        conn.close()
        return user
