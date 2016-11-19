class WxConfig(object):

    APPID = 'wxb957e3605e03b369'
    AppSecret = 'a2445b89eaf6f07b8cc3699069e2a768'

    config_get_access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (AppID, AppSecret)

    menu_create_url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token='

    menu_get_url = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token='

    menu_delete_url = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token='
