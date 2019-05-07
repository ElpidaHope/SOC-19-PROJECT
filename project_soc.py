# importing all the needed libraries

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
import datetime
import os

# creating today's date
date = datetime.datetime.now()
date_ = date.strftime('%A,%d %B,%Y')
num = int(input("Enter number of items sold today, {}:".format(date_)))

count = 0
total_unit = 0
price_unit = 0

new_item = []
new_price = []
new_unit = []

# creating a while loop to allow user enter the items multiple times
while count < num:
    item_ = input("Enter the item:")
    unit = int(input('Enter unit of item sold:'))
    price = int(input('Enter the price of item:'))
    print('-'*30)             # this is to indicate the different input of the user
    count += 1
    price_unit_ = unit * price
    price_unit += price_unit_
    new_item.append(item_)
    new_price.append(price)
    new_unit.append(unit)


# using pandas to convert the details entered by the user to a csv file
data = pd.DataFrame({'Items': new_item, 'Unit': new_unit, 'Price(#)': new_price})
data.to_csv(os.getcwd() + '/Customer.csv', index=False)


# sending the details to the customer's mail using smtplib
customer_name = input('Enter the name of seller').upper()
msg_subject = 'SALES INVENTORY OF {}'.format(customer_name)
msg_body = 'The total price of items sold today, {} is #{}'.format(date_, price_unit) + \
           '\nThe items sold today and their prices are shown in the file attached below '
recipient = input("Enter customer's mail")
your_mail = input('Enter your mail')
your_password = input('Enter your password')


msg = MIMEMultipart()
msg['To'] = recipient
msg['From'] = your_mail
msg['Subject'] = msg_subject
msg['Body'] = msg_body
body = msg_body
msg.attach(MIMEText(body, 'plain'))


# attaching the csv file to the mail to be sent
filename = 'Customer.csv'
filepath = "/home/jesufemi/PycharmProjects/SOC'19 Project/" + filename
path = open(filepath, 'rb')
part = MIMEBase('application', 'octet stream')
part.set_payload(path.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
msg.attach(part)
text = msg.as_string()


server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(your_mail, your_password)
server.sendmail(your_mail, recipient, text)
server.quit()
print('Email sent successfully')
