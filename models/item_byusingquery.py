import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision = 2))

    def __init__(self,name,price):
        self.name=name
        self.price=price

    def jason(self):
        return {'name':self.name,'price':self.price}

    @classmethod
    def find_by_name(cls,name):
        conn=sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = 'select name,price from items where name = ?'

        result = cursor.execute(query,(name,))  #parameter must be a tuple
        row = result.fetchone()
        if row:
            item = cls(*row)
        else:
            item = None

        conn.close()
        return item
    
    
    def insert(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = 'insert into items (name,price) values (?,?)'
        cursor.execute(query,(self.name,self.price)) #parameter must be in a tuple
        conn.commit()
        conn.close()
    
    
    def update(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = 'update items set price = ? where name = ?'
        cursor.execute(query,(self.price,self.name)) #parameter must be in a tuple
        conn.commit()
        conn.close()
    
  
    def delete(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = 'delete from items where name = ?'
        cursor.execute(query,(self.name,)) #parameter must be in a tuple
        conn.commit()
        conn.close()
