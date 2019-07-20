import yaml
import os
from flask import (
    Flask,
    request,
    jsonify
)
from flask_restful import Api
from resources import (
    add_student_resources,
    add_company_resources,
    add_job_resources,
)
from utils.database_utils import (
    create_tables,
)

with open("config.yaml") as cfg_file:
    cfg = yaml.load(cfg_file, Loader=yaml.Loader).get(os.environ['ENV'])


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


@app.before_request
def authorize_token():
    try:
        auth_header = request.headers.get("Authorization")
        if "Bearer" in auth_header:
            token = auth_header.split(' ')[1]
            if token != cfg.get('api-key'):
                raise ValueError('Authorization failed.')
        else:
            raise ValueError('Authorization failed.')
    except Exception:
        return jsonify({}), 401


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
