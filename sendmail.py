#!/usr/bin/python
#coding:utf-8
import smtplib
from email.mime.text import MIMEText
import sys
# configure your own parameters here
#下面邮件地址的smtp地址
mail_host = 'smtp.sohu.com'
#用来发邮件的邮箱,在发件人抬头显示(不然你的邮件会被当成是垃圾邮件)
mail_user = '15669981162@sohu.com'
#上面邮箱的密码
mail_pass = 'Wahy@8fk'
#上面smtp地址的主网站地址
mail_postfix = 'mail.sohu.com'
def send_mail(to_list,subject,content):
    me = mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content, 'plain', 'utf-8')
    # 必须使用'utf-8'参数，否则默认为us-ascii, 在部分邮件客户端中文会显示为乱码
    msg['Subject'] = subject
    msg['From'] = me
    msg['to'] = to_list
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me,to_list,msg.as_string())
        s.close()
        return True
    except Exception,e:
        print str(e)
        return False

send_mail(sys.argv[1], sys.argv[2], sys.argv[3])