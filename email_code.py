import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class AWSSender:
    s = smtplib.SMTP('email-smtp.us-west-1.amazonaws.com')

    s.connect('email-smtp.us-west-1.amazonaws.com', 25)

    s.starttls()

    s.login('AKIAVCQ2ZWYV2OGEJJXK', 'BLvC6IjhAX1ujyoGF67KY/2ZBpWwMcp1n6/Y87Ku3eqU')

    #msg = 'From: derrickteshiba@g.ucla.edu\nTo: derrickteshiba@g.ucla.edu\nSubject: Test email\n\nThis is a test email sent using Python'

    #s.sendmail('derrickteshiba@g.ucla.edu', 'derrickteshiba@g.ucla.edu', msg)

    def quit(self):
        self.s.quit()
    
    def load_plain_text(self, text):
        self.text_plain = text

    def assign_html(self, html_path): # pass in html path
        self.html_path = html_path

    def generate_body(self):
        self.html = open(self.html_path, 'r').read()
        self.html = self.html.replace('{{ content }}', self.text_plain)

    def send(self, subject, sender, reciever):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = reciever

        plain = MIMEText(self.text_plain, 'plain')
        html = MIMEText(self.html, 'html')

        msg.attach(plain)
        msg.attach(html)

        self.s.sendmail(sender, reciever, msg.as_string())
        print("Sent to " + reciever, end="")
    

email_list = open('email_list.txt', 'r').readlines()
subject = "Weekly Updates"
aws = AWSSender()
aws.load_plain_text("My shit works .") # Replace the content in the html with the text we want
aws.assign_html('template.html') # html file
aws.generate_body()

for email in email_list:
    aws.send(subject, "derrickteshiba@g.ucla.edu", email)