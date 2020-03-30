#coding:utf-8
#Name        : BingDesktop.py
#Version     : 1.00 (Python3 version)
#Usage       : BingDesktop.py
#Description : 通过爬虫获取图片URL和信息, 下载图片到指定位置, 设置墙纸
#Date        : 2020/3/27
#Author      : dahai.zhou

import urllib.request
import requests
import os.path
import ctypes
import datetime
import time
from bs4 import BeautifulSoup
import re

# 保存图片到本地硬盘文件夹LocalFolderPath中
def DownloadPictureToLocal(Picture, LocalFolderPath):
    try:
        if not os.path.exists(LocalFolderPath):
            print ('文件夹', LocalFolderPath, '不存在，重新建立')
            os.makedirs(LocalFolderPath)
        # 拼接目录与文件名，得到图片路径
        FullPath = os.path.join(LocalFolderPath, str(datetime.date.today())+'('+Picture[1]+')'+'.jpg')
        # 下载图片，并保存到文件夹中
        urllib.request.urlretrieve(Picture[0], FullPath)
    except IOError as e:
        print ('文件操作失败', e)
        exit(1)
    except Exception as e:
        print ('错误 ：', e)
        exit(1)
    return FullPath

# 请求网页，解析并获取图片URL和图片信息 (哪里, 谁拍的, copyright等)
# 函数版本v1.0, 适用于2020/3/27
def GetPictureUrlAndInfo(BingUrl = 'https://cn.bing.com/'):
    r = requests.get(BingUrl)
    soup = BeautifulSoup(r.text, 'lxml')
    div1 = soup.find_all('link', id="bgLink")
    PictureUrl = BingUrl + div1[0].get('href')

    div2 = soup.find_all('a', id="sh_cp")
    PictureInfo = div2[0].get('title').encode("GBK", "ignore").decode("GBK")  # 过滤copyright符号, 否则Python打印会出错
    PictureInfo = re.sub('[\/:*?"<>|]', '-', PictureInfo)  # 过滤斜杠等
    return [PictureUrl, PictureInfo]

# 设置图片绝对路径FullPath所指向的图片为壁纸
def SetWallpaper(FullPath):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, FullPath, 0)

# 通过爬虫获取图片URL和信息, 下载图片到指定位置, 设置墙纸
def main():
    LocalFolderPath = r"E:\Picture\Bing"       # 图片要被保存在的位置
    Picture = GetPictureUrlAndInfo()     # 获取图片URL和信息, 返回值为list
    FullPath = DownloadPictureToLocal(Picture, LocalFolderPath)
    SetWallpaper(FullPath)
    print("成功保存至如下地址并设置墙纸:", FullPath)
    time.sleep(10)

main()
