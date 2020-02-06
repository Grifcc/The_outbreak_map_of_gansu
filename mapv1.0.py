# -*- coding:utf-8 -*-
#       copyright:maxwell1280
#       pyechart==1.6.2
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.globals import RenderType
import requests
import json
import datetime

time=str(datetime.datetime.now())
title='甘肃疫情地图'+time[:-7]+'更新'

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

data=list(zip(attr,value))

def map_base() -> Map:
    c = (
        Map(init_opts=opts.InitOpts(width="1500px", height="700px",page_title= "甘肃疫情地图",renderer=RenderType.CANVAS ))
        .add("确诊", data, "甘肃",name_map=name,is_map_symbol_show=False)
        .set_global_opts(title_opts=opts.TitleOpts(title=title,pos_left='10%'),
                         visualmap_opts=opts.VisualMapOpts(max_=max(value),range_text=['确诊人数',''],
                                                           range_color=["#F5F5F5","#FF8C00","#FF0000"]),
                         toolbox_opts=opts.ToolboxOpts(is_show=True,orient= "vertical",pos_top='middle'))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    return c

map_base().render('index.html')