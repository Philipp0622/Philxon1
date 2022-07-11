#!/bin/python3
from doctest import debug
from flask import Flask, request
from flask_restful import Resource, Api
import pymysql.cursors
import json
import os

app = Flask(__name__)
api = Api(app)

test = "test"

# Set default values
default_db_ip = '34.159.3.127'
default_db_user = 'pexon-training'
default_db_password = 'pexon-training2022!'
default_db_name = 'books'
db_charset = 'utf8mb4'

# Init Database
db_connection = pymysql.connect(
  host=os.environ.get('DB_HOST', '34.159.3.127'),
  user=os.environ.get('DB_USER', 'pexon-training'),
  password=os.environ.get('DB_PASSWORD', 'pexon-training2022!'),
  db=os.environ.get('DB_NAME', 'books'),
  charset='utf8mb4',
  cursorclass=pymysql.cursors.DictCursor
)

db_cursor = db_connection.cursor()

@ app.route("/hello", methods=['GET', 'POST', 'DELETE']) # Hier kannst Du Routen definieren, über die die App erreichbar ist
def books():
    return "Hello World"

def db_get(sql):
    db_cursor.execute(sql)
    return db_cursor.fetchall()

def db_post(sql, values):
  db_cursor.execute(sql, values)
  db_connection.commit()
  return db_cursor.fetchall()

class GetAllBooks(Resource):
    def get(self):
        result = None
        sql = 'SELECT * FROM books'
        result = db_get(sql)
        return result
        

class GetBookById(Resource):
    def get(self, id):
        result = None
        sql = "SELECT * FROM books WHERE id ='"+ str(id) +"'"
        result = db_get(sql)
        return result

class GetBookByYear(Resource):
    def get(self, year):
        result = None
        sql = "SELECT * FROM books WHERE year_written ='"+ str(year) +"'"
        result = db_get(sql)
        return result

class AddNewBook(Resource):
    def post(self):
        result = None
        body = request.json
        sql = 'INSERT INTO books (title, year_written, author) VALUES (%s, %s, %s)'
        result = db_post(sql, (body['title'], body['year_written'], body['author']))
        return json.dumps(result)

class DeleteBookById(Resource):
    def delete(self, id):
        result = None
        sql = "DELETE FROM books WHERE id ='"+ str(id) +"'"
        result = db_get(sql)
        return result

api.add_resource(GetAllBooks, '/api/v1/book')
api.add_resource(GetBookById, '/api/v1/book/<int:id>')
api.add_resource(GetBookByYear, '/api/v1/book/year/<int:year>')
api.add_resource(AddNewBook, '/api/v1/book')
api.add_resource(DeleteBookById, '/api/v1/book/<int:id>')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Erhalte den Port aus der Environment Variable, sonst benutze 80
    app.run(host='0.0.0.0', port=port)      # Starte die App