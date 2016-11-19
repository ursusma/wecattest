from .basecache import BaseCache

class TokenCache(BaseCache):

    expire_access_token = 7200
    expire_js_token = 30 * 24 * 3600
    KEY_ACCESS_TOKEN = 'access_token'
    KEY_JSAPI_TICKET = 'jsapi_ticket'


    def set_access_cache(self,key,value):

        res = self.redis_ctl.set(key,value)
        self.redis_ctl.expire(key,self.expire_access_token)
        return res


    def set_js_cache(self,key,value):

        res = self.redis_ctl.set(key,value)
        self.redis_ctl.expire(key,self.expire_js_token)
        return res


    def get_cache(self,key):

        try:
            v = (self.redis_ctl.get(key)).decode('utf-8')
            return v
        except Exception:
            return None
