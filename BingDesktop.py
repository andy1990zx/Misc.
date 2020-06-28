#coding:utf-8
"""
BSD 2-Clause License

Copyright (c) 2020, Sea Zhou (WeChat: uefi64)
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
"""

"""
Name        : BingDesktop.py
Usage       : BingDesktop.py
EXE Package : pyinstaller -F BingDesktop.py
Description : 通过爬虫获取图片URL和信息, 下载图片到指定位置, 设置墙纸
Author      : andy1990zx@163.com
Change      :
Data          Name          Version    Description
2020/4/23     andy1990zx    1.01       Add output string; fix the issue sometime set wallpaper fail
"""

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
def GetPictureUrlAndInfo(BingUrl = 'https://cn.bing.com'):
    r = requests.get(BingUrl)
    soup = BeautifulSoup(r.text, 'lxml')
    div1 = soup.find_all('link', id="bgLink")
    PictureUrl = BingUrl + div1[0].get('href')

    div2 = soup.find_all('a', id="sh_cp")
    PictureInfo = div2[0].get('title').encode("GBK", "ignore").decode("GBK")
    PictureInfo = re.sub('[\/:*?"<>|]', '-', PictureInfo)
    return [PictureUrl, PictureInfo]

# 设置图片绝对路径FullPath所指向的图片为壁纸
def SetWallpaper(FullPath):
    return ctypes.windll.user32.SystemParametersInfoW(20, 0, r''+FullPath, 0)

# 通过爬虫获取图片URL和信息, 下载图片到指定位置, 设置墙纸
def main():
    print ("BingDesktop v1.01\n  by andy1990zx")

    LocalFolderPath = r"E:\Picture\Bing"       # 图片要被保存在的位置
    Picture = GetPictureUrlAndInfo()     # 获取图片URL和信息, 返回值为list
    print ("图片URL如下: \n   ", Picture[0])
    print ("图片信息如下: \n   ", Picture[1])
    print ("图片下载中...")
    FullPath = DownloadPictureToLocal(Picture, LocalFolderPath)
    print ("图片下载成功, 本地路径如下: \n   ", FullPath)
    Temp = SetWallpaper(FullPath)
    print("成功设置墙纸, 返回值为: ", Temp)
    time.sleep(10)

main()
