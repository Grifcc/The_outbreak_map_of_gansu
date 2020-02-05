# -*- coding:utf-8 -*-
#       copyright:maxwell1280
#       pyechart==0.1.9.4

from pyecharts import Map
import requests
import json
import datetime

time=str(datetime.datetime.now())
title='甘肃疫情地图\n'+time[:-7]+'更新'

url = 'https://service-f9fjwngp-1252021671.bj.apigw.tencentcs.com/release/pneumonia'
html = requests.get(url).text
unicodestr=json.loads(html)  #将string转化为dict
new_list = unicodestr.get("data").get("listByArea")  #获取data中的内容，取出的内容为str
a = new_list[24]["cities"]
dic={}
for i in a:
    dic[i['cityName']]=i['confirmed']
attr = list(dic.keys())
value = list(dic.values())
name = {"甘南藏族自治州": "甘南",
        "临夏回族自治州":"临夏",
        "兰州市":"兰州",
        "嘉峪关市":"嘉峪关",
        "金昌市":"金昌",
        "白银市":"白银",
        "天水市":"天水",
        "武威市":"武威",
        "张掖市":"张掖",
        "平凉市":"平凉",
        "酒泉市":"酒泉",
        "庆阳市":"庆阳",
        "陇南市":"陇南",
        "定西市":"定西",}
standard=list(name.values())
for i in standard:
    if i not in attr:
        attr.append(i)
        value.append(0)
map = Map(title, title_color="#2E2E2E",
          title_text_size=20,title_top=20,
          title_pos="center", width=1200, height=600)

map.add("确诊", attr, value, type="effectScatter",maptype=u'甘肃',visual_range=[0, max(value)],
        is_visualmap=True, is_map_symbol_show=False,visual_range_text=['','确诊人数'],
        visual_range_color =["#F5F5F5","#FF8C00","#FF0000"],
        name_map = name,visual_text_color='#000')
map.show_config()
map.render('index.html')