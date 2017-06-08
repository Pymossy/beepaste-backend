import yaml
from sanic import Sanic
from sanic.response import json
from SanicMongo import connect

from api import views, tools
from tools import get_config, get_logger

logger = get_logger('beepaste')

web_cnf = get_config('web_server')
mongo_cnf = get_config('mongodb')

logger.info('initiating connection to mongodb using config')
connect(**mongo_cnf)
logger.info('connected to mongodb')

app = Sanic('beepaste')

tools.add_api_routes(app)

if __name__ == "__main__":
    logger.info('Starting server')
    app.run(**web_cnf)
