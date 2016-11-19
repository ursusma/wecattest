from cache.tokencache import TokenCache

import requests
import json

menu_create_url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token='

menu_get_url = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token='

menu_delete_url = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token='

class WxMenuServer(object):

    _token_cache = TokenCache()

    def create_menu(self):

        access_token = self._token_cache.get_cache(self._token_cache.KEY_ACCESS_TOKEN)
        if access_token:
            url = menu_create_url + access_token
            data = self.create_menu_data()
            r = requests.post(url,data.encode('utf-8'))
            if r.status_code == 200:
                res = r.text
                json_res = json.loads(res)
                if 'errcode' in json_res.keys():
                    errcode = json_res['errcode']
                    return errcode


    def get_menu(self):

        access_token = self._token_cache.get_cache(self._token_cache.KEY_ACCESS_TOKEN)
        if access_token:
            url = menu_get_url + access_token
            r = requests.get(url)
            if r.status_code == 200:
                res = r.text
                json_res = json.loads(res)
                if 'errcode' in json_res.keys():
                    errcode = json_res['errcode']
                    return errcode


    def delete_menu(self):

        access_token = self._token_cache.get_cache(self._token_cache.KEY_ACCESS_TOKEN)
        if access_token:
            url = menu_delete_url + access_token
            r = requests.get(url)
            if r.status_code == 200:
                res = r.text
                json_res = json.loads(res)
                if 'errcode' in json_res.keys():
                    errcode = json_res['errcode']
                    return errcode


    def create_menu_data(self):

        menu_data = {
            "button":[
            {
                "type":"view",
                "name":"test",
                "url":"http://www.51huiu.cn/lnr"
            },

            {
                "name":"tool set",
                "sub_button":[
                {
                    "type":"click",
                    "name":"joke",
                    "key":"v1001_joke"
                },
                {
                    "type":"click",
                    "name":"translate",
                    "key":"v1001_translate"
                },
                {
                    "type":"click",
                    "name":"weather",
                    "key":"v1001_weather"
                }
                ]
            },

            {
                "type":"view",
                "name":"about me",
                "url":"http://www.51huiu.cn/lnr"
            }
            ]
        }
        MENU_DATA = json.dumps(menu_data,ensure_ascii=False)
        return MENU_DATA


if __name__=='__main__':

    wx_menu_server = WxMenuServer()
    wx_menu_server.create_menu()
