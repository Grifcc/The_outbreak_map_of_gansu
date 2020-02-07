from pyecharts.faker import Faker
from pyecharts.charts import Bar, Tab, Page,Grid, Map
from pyecharts import options as opts
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
dic_com={}
dic_cur={}
dead=0
cured=0
#{'cityName': '平凉', 'confirmed': 1, 'suspected': 0, 'cured': 0, 'dead': 0}
for i in a:
    dic_com[i['cityName']]=i['confirmed']
    dic_cur[i['cityName']] = i['cured']
    dead+=i['dead']
    cured+=i['cured']
attr_com = list(dic_com.keys())
value_com= list(dic_com.values())
attr_cur = list(dic_cur.keys())
value_cur= list(dic_cur.values())
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
standard_com=list(name.values())
standard_cur=list(name.values())
for i in standard_com:
    if i not in attr_com:
        attr_com.append(i)
        value_com.append(0)
for i in standard_cur:
    if i not in attr_cur:
        attr_cur.append(i)
        value_cur.append(0)

data_com=list(zip(attr_com,value_com))
data_cur=list(zip(attr_cur,value_cur))
subtitle='全省确诊共计确诊{}例\n治愈出院{}例，死亡{}例'.format(sum(value_com),cured,dead)
text='源码连接:https://github.com/Maxwell1280/The_outbreak_map_of_gansu'
subtext='copyright@maxwell1280' \
     '\n反馈：maxwell1280\n企鹅号:1531045347'
def bar_base():
    c = (
        Bar(init_opts=opts.InitOpts(width="1300px", height="550px"))
        .add_xaxis(attr_com)
        .add_yaxis("治愈", value_cur,color='#FF0000')
        .add_yaxis("确诊", value_com,color='#00FF00')
        .set_global_opts(title_opts=opts.TitleOpts(title=text,title_link='https://github.com/Maxwell1280/The_outbreak_map_of_gansu',
                                                   subtitle_link='http://wpa.qq.com/msgrd?v=3&uin=1531045347&site=qq&menu=yes',
                                                   subtitle=subtext,pos_left='45%',pos_top='middle',item_gap=15,
                                                   title_textstyle_opts=opts.TextStyleOpts(color='#A9A9A9',font_weight='normal',font_size=15),
                                                   subtitle_textstyle_opts=opts.TextStyleOpts(color='#A9A9A9',font_size=15)))
    )
    return c

def map_base_confirmed():
    c = (
        Map(init_opts=opts.InitOpts(width="1300px", height="700px"))
            .add("确诊", data_com, "甘肃", name_map=name, is_map_symbol_show=False)
            .set_global_opts(title_opts=opts.TitleOpts(title=title, subtitle=subtitle, pos_left='10%', item_gap=50,
                                                       subtitle_textstyle_opts=opts.TextStyleOpts(color='#FF0000',
                                                                                                  font_style='normal',
                                                                                                  font_weight='bold',
                                                                                                  font_family='Courier New',
                                                                                                  font_size=25)),

                             visualmap_opts=opts.VisualMapOpts(max_=max(value_com), range_text=['确诊人数', ''],
                                                               range_color=["#F5F5F5", "#FF8C00", "#FF0000"]),
                             toolbox_opts=opts.ToolboxOpts(is_show=True, orient="vertical", pos_top='middle'))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    return c

def map_base_cured():
    c = (
        Map(init_opts=opts.InitOpts(width="1300px", height="550px"))
            .add("治愈", data_cur, "甘肃", name_map=name, is_map_symbol_show=False)
            .set_global_opts(
                             visualmap_opts=opts.VisualMapOpts(max_=max(value_cur), range_text=['治愈人数', ''],
                                                               range_color=["#F5F5F5", "#ADFF2F", "#00FF00"]),
                             toolbox_opts=opts.ToolboxOpts(is_show=True, orient="vertical", pos_top='middle'))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    return c



page=Page(page_title='甘肃疫情地图')
page.add(map_base_confirmed())
page.add(map_base_cured())
page.add(bar_base())
page.render()