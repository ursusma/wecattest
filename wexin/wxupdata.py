import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wexin.settings")

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)

from wexinapp.cache.tokencache import TokenCache
from wexinapp.models import *

import requests
import json

updata_img_url = 'https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token='

updata_source_url = 'https://api.weixin.qq.com/cgi-bin/media/uploadnews?access_token='

updata_mass_url = 'https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token='

file_url = "http://file.api.weixin.qq.com/cgi-bin/media/upload?access_token="

appid = 'you addid'
appsecret = 'you appsecret'
access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (appid, appsecret)
r_test = requests.get(access_token_url)
res_test = json.loads(r_test.text)
getres_test = res_test['access_token']

class WxUpdata(object):

    _token_cache = TokenCache()
    wxdata = WxText.objects.all()

    def imgupdata(self):
#        access_token = self._token_cache.get_cache(self._token_cache.KEY_ACCESS_TOKEN)
        access_token = getres_test
        url = file_url + access_token + '&type=image'
        s = []
        if access_token:
            for i in range(0,3):
                id = i
                get_id = '/home/django/wexin/wexinapp/img/%d.jpg' %(i)
                fis = {'media':open(get_id,'rb')}
                try:
                    r = requests.post(url=file_url,files=fis)
                    if r.status_code == 200:
                        res = json.loads(r.text)
                        s.append(res["media_id"])
                except:
                    err = open('/home/django/wexin/wexinapp/log.txt','a')
                    err.write('img error'+'/n')
                    err.close()
            return s

    def sourceupdata(self):
#        access_token = self._token_cache.get_cache(self._token_cache.KEY_ACCESS_TOKEN)
        access_token = getres_test
        a = []
        m_id = []
        if access_token:
            try:
                url = updata_source_url + access_token
                t = []
                te = []
                for i in wxdata:
                    t.append(i.title.encode('utf-8'))
                    te.append(i.text.encode('utf-8'))
                a = [t,te]
                formdata = updataform(a)
                r = requests.post(url,data=json.dumps(formdata))
                if r.status_code == 200:
                    res = json.loads(r.text)
                    m_id.append(res['media_id'])
                return m_id
            except:
                err = open('/home/django/wexin/wexinapp/log.txt','a')
                err.write('source error'+'/n')
                err.close()

    def massupdata(self):
#        access_token = self._token_cache.get_cache(self._token_cache.KEY_ACCESS_TOKEN)
        access_token = getres_test
        if access_token:
            try:
                url = updata_mass_url + access_token
                uppost = updatamass()
                r = requests.post(url,data=json.dumps(uppost))
                getjson = json.loads(r.text)
                err = open('/home/django/wexin/wexinapp/log.txt','a')
                err.write(getjson['errmsg'] + '/n')
                err.close()
            except:
                err = open('/home/django/wexin/wexinapp/log.txt','a')
                err.write('mass error'+'/n')
                err.close()

    def updataform(a):
        imgtext = imgupdata()
        dataform = {
            "articles": [
                {
                    "thumb_media_id":imgtext[0],
             title":a[0][0],
                    "content":a[1][0],
		},
                {
                    "thumb_media_id":imgtext[1],
                    "title":a[0][1],
                    "content":a[1][1],
                },
                {
                    "thumb_media_id":imgtext[2],
                    "title":a[0][2],
                    "content":a[1][2],
                }
            ]
        }
        return dataform

    def updatamass(self):
        meid = sourceupdata()
        mass_form = {
            "filter":{
                "is_to_all":"false",
                "group_id":"0"
            },
            "mpnews":{
                "media_id":meid
            },
            "msgtype":"mpnews"
        }
        return mass_form

if __name__=='__main__':
    wxupdata = WxUpdata()
    wxupdata.massupdata()
