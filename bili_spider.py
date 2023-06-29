'''
author:零晨的小工具箱
email：lingchenbox@163.com
time:20230629
usage:输入个人空间链接，格式如下：https://space.bilibili.com/37090048/video
function：获取某一个up主的视频播放量、上传日期、以及视频名称
'''

from lxml import  etree
from selenium import webdriver
import time
import xlwt
play_num = []
title_bili = []
release_time = []
up_space_url = input("输入需要收集的up个人空间链接:") #类似：https://space.bilibili.com/37090048/video

browser = webdriver.Chrome()
browser.get(up_space_url)
time.sleep(3)  #防止网页未加载完成报错
html = etree.HTML(browser.page_source)

try:
    page_num= html.xpath("//*[@id=\"submit-video-list\"]/ul[3]/span[1]/text()")[0].strip(" 页，").strip("共 ") #获取所有页数

except:
    page_num = 1  #因为只有一页视频的xpath会报错，索性直接赋值

up_name = html.xpath("//*[@id=\"h-name\"]/text()")[0]  #姓名
fans_num = html.xpath('//*[@id="n-fs"]/text()')[0].strip() #粉丝数获取之后是带有回车符号和空格
print(int(page_num))
print(up_name)
print(fans_num)



for i in range(1,int(page_num)+1):


    browser.get(up_space_url + "?tid=0&pn="+ str(i) +"&keyword=&order=pubdate") #逐页获取bilibili网址，B站规则更改了，之前是使用ajax加载，现在直接用网址就可以获取不同页的数据了
    time.sleep(3)
    html = etree.HTML(browser.page_source)
    title_bili0 = html.xpath("//*[@id=\"submit-video-list\"]/ul[2]/li/a[2]/text()")  # 视频标题
    play_num1 = html.xpath("//*[@id=\"submit-video-list\"]/ul[2]/li/div/span[1]/span/text()")  #播放量
    play_num1 = [j.strip() for j in play_num1]
    play_num0 = []
    for k in play_num1:    #把文本改成数字格式
        try :
            int(k)
            play_num0.append(int(k))
        except:             #这一部分就是”1.4万“这一类的。
            play_num0.append(float(k.strip("万"))*10000)


    release_time0 = html.xpath("//*[@id=\"submit-video-list\"]/ul[2]/li/div/span[2]/text()") #视频发布时间
    release_time0 = [j.strip().replace("-","/") for j in release_time0]
    title_bili = title_bili + title_bili0
    play_num = play_num + play_num0
    release_time = release_time + release_time0

print(title_bili,play_num,release_time) #将获取到的三种数据打印出来，随b站规则变化xpath规则也要随之更新，容易察觉到问题

browser.close()

wb = xlwt.Workbook(encoding='utf-8')
ws1 = wb.add_sheet(sheetname="b站up主选题及播放数据")
ws1.write(0, 0, '标题')
ws1.write(0, 1, '播放量')
ws1.write(0, 2, '上传时间')

for i in range(3):
    for j in range(len(title_bili)):
        if i == 0:
            ws1.write(j+1, i, title_bili[j])  #参数1，行；参数2，列；参数3，要写入的值。
        elif i == 1:
            ws1.write(j + 1, i, play_num[j])
        else:
            ws1.write(j + 1, i, release_time[j])

wb.save("D:/b站选题-{}.xls".format(up_name + "-fans" + fans_num))
