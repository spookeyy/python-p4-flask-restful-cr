#!/usr/bin/env python3

from flask import Flask, request, make_response # request is a class from Flask that allows us to access the request object
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__) #Flask is a class from Flask that allows us to create our app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db) #Migrate is a class from Flask-Migrate (it's syntax is --- migrate = Migrate(app, db))
db.init_app(app) #db is a class from Flask-SQLAlchemy

api = Api(app) #Api is a class from Flask-RESTful responsible for creating routes in our app

class Home(Resource):
    def get(self):
        response_dict = {
            'status': 'success', 
            'message': 'Welcome to the Newsletter RESTful API', 
        }

        response = make_response( # 200, make_response is responsible for creating a response object
            response_dict,  # response_dict is the data that we want to return
            200 # status code
        )

        return response

api.add_resource(Home, '/') # add_resource is a method from Flask-RESTful that allows us to create routes

class Newsletters(Resource):
    def get(self):

        response_dict_list = [n.to_dict() for n in Newsletter.query.all()] # to_dict is a method from our model

        response = make_response(
            response_dict_list,
            200,
        )

        return response

    # creating records with POST requests
    def post(self):
        new_record = Newsletter(
            title=request.form['title'],
            body=request.form['body'],
        )

        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()

        response = make_response(
            response_dict,
            201, # status code for created
        )

        return response

api.add_resource(Newsletters, '/newsletters') #route for the resource class

class NewsletterByID(Resource):
    def get(self, id):
        response_dict = Newsletter.query.filter_by(id=id).first().to_dict()

        response = make_response(
            response_dict,
            200,
        )

        return response

api.add_resource(NewsletterByID, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
