from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
from .models import *
from datetime import datetime
from django.utils.encoding import smart_str

import urllib.request
import re
import os
import hashlib
import json
import requests
import traceback
import xml.etree.ElementTree as ET
import time

# Create your views here.

wxtoken = 'yourtoken'
key = 'your tuling key'
url = 'http://www.tuling123.com/openapi/api'
#appid = ''
#appsecret = ''
appid = 'yourappid'
appsecret = 'youraddsecret'

@csrf_exempt
def lnr(request):

    def get(request):
        signature = request.GET.get("signature","")
        timestamp = request.GET.get("timestamp","")
        nonce = request.GET.get("nonce","")
        echostr = request.GET.get("echostr","")
        token = wxtoken

        tmp_list = [token,timestamp,nonce]
        tmp_list.sort()
        tmp_str = tmp_list[0] + tmp_list[1] + tmp_list[2]
        tmpstr = hashlib.sha1(tmp_str.encode('utf-8')).hexdigest()

        if tmpstr == signature:
            return echostr
        else:
            return 'error'

    def datatext(t):
        text = getjson(t)
        return text

    def dataimage(u):
#        i = 'picture url:' + u + 'mediaid:' + m
        i = 'picture url:' + u
        return i

    def datavoice(format):
        f = 'format:' + format
        return f

    def datalocation(x,y,s,l):
        t = 'position:' + x + ' ' + y + '\n' + 'size:' + s + '\n' + l
        return t

    def datalink(t,d,u):
        t = 'title:' + t + '\n' + 'des:' + d + '\n' + 'url:' + u
        return t

    def dataevent(xmldata):
        if xmldata.find('Event').text == 'subscribe':
            username = xmldata.find('FromUserName').text
            t = 'welcome subscribe!if you need help,please set "help"'
            return t
        elif xmldata.find('Event').text == 'subscribe' and xmldata.find('EventKey').text != '':
            t = 'no subscribe users scanning QR code,KEY:' + xmldata.find('EventKey').text + '\n' + 'ticket:' + xmldata.find('Ticket').text
            return t
        elif xmldata.find('Event').text == 'SCAN':
            t = 'subscribe users scanning QR code,KEY:' + xmldata.find('EventKey').text + '\n' + 'ticket:' + xmldata.find('Ticket').text
            return t
        elif xmldata.find('Event').text == 'LOCATION':
            t = 'geography' + '\n' + xmldata.find('Latitude').text + '\n' + xmldata.find('Longitude').text + '\n' + 'Precision' + xmldata.find('Precision').text
            return t
        elif xmldata.find('Event').text == 'CLICK':
            t = 'click event,key:' + xmldata.find('EventKet').text
            return t
        else:
            pass

#    def datavideo():
#        s

    def retext(to,fr,te):
        ti = int(time.time())
        xmlForm = '''
            <xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%d</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[%s]]></Content>
            </xml>
            '''%(fr,to,ti,te)
        return xmlForm

    def post(request):
        xmlData = ET.fromstring(request.body)
        touser = xmlData.find('ToUserName').text
        fromuser = xmlData.find('FromUserName').text
        test = xmlData.find('MsgType').text

        if test == 'text':
            t = xmlData.find('Content').text
            text = datatext(t)
        elif test == 'image':
            picurl = xmlData.find('PicUrl').text
#            medid = xmlData.find('MediaId').text
            ima = dataimage(picurl)
        elif test == 'voice':
            format = xmlData.find('Format').text
            text = datavoice(format)
        elif test == 'location':
            x = xmlData.find('Location_X').text
            y = xmlData.find('Location_Y').text
            size = xmlData.find('Scale').text
            label = xmlData.find('Label').text
            text = datalocation(x,y,size,label)
        elif test == 'link':
            title = xmlData.find('Title').text
            des = xmlData.find('Description').text
            url = xmlData.find('Url').text
            text = datalink(title,des,url)
        elif test == 'video':
            text = 'this is video'
        elif test == 'event':
            text = dataevent(xmlData)

        res = retext(touser,fromuser,text)
        return res

    def getjson(recMsg):
        f = {"key":key,"info":recMsg}
        r = requests.post(url,data=f)
        resp = r.text
        if len(resp) == 0:
            return None
        js = json.loads(resp)
        if js['code'] == 100000:
            return js['text'].replace('<br>','\n')
        elif js['code'] == 200000:
            return js['url']
        else:
            return None
#
#    def resplay(to,fr,con):
#        ti = int(time.time())
#        xmlForm = '''
#            <xml>
#            <ToUserName><![CDATA[%s]]></ToUserName>
#            <FromUserName><![CDATA[%s]]></FromUserName>
#            <CreateTime>%d</CreateTime>
#            <MsgType><![CDATA[text]]></MsgType>
#            <Content><![CDATA[%s]]></Content>
#            </xml>
#            '''%(to,fr,ti,con)
#        return xmlForm
#
#    def post(request):
#        xmlData = ET.fromstring(request.body)
#
#        touser = xmlData.find('ToUserName').text
#        fromuser = xmlData.find('FromUserName').text
#        msgtype = xmlData.find('MsgType').text
#        content = xmlData.find('Content').text.encode('utf-8')
#
#        aio = getjson(content)
#
#        da = [touser,fromuser,msgtype,aio]
#
#        if da[2] == 'text':
#            to = da[1]
#            fr = da[0]
#            con = da[3]
#            res = resplay(to,fr,con)
#            return res
        

    if request.method == "GET":
        return HttpResponse(get(request))
    elif request.method == "POST":
        return HttpResponse(post(request))
