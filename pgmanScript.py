import logging as log
import os
import smtplib
import sys
import traceback
import mysql.connector
from mysql.connector import Error
from dateutil import relativedelta
from datetime import datetime
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

current_date = datetime.strftime(datetime.today(), '%d-%m-%y')
log.basicConfig(filename="PGMAN" + str(current_date)+".log",
                format="%(asctime)s %(message)s", filemode='a')
logger = log.getLogger()
logger.setLevel(log.INFO)

u_mail = "mr.iotdeveloper@gmail.com"
u_pass = ""

to_mail = ""
text = ""
subject = " Reminder to Pay Rent for the Current Month"

conn = mysql.connector.connect(host="localhost", user="root", password="root",
                               database='pgmans', auth_plugin='mysql_native_password')

date = str(datetime.today()).split(' ')
todayDate = datetime.strptime(date[0], "%Y-%m-%d")
today = str(date[0]).split('-')
dt_object = datetime.strptime(str(today[1]), '%m')
month_name = dt_object.strftime("%B")
year = str(today[0])

# Method for send the email of rent alert
def send_mail(email, subject):
    message = MIMEMultipart("alternative", None, [
                            MIMEText(text), MIMEText(html, 'html')])
    message["Subject"] = "" .join(subject)
    message["From"] = "" .join(u_mail)
    message["To"] = "" .join(email)

    # smtp server adderess or port number.
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.ehlo()
    smtp_server.login(u_mail, u_pass)
    smtp_server.sendmail(u_mail, email, message.as_string())
    smtp_server.quit()
    log.info(message.as_string())
    log.info("Successfully sent on %s" % email)


try:
    if conn.is_connected():
        db_info = conn.get_server_info()
        log.info("DB Server version %s" % str(db_info))
        cursor = conn.cursor()
        cursor.execute("select database();")
        dbname = cursor.fetchone()
        log.info("Selected database is %s" % str(dbname))
        cursor.execute("select * from guest")
        result = cursor.fetchall()
        shiftDate = datetime.strptime("2023-04-13", "%Y-%m-%d")
        log.info("Today's date is %s" % str(todayDate))
        

        for i in result:
            # log.info(str(i))
            to_mail = i[3]
            name = i[6]
            log.info("email: " + to_mail)
            log.info("name: " + name)
            guest_dashboard = "localhost:8082/guest/dashboard"
            shiftDate = str(i[23]).split(' ')
            shiftDay = shiftDate[0].split('-')

            # log.info(i)
            log.info(str(shiftDate))
            # log.info(str(shiftDay[1]))
            log.info(str(today[2]))
            shiftedDate = datetime.strptime(str(shiftDate[0]), "%Y-%m-%d")
            log.info("Shifted date is " + str(shiftedDate))
            if (int(shiftDay[2]) == int(today[2])):
                query = "update guest set paymentstatus=b'0',paidamount=0,remainingamount=" + \
                    str(i[21]+i[22]) + " where id='"+str(i[0])+"';"
                log.info(query)
                x = cursor.execute(query)
                conn.commit()

                # Get pg details of guests
                getpg_query = "select * from pgdetails where id=" + i[16] + ";"
                cursor.execute(getpg_query)
                pg = cursor.fetchone()
                pgname = pg[1]
                log.info(str(pg))

                # Create a message to send an alert email
                html = f'''\
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" 
                        integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
                        <style>
                        </style>
                    </head>
                    <body>
                        <div class="container">
                        <h5 style="font-size: medium;">Dear {name},</h5>
                        <p> We are writing to remind you about the payment of your rent for the <span style="font-weight: 600;">{month_name} {year}</span>. 
                            As our valued tenant, it is essential to keep your rental account up to date.</p>
                        <p>Please note that the rent for <span style="font-weight: 600;">{pgname}</span> is due on <span style="font-weight: 600;">{date[0]}</span>. 
                            We kindly request that you settle the outstanding balance as soon as possible to avoid any inconvenience or late fees. 
                            Timely payment helps us maintain the property and provide the best possible living experience for all our residents.</p>
                            <p>To facilitate the payment process, we offer several convenient options:</p>
                            <ul>
                                <li>Online Payment: You can make a secure online payment by visiting our website <a href="{guest_dashboard}">{guest_dashboard}</a>. 
                                    Follow the instructions on the payment portal to complete the transaction.</li>
                                <li>Cash Payment: If you prefer to pay your owner, please visit the office during business hours.</li>
                            </ul>
                            <p>If you have any questions or concerns regarding your rent or any other aspect of your tenancy, please do not hesitate to contact us. 
                                We are here to assist you.</p>
                            <p>Thank you for your understanding and prompt attention to this matter.</p>
                            <h5>Note: Do not reply of this mail, this is system generated mail</h5>
                            <h5>Sincerely,</h5>
                            <h5 style="font-size: medium;">PGMAN Assistant</h5>
                            <h5 style="font-size: medium;">8709394895</h5>
                        </div> 
                    </body>
                    </html>
                '''
                log.info("Payment satus has been changed")
                log.info(html)
                send_mail(to_mail,subject)
                log.info("Reminder mail sent to " + name)

except Exception as exception:
    traceback.print_exc()
    logger.setLevel(log.ERROR)
    log.error(exception)

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        log.info("Database connection closed")
