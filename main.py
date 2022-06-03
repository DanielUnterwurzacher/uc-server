# Declarative-Variante wird hier benutzt
import base64
import os

from flask import Flask, request,jsonify
from sqlalchemy import Column, Integer, Text, Float, DateTime, create_engine, BLOB
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func, or_
from flask_restful import Resource, Api
from dataclasses import dataclass
import json

from ai import faceRecognition

Base = declarative_base()  # Basisklasse aller in SQLAlchemy verwendeten Klassen
metadata = Base.metadata
engine = create_engine(r'sqlite:///C:\temp\diplomarbeit_uc.sqlite3')  # Welche Datenbank wird verwendet
db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))
Base.query = db_session.query_property()  # Dadurch hat jedes Base - Objekt (also auch ein GeoInfo) ein Attribut query für Abfragen

app = Flask(__name__)
api = Api(app)

@dataclass
class User(Base):
    __tablename__ = 'users'
    user_id: int
    name: str
    password: str
    image: str

    user_id = Column(Integer, primary_key=True)
    name = Column(Text)
    password = Column(Text)
    image = Column(Text)

@dataclass
class Article(Base):
    __tablename__ = 'product'
    product_id: int
    product_name: str
    amount: int
    user_id: int

    product_id = Column(Integer, primary_key=True)
    product_name = Column(Text)
    amount = Column(Integer)
    user_id = Column(Integer)

def encode_base64(fName):
    with open(fName, 'rb') as file:
        binary_file_data = file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        return base64_encoded_data.decode('utf-8')

def decode_Base64(fName, data):
    data_base64 = data.encode('utf-8')
    with open(fName, 'wb') as file:
        decoded_data = base64.decodebytes(data_base64)
        file.write(decoded_data)

class AllUserREST(Resource):
    def get(self):
        infos = User.query.all()
        return jsonify(infos)

class UserREST(Resource):
    def get(self, id):
        infos = User.query.get(id)
        return jsonify(infos)

    def put(self, id):
        d = request.get_json(force=True)['info']
        info = User(name=d['name'], password=d['password'], image=d['image'])
        db_session.add(info)
        db_session.flush()
        return jsonify({'message': 'user succesfully added'})

    def delete(self, id):
        info = User.query.get(id)
        if info is None:
            return jsonify({'message': 'user with id %d does not exist' % id})
        db_session.delete(info)
        db_session.flush()
        return jsonify({'message': 'picture with id %d deleted' % id})

    #gibt alle Artikel eines Users zurück
    def patch(self, id):
        #wird aufgerufen um Artikel eines Users zu bekommen, nicht um einen User zu ändern
        d = json.loads(request.data)
        enc = d['image']
        decode_Base64('img/android.png', enc)
        listFromDB = User.query.all()
        jlistDB = jsonify(listFromDB)
        strike = faceRecognition(enc, jlistDB)
        # gibt keinen User Zurück sondern seine Produkte!!!!
        infos = Article.query.filter(Article.user_id == strike).all()
        return jsonify(infos)

class ArticleREST(Resource):
    def get(self, id):
        infos = Article.query.get(id)
        return jsonify(infos)

    def put(self, id):
        d = request.get_json(force=True)['info']
        info = Article(product_name=d['product_name'], amount=d['amount'], user_id=d['user_id'])
        db_session.add(info)
        db_session.flush()
        return jsonify({'message': 'article added'})

    def delete(self, id):
        info = Article.query.get(id)
        if info is None:
            return jsonify({'message': 'article with id %d does not exist' % id})
        db_session.delete(info)
        db_session.flush()
        return jsonify({'message': 'article with id %d deleted' % id})

    #ändert alle Artikel eines Users
    def patch(self, id):
        info = User.query.get(id)
        if info is None:
            return jsonify({'message': 'user with id %d does not exist' % id})
        data = json.loads(request.form['info'])
        for i in range(0,len(data)):
            infoArticle = Article.query.get(data[i]['product_id'])
            if infoArticle is None:
                return jsonify({'message': 'article with id %d does not exist' % data[i]['product_id']})
            infoArticle.product_name = data[i]['product_name']
            infoArticle.amount = data[i]['amount']
            db_session.add(infoArticle)
        db_session.flush()
        return jsonify({'message': 'user articles with userid %d modified' % id})

api.add_resource(UserREST, '/user/<int:id>')
api.add_resource(ArticleREST, '/article/<int:id>')
api.add_resource(AllUserREST, '/user')

@app.teardown_appcontext
def shutdown_session(exception=None):
    print("Shutdown Session")
    db_session.remove()

def init_db():
    # Erzeugen der Tabellen für die Klassen, die oben deklariert sind (muss nicht sein, wenn diese schon existiert)
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()
    app.run(debug=True,host='0.0.0.0')


