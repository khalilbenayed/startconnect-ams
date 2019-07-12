from flask import Flask
from flask_restful import Api
from resources import (
    add_student_resources,
    add_company_resources,
    add_job_resources,
)
from utils.database_utils import (
    create_tables,
)


# define and create flask app and flask_restful api
def create_app(config_name):
    app = Flask(config_name)
    api = Api(app)

    # register resources to the api
    add_student_resources(api)
    add_company_resources(api)
    add_job_resources(api)

    # create all tables if needed before first request
    app.before_first_request(create_tables)
    return app, api


app, api = create_app(__name__)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
