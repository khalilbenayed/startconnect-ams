from flask import Flask
from flask_restful import Api
from resources.student import add_student_resources
from utils.database_utils import (
    open_database_connection,
    close_database_connection,
    create_tables,
)

# define and create flask app and flask_restful api
app = Flask(__name__)
api = Api(app)


# register resources to the api
add_student_resources(api)


# open and close db connection before and after every request
# @app.before_request
# def before_request():
#     open_database_connection()
#
#
# @app.after_request
# def after_request(response):
#     close_database_connection()
#     return response


# create all tables if needed before first request
app.before_first_request(create_tables)


if __name__ == '__main__':
    app.run(debug=True)
