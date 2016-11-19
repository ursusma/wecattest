import redis

CACHE_SERVER = {
    'host':'172.17.0.3',
    'port':6379,
    'database':0,
    'password':'',
}


class BaseCache(object):

    _host = CACHE_SERVER.get('host','')
    _port = CACHE_SERVER.get('port','')
    _database = CACHE_SERVER.get('database','')
    _password = CACHE_SERVER.get('password','')

    @property
    def redis_ctl(self):

        redis_ctl = redis.Redis(host=self._host,port=self._port,db=self._database,password=self._password)
        return redis_ctl
