#!/bin/python
#Coding="utf-8"
from lxml import etree
import sys
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
from datetime import datetime
import pytz
import re

def getResult(DATE,SITE):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }
    res = requests.get(SITE, headers=headers)
    flag = False
    bookable = []
    full = []
    tree = etree.HTML(res.text)
    items = tree.xpath('//div[@class="bookingList"]/ul/li')
    doctor_name = tree.xpath('//div[@class="docBox"]/div[@class="docNav"]/span/i/text()')[0]
    for item in items:
        date = item.xpath('./h1/text()')[0].split(" ")
        m_d = date[0].split("2023-")[1]
        if m_d in DATE:
            flag = True
            time = [m_d + date[1] + date[2]]
            if item.xpath('./a/text()')[0] == "可预约":
                bookable.append(time)
            else:
                full.append(time)
    return flag,bookable,full,doctor_name


# 保存email内容
def saveEmail(email_path, message):

    with open(email_path, 'w', encoding="utf-8") as email:
        email.writelines(message)

def sendWx(bookable_list,full_list,BOOK_DATE,doctor_name):
    app_id = os.environ["APP_ID"]
    app_secret = os.environ["APP_SECRET"]
    user_ids = os.environ["USER_ID"].split(',')
    template_ids = os.environ["TEMPLATE_ID"]
    client = WeChatClient(app_id, app_secret)
    wm = WeChatMessage(client)
    china_tz = pytz.timezone('Asia/Shanghai')
    now = datetime.now(china_tz)
    now_formatted = now.strftime('%Y-%m-%d %H:%M')
    data = {
        "now_formatted": {"value":now_formatted},
        "doctor_name": {"value":doctor_name},
        "bookable_list":{"value":bookable_list},
        "full_list":{"value":full_list},
        "BOOK_DATE": {"value":BOOK_DATE},
    }

    for i in range(len(user_ids)):
        wm.send_template(user_ids[i], template_ids, data)


if __name__ == "__main__":
    FORMATED_MESSAGE = """
    当前可预约:{0}
    已约满:{1}
    """
    BOOK_DATE = os.environ["BOOK_DATE"]
    SITE = os.environ["SITE"]


    flag,bookable,full,doctor_name = getResult(BOOK_DATE,SITE)
    bookable_list = []
    full_list = []
    if flag: # 出号了
        if len(bookable) > 0:
            for b in bookable:
                bookable_list += b
        if len(full) > 0:
            for f in full:
                full_list += f

        if len(bookable) == 0 and len(full) > 0:

            match = re.findall(r'(?<=-)\d{2}-\d{2}(?=[^\d])',full[-1])[0]
            if match == BOOK_DATE[-1]:
                full_list = "全部约满了 请重新定一个日期"

        sendWx(bookable_list,full_list, BOOK_DATE, doctor_name) # 出号了才向微信推消息。
        email_message = FORMATED_MESSAGE.format(bookable_list,full_list)
    else:
        email_message = "全都未出号"
    email_path = "email.txt"
    saveEmail(email_path,email_message)
    
