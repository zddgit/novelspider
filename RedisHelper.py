import redis


class RedisHelper:
    __pool = redis.ConnectionPool(host="192.168.10.53", port=8555)
    __redis = None

    def __init__(self):
        self.__redis = redis.Redis(connection_pool=self.__pool)

    def get_redis(self):
        return self.__redis
