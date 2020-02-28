import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

from monkey.config import config

from monkey.utils.tools import singleton

@singleton
class MotorBase:
    '''
    About motor's doc https://github.com/mongodb/motor
    '''
    _db = {}
    _collection = {}
    MONGODB = Config.MONGODB

    def __init__(self,loop=None):
        self.motor_uri = ''
        self.loop = loop or asyncio.get_event_loop()
    
    def client(self, db):
        # motor
        self.motor_uri = 'mongodb://{account}{host}:{port}/database'.format(
            account = '{username}:{password}@'.format(
                username = self.MONGODB['MONGO_USERNAME'],
                password = self.MONGODB['MONGO_PASSWORD'] if self.MONGODB['MONGO_USERNAME'] else '',
            host = self.MONGODB['MONGO_HOST'] if self.MONGODB[]

            )
        )