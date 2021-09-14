# -*- coding:utf-8 -*-
#  2020/12/10 
#  raids.py
#  
# author:gyl
from tools.config import config_h
import redis
class redis_h(object):
    def __init__(self,host,port,db,decode_responses=False):
        self.host = host
        self.port = port
        self.db = db
        self._registry = []
        self.decode_responses=decode_responses
    def connect_redis(self):
        pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db,decode_responses=self.decode_responses)
        # pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db,decode_responses=True)
        red = redis.Redis(connection_pool=pool)
        return red

# rehis_h = redis_h(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB).connect_redis()
host=config_h.get_config('Redis','REDIS_HOST')
port=config_h.get_config('Redis','REDIS_PORT')
db = config_h.get_config('Redis','REDIS_DB')
rehis_h = redis_h(host=host, port=port, db=db,decode_responses=True).connect_redis()
rehis_h3 = redis_h(host=host, port=port, db=3,decode_responses=True).connect_redis()
