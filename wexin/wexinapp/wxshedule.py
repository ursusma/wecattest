from cache.tokencache import TokenCache

import sys
import requests
import json
import os

AppID = 'wxb957e3605e03b369'
AppSecret = 'a2445b89eaf6f07b8cc3699069e2a768'

config_get_access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (AppID, AppSecret)


class WxShedule(object):

    _token_cache = TokenCache()
    _expire_time_access_token = 7000 * 1000

    def get_access_token(self):

        url = config_get_access_token_url
        r = requests.get(url)
        if r.status_code == 200:
            res = r.text
            d = json.loads(res)
            if 'access_token' in d.keys():
                access_token = d['access_token']
                self._token_cache.set_access_cache(self._token_cache.KEY_ACCESS_TOKEN,access_token)
                self.get_jsapi_ticket()
                return access_token


    def get_jsapi_ticket(self):

        access_token = self._token_cache.get_cache(self._token_cache.KEY_ACCESS_TOKEN)
        if access_token:
            url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi' % access_token
            r = requests.get(url)
            if r.status_code == 200:
                res = r.text
                d = json.loads(res)
                errcode = d['errcode']
                if errcode == 0:
                    jsapi_ticket = d['ticket']
                    self._token_cache.set_access_cache(self._token_cache.KEY_JSAPI_TICKET,jsapi_ticket)


if __name__=='__main__':

    wx_shedule = WxShedule()
    wx_shedule.get_access_token()
