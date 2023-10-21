#!/bin/python
#Coding="utf-8"
from lxml import etree
import sys
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate



def getResult(DATE,SITE):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }
    res = requests.get(SITE, headers=headers)
    flag = False
    available = []
    tree = etree.HTML(res.text)
    items = tree.xpath('//div[@class="bookingList"]/ul/li')
    for item in items:
        date = item.xpath('./h1/text()')[0].split(" ")
        m_d = date[0].split("2023-")[1]
        if m_d == DATE:
            flag = True
            if item.xpath('./a/text()')[0] == "可预约":
                available.append(DATE + date[2])
    return flag,available


# 发送邮件
# def sendEmail(content):
#     message = MIMEText(content, 'plain', 'utf-8')
#     message['From'] = "GitHub Actions<" + sender + ">"
#     message['To'] = "<" + receiver + ">"
#
#     subject = "CSDN Report"
#     message['Subject'] = Header(subject, 'utf-8')
#
#     try:
#         smtpObj = smtplib.SMTP_SSL(mail_host, mail_port)
#         smtpObj.login(mail_user, mail_password)
#         smtpObj.sendmail(sender, receiver, message.as_string())
#         print("邮件发送成功")
#
#     except smtplib.SMTPException:
#         print("Error: 无法发送邮件")


# 保存email内容
def saveEmail(email_path, message):
    with open(email_path, 'w', encoding="utf-8") as email:
        email.writelines(message)




if __name__ == "__main__":

    DATE = sys.argv[1]
    SITE = sys.argv[2]
    flag,available = getResult(DATE,SITE)
    temp = ''
    if flag:
        if len(available) > 0:
            for avail in available:
                temp += avail
            message = temp+"可预约"
        else:
            message = "即将可预约"
        email_path = "email.txt"
        saveEmail(email_path, message)


    client = WeChatClient(app_id, app_secret)
    wm = WeChatMessage(client)
    wm.send_template(,, )