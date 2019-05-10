from flask import Flask
from flask_restful import Resource, Api
from wsgi import add_resources

app = Flask(__name__)
api = Api(app)

add_resources(api)

if __name__ == '__main__':
    app.run(debug=True)