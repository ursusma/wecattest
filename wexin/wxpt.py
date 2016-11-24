#!/usr/bin python
# -*- coding:utf-8 -*-
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wexin.settings")

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)

#import django
#django.setup()

from wexinapp.models import *

import re
import urllib.request
import requests
import string

def geturl(url):
    a = urllib.request.Request(url)
    a.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36' '(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
    dateurl = urllib.request.urlopen(url).read()
    return dateurl

def retext(dateurl):
    reimg = r'data-original="(.*)">'
    retitle = r'class="Post__rightContainer__title Post__rightContainer__title--newest".*\s*(.*)\s*</a>'
    retext = r'class="Post__rightContainer__summary Post__rightContainer__summary--newest">\s*(.*)\s*</a>'
    date = dateurl.decode('utf-8')
    img = re.findall(reimg,date)
    title = re.findall(retitle,date)
    text = re.findall(retext,date)
    tetol = [img,title,text]
    return tetol

def getstr(tetol):
    WxText.objects.all().delete()
    for i in range(0,3):
        url = tetol[0][i]
        urllib.request.urlretrieve(url,'/home/django/wexin/wexinapp/img/%s.jpg'%i)
        f = str(i) + '.jpg'
#        f = '/home/django/wexin/wexinapp/img/%s.jpg'%i
        name = ''
        gettitle = ''
        gettext = ''
        gettitle = tetol[1][i].rstrip()
        gettext = tetol[2][i].rstrip()
        WxText.objects.create(title=gettitle,img=url,text=gettext)

#def writetext(st):
#    f = open('news.doc','w')
#    f.write(st)
#    f.close

if __name__=='__main__':
    url = "http://wallstreetcn.com/"
    dateurl = geturl(url)
    tetol = retext(dateurl)
    text = getstr(tetol)
#    writetext(text)
