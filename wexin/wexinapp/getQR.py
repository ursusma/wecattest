from cache.tokencache import TokenCache

import json
import requests
import urllib.request

get_QR_url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket='
post_QR_url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token='
token_cache = TokenCache()

def post_data():
    post_file = {
        "action_name":"QR_LIMIT_SCENE",
        "action_info":{
            "scene":{
                "scene_str":"1"
            }
        }
    }
    access_token = token_cache.get_cache(token_cache.KEY_ACCESS_TOKEN)
    url = post_QR_url + access_token
    r = requests.post(url,data=json.dumps(post_file))
    res = json.loads(r.text)
    ticket_file = res['ticket']
    url = get_QR_url + ticket_file
    urllib.request.urlretrieve(url,'/home/django/wexin/wexinapp/img/qr_code.jpg')
    return url

if __name__=='__main__':
    print(post_data())
