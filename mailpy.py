# **********************************************
# *                                            *
# *                Author                      *
# *             Akash Kumar                    *
# *                                            *
# *                                            *
# **********************************************
import email
import logging as log
import os
import traceback
import sys
import smtplib
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from tabulate import tabulate
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

current_date = datetime.strftime(datetime.today(), '%y-%m-%d')
log.basicConfig(filename=str(current_date)+".log",
                format="%(asctime)s %(message)s", filemode='a')
logger = log.getLogger()
logger.setLevel(log.INFO)

r_count = 0
cnames = []
data = [["Sun",696000,1989100000],["Earth",6371,5973.6],["Moon",1737,73.5],["Mars",3390,641.85]]
html = """"""
log.info("====================== LOG ======================")

try:
    conn = mysql.connector.connect(
        host="localhost", user='root', password='root', database='techblog')
    if conn.is_connected():
        db_info = conn.get_server_info()
        log.info("DB Server version %s" % str(db_info))
        cursor = conn.cursor()
        cursor.execute("select database();")
        dbname = cursor.fetchone()
        log.info("you are connected with %s" % str(dbname))
        cursor.execute("select count(*) from user")
        result = cursor.fetchall()
        for i in result:
            for x in i:
                data_count = x
                log.info("Total row Count is %s" % str(data_count))

        cursor.execute(
            "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'techblog' and TABLE_NAME = 'user';")
        result = cursor.fetchall()
        for cols in result:
            for cname in cols:
                cnames.append(cname)
                log.info(cname)
        # log.info(str(result))
        log.info(str(cnames))
        log.info("Success")

        try:
            def send_mail():
                u_mail = "yourmail@gmail.com"
                u_pass = "Password"
                to = ["araushan11@gmail.com"]

                text = """
Hello,
Here is your data

{table}
Regards,
Akash kumar         
                """
                html = f'''\
                    <html>
                        </style>
                        <body>
                            <p>DB Name is </p><h2>{str(dbname)}</h2>
                            <p style="color:red; background:white">Total number of count is  </p><h2>{str(data_count)}</h2>
                            <div>
                            <table style="text-align:center" "width:50%" cellspacing="0" cellpadding="0" align="center" border="1" width="750">
                                <thead>
                                <tr><th>File status</th><th>Data Count</th>
                                </thead>
                                <tbody>
                                
                                <tr><td>Success</td><td>6371</td></tr>
                                <tr><td>Success</td><td>637</td></tr>
                                </tbody>
                            </table>
                            </div>  
                        </body>
                    </html>
                        '''# % (str(dbname), str(data_count))
#                 html = """
# <html><body><p>Hello, Friend.</p>
# <p>Here is your data:</p>
# {table}
# <p>Regards,</p>
# <p>Me</p>
# </body></html>
# """
                text = text.format(table=tabulate(data,headers="firstrow", tablefmt="grid"))
                # html = html.format(table=tabulate(data,headers="firstrow", tablefmt="html"))
                log.info(text)
                message = MIMEMultipart("alternative", None, [MIMEText(text), MIMEText(html, 'html')])
                message["Subject"] = "" .join("Transaction of %s" % str(current_date))
                message["From"] = "" .join(u_mail)
                message["To"] = "," .join(to)
                log.info(type(message))
                smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                smtp_server.ehlo()
                # smtp_server.starttls()
                # smtp_server.ehlo()
                smtp_server.login(u_mail, u_pass)
                smtp_server.sendmail(u_mail, to, message.as_string())
                smtp_server.quit()
                log.info(message.as_string())
                log.info("Successfully sent on %s" % to)

            send_mail()
        except Exception as mailerr:
            log.error(mailerr)
            traceback.print_exc()

except Exception as err:
    logger.setLevel(log.ERROR)
    log.error(err)
    print(err)
    traceback.print_exc()

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        log.info("Database Connection close.")
