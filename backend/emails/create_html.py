from fastapi import Depends, APIRouter
from datetime import datetime

from crud import get_all_users, get_all_prs
from dependencies import get_mongo_db
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



router = APIRouter(prefix="/email", tags=["email"])

@router.put("/rewwrite_user_list")
async def create_user_list(db = Depends(get_mongo_db)):
    users = get_all_users(db)
    f = open('./emails/email_list.txt', 'w')
    for user in users:
        f.write(user)
        f.write('\n')

    f.close()

    
    '''  
    f = open('email_list.txt', 'r')
    for user in f.readlines():
        print(user, end="")
    f.close()
    '''
@router.put("/rewrite_html")
async def create_html(db = Depends(get_mongo_db)):
    # first get info 
    pr_lst = get_all_prs(db)


    # then redo the html file 
    print(pr_lst[0])
    html = open('./emails/template.html').read()
    html = html.replace('{{ content1 }}', pr_lst[0]["description"])
    html = html.replace('{{ content2 }}', pr_lst[1]["description"])
    html = html.replace('{{ content3 }}', pr_lst[2]["description"])
    html = html.replace('{{ content4 }}', pr_lst[3]["description"])

    dates = [pr_lst[i]["created_at"] for i in range(4)]
    titles = [pr_lst[i]["url"] for i in range(4)]

    parsed_titles = [title.split("/")[-3] for title in titles]
    parsed_dates = []
    for date in dates:
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        parsed_date = datetime.strptime(date, date_format)   
        formatted_date = parsed_date.strftime("%B %d, %Y")
        parsed_dates.append(formatted_date)

    print(parsed_titles)
    print(parsed_dates)
    html = html.replace('{{ date1 }}', parsed_dates[0])
    html = html.replace('{{ date2 }}', parsed_dates[1])
    html = html.replace('{{ date3 }}', parsed_dates[2])
    html = html.replace('{{ date4 }}', parsed_dates[3])

    html = html.replace('{{ title1 }}', parsed_titles[0].capitalize())
    html = html.replace('{{ title2 }}', parsed_titles[1].capitalize())
    html = html.replace('{{ title3 }}', parsed_titles[2].capitalize())
    html = html.replace('{{ title4 }}', parsed_titles[3].capitalize())

    send_html = open('./emails/send_template.html', 'w')
    send_html.write(html)
    send_html.close()

@router.post("/send_emails")
async def send_emails(db = Depends(get_mongo_db)):
    s = smtplib.SMTP('email-smtp.us-west-1.amazonaws.com')

    s.connect('email-smtp.us-west-1.amazonaws.com', 25)

    s.starttls()

    s.login('AKIAVCQ2ZWYV2OGEJJXK', 'BLvC6IjhAX1ujyoGF67KY/2ZBpWwMcp1n6/Y87Ku3eqU')

    email_list = open("./emails/email_list.txt", 'r').readlines()
    html = open("./emails/send_template.html").read()
    
    for user in email_list:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Weekly Updates"
        msg['From'] = "derrickteshiba@g.ucla.edu"
        msg['To'] = user

        send_html = MIMEText(html.replace('{{ user }}', user), 'html')
        msg.attach(send_html)
        s.sendmail("derrickteshiba@g.ucla.edu", user, msg.as_string())
        print("Sent to " + user, end="")