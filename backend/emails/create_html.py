from fastapi import Depends, APIRouter


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
    html = open('./emails/template.html').read()
    html = html.replace('{{ content1 }}', pr_lst[0])
    html = html.replace('{{ content2 }}', pr_lst[1])
    html = html.replace('{{ content3 }}', pr_lst[2])
    html = html.replace('{{ content4 }}', pr_lst[3])

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