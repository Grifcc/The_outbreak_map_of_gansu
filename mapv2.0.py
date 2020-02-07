# -*- coding:utf-8 -*-
# copyright:maxwell1280
# pyechart==0.5.11

from pyecharts.charts import Bar, Page, Map
from pyecharts import options as opts
import requests
import json
from fake_useragent import UserAgent
import datetime


#从甘肃卫健委爬取疫情数据
ua = UserAgent()
headers = {"User-Agent": ua.random} # 伪造头
rs = requests.get("http://wsjk.gansu.gov.cn/yqdt/yq/getInfoGroupByCity", headers=headers).text
data=json.loads(rs)['data']['list']

#数据处理
dic_com={}
dic_cur={}
dead=data[0]['swrs']
cured=data[0]['zyrs']
comfired=data[0]['qzrs']

for i in data[1:]:
    dic_com[i['zsmc']]=i['qzrs']
    dic_cur[i['zsmc']] = i['zyrs']

city=[]    #城市名
for  j in dic_cur.keys():
    city.append(j[:2])


#各项数据
data_cur=list(zip(dic_cur.keys(), dic_cur.values()))  #治愈数据
data_com=list(zip(dic_com.keys(), dic_com.values()))  #确诊数据
time=str(datetime.datetime.now())   #更新时间
title='甘肃疫情地图'+time[:-7]+'更新'   #确诊地图主标题
link_git='https://github.com/Maxwell1280/The_outbreak_map_of_gansu'
link_qq='http://wpa.qq.com/msgrd?v=3&uin=1531045347&site=qq&menu=yes'
subtitle='全省确诊共计确诊{}例\n治愈出院{}例，死亡{}例\n(数据来源：甘肃卫健委)'.format(comfired,cured,dead)     #确诊地图副标题
text='源码连接:'+link_git     #直方图主标题
subtext='copyright@maxwell1280' \
     '\n反馈：maxwell1280\n企鹅号:1531045347'      #直方图副标题
path='/var/www/html/index.html'


#数据直方图
def bar_base():
    c = (
        Bar(init_opts=opts.InitOpts(width="1300px", height="550px"))
        .add_xaxis(city)
        .add_yaxis("治愈", list(dic_cur.values()),color='#FF0000')
        .add_yaxis("确诊", list(dic_com.values()),color='#00FF00')
        .set_global_opts(title_opts=opts.TitleOpts(title=text,title_link=link_git,subtitle_link=link_qq,
                                                   subtitle=subtext,pos_left='45%',pos_top='middle',item_gap=15,
                                                   title_textstyle_opts=opts.TextStyleOpts(color='#A9A9A9',
                                                                                           font_weight='normal',
                                                                                           font_size=15),
                                                   subtitle_textstyle_opts=opts.TextStyleOpts(color='#A9A9A9',
                                                                                              font_size=15)))
    )
    return c


#确证病例地图
def map_base_confirmed():
    c = (
        Map(init_opts=opts.InitOpts(width="1300px", height="700px"))
            .add("确诊", data_com, "甘肃", is_map_symbol_show=False)
            .set_global_opts(title_opts=opts.TitleOpts(title=title, subtitle=subtitle, pos_left='10%', item_gap=50,
                                                       subtitle_textstyle_opts=opts.TextStyleOpts(color='#FF0000',
                                                                                                  font_style='normal',
                                                                                                  font_weight='bold',
                                                                                                  font_family='Courier New',
                                                                                                  font_size=25)),

                             visualmap_opts=opts.VisualMapOpts(max_=max(dic_com.values()), range_text=['确诊人数', ''],
                                                               range_color=["#F5F5F5", "#FF8C00", "#FF0000"]),
                             toolbox_opts=opts.ToolboxOpts(is_show=True, orient="vertical", pos_top='middle'))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    return c


#治愈病例地图
def map_base_cured():
    c = (
        Map(init_opts=opts.InitOpts(width="1300px", height="550px"))
            .add("治愈", data_cur, "甘肃",  is_map_symbol_show=False)
            .set_global_opts(
                             visualmap_opts=opts.VisualMapOpts(max_=max(dic_cur.values()), range_text=['治愈人数', ''],
                                                               range_color=["#F5F5F5", "#ADFF2F", "#00FF00"]),
                             toolbox_opts=opts.ToolboxOpts(is_show=True, orient="vertical", pos_top='middle'))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    return c


#主函数
def main():
    page=Page(page_title='甘肃疫情地图')
    page.add(map_base_confirmed())
    page.add(map_base_cured())
    page.add(bar_base())
    page.render( )


if __name__ == "__main__":
    main()