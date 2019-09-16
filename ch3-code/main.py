#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from api.utils.database import db
from api.utils.responses import response_with
import api.utils.responses as resp
from api.routes.authors import author_routes
from api.routes.books import book_routes
from api.routes.users import user_routes
from flask_jwt_extended import JWTManager
from api.config.config import DevelopmentConfig, ProductionConfig, TestingConfig

app = Flask(__name__)


if os.environ.get('WORK_ENV') == 'PROD':
    app_config = ProductionConfig
elif os.environ.get('WORK_ENV') == 'TEST':
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig

app.config.from_object(app_config)

db.init_app(app)
with app.app_context():
    db.create_all()
app.register_blueprint(author_routes, url_prefix='/api/authors')
app.register_blueprint(book_routes, url_prefix='/api/books')
app.register_blueprint(user_routes, url_prefix='/api/users')


# START GLOBAL HTTP CONFIGURATIONS
@app.after_request
def add_header(response):
    return response

@app.errorhandler(400)
def bad_request(e):
    logging.error(e)
    return response_with(resp.BAD_REQUEST_400)

@app.errorhandler(500)
def server_error(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_500)

@app.errorhandler(404)
def not_found(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_404)

# END GLOBAL HTTP CONFIGURATIONS


jwt = JWTManager(app)
db.init_app(app)
with app.app_context():
    # from api.models import *
    db.create_all()
    
if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", use_reloader=False)