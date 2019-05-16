from flask import Flask
from flask_restful import Api
from wsgi import add_resources
from utils.database_utils import (
    open_database_connection,
    close_database_connection,
    create_tables,
)

app = Flask(__name__)
api = Api(app)

add_resources(api)


@app.before_request
def before_request():
    open_database_connection()


@app.after_request
def after_request(response):
    close_database_connection()
    return response


app.before_first_request(create_tables)


if __name__ == '__main__':
    app.run(debug=True)
