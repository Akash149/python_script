# **********************************************
# *                                            *
# *                                            *
# *                                            *
# *                                            *
# *                                            *
# **********************************************
import email
import logging as log
import os
import sys
import smtplib, ssl
import mysql.connector
from  mysql.connector import Error
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

current_date = datetime.strftime(datetime.today(), '%y-%m-%d')
log.basicConfig(filename=str(current_date)+".log",format="%(asctime)s %(message)s",filemode='a')
logger = log.getLogger()
logger.setLevel(log.INFO)

r_count = 0


log.info("====================== LOG ======================")

try:
    conn = mysql.connector.connect(host="localhost", user='root', password='root', database='techblog')
    if conn.is_connected():
        db_info = conn.get_server_info()
        log.info(db_info)
        cursor = conn.cursor()
        cursor.execute("select database();")
        dbname = cursor.fetchone()
        log.info("you are connected with %s"%str(dbname))
        cursor.execute("select count(*) from user")
        result = cursor.fetchall()
        for i in result: 
            r_count = i 
            log.info("Total row Count is %s"%str(r_count))
        #send_mail()
        log.info("Success")
    
        try:
            u_mail = 'mr.iotdeveloper@gmail.com'
            u_pass = 'xwpjqzsdwxvwhnkt'
            to = 'araushan11@gmail.com'
            context = ssl.create_default_context()
            subject = "Test for mail"
            body = ''
            data_count = r_count
            message = MIMEMultipart("alternative")
            message["Subject"] = "Transaction of %s"%current_date
            message["From"] = u_mail
            message["To"] = to
            
            html = """
                <html>
                    <body>
                        <p>DB Name is </p><h2>%s</h2>
                        <p>Total number of count is  </p><h2>%s</h2>
                    </body>
                </html>
                    """%(str(dbname),str(data_count))
            log.info(html)
            message.attach(MIMEText(html,"html"))
            def send_mail():
                smtp_server = smtplib.SMTP_SSL('smtp.gmail.com',465)
                smtp_server.ehlo()
                # smtp_server.starttls(context=context)
                # smtp_server.ehlo()
                smtp_server.login(u_mail,u_pass)
                smtp_server.sendmail(u_mail,to,message)
                log.info(message)
                log.info("Successfully sent on %s"%str(to))
        
        except Exception as mailerr:
            log.ERROR(mailerr)
            
    send_mail()
                       
except Exception as err:
    logger.setLevel(log.ERROR)
    log.error(err)
    print(err)
    
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        log.info("Database Connection close.")