from SanicMongo import connect
from beepaste import logger
from beepaste import mongo_cnf
from beepaste import app


@app.listener('after_server_start')
async def notify_mongo_started(app, loop):
    # db init
    logger.info('initiating connection to mongodb using config')
    connect(**mongo_cnf)
    logger.info('connected to mongodb')