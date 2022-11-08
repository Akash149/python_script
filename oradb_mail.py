
import email
import logging as log
import os
import traceback
import sys
import smtplib
import cx_Oracle
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
html = """"""
log.info("====================== LOG ======================")

try:
    # Oracle db connection with username/password@hostaddress:PortNumber/SID
    conn = cx_Oracle.connect('system/password@localhost:1521/xe')
    cursor = conn.cursor()
    log.info(f"Database version is {conn.version}")
    cursor.execute("select * from employee")
    result = cursor.fetchall()
    log.info(result)
    for i in result:
        r_count += 1
    log.info("Total count is %d"%r_count)
    log.info("Success")

    try:
        def send_mail():

            # Sender email and password.
            u_mail = "yourmail@gmail.com"
            u_pass = "password"

            # Receiver email.
            to = ["araushan11@gmail.com"]
            text = ""
            # Formated string of html
            html = f'''\
                    <html>
                        </style>
                        <body>
                            <div>
                            <table style="text-align:center" "width:50%" cellspacing="0" cellpadding="0" align="center" border="1" width="750">
                                <thead>
                                <tr><th>File status</th><th>Count of Employee</th>
                                </thead>
                                <tbody>
                                
                                <tr><td>Success</td><td>{r_count}</td></tr>
                                <tr><td>Success</td><td>{r_count}</td></tr>
                                </tbody>
                            </table>
                            </div>  
                        </body>
                    </html>
                        '''
            message = MIMEMultipart("alternative", None, [
                                    MIMEText(text), MIMEText(html, 'html')])
            message["Subject"] = "" .join(
                "Transaction of %s" % str(current_date))
            message["From"] = "" .join(u_mail)
            message["To"] = "," .join(to)
            log.info(type(message))

            # smtp server adderess or port number.
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.ehlo()
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

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
        log.info("Database Connection close.")
