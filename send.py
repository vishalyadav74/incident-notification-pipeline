import smtplib
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, body_html, to_list, cc_list=None):
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    smtp_user = 'incident@businessnext.com'
    smtp_password = 'btxnzsrnjgjfjpqf'  # ⚠️ PROD: move to Jenkins credentials

    msg = MIMEMultipart('alternative')
    msg['From'] = smtp_user
    msg['To'] = ', '.join(to_list)
    if cc_list:
        msg['Cc'] = ', '.join(cc_list)

    msg['Subject'] = subject
    msg.attach(MIMEText(body_html, 'html'))

    recipients = to_list + (cc_list or [])

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(smtp_user, recipients, msg.as_string())
    server.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--subject', required=True)
    parser.add_argument('--to', required=True)
    parser.add_argument('--cc', default='')
    parser.add_argument('--body', required=True)

    args = parser.parse_args()

    to_list = [x.strip() for x in args.to.split(',') if x.strip()]
    cc_list = [x.strip() for x in args.cc.split(',') if x.strip()]

    with open(args.body, 'r') as f:
        body_html = f.read()

    send_email(
        subject=args.subject,
        body_html=body_html,
        to_list=to_list,
        cc_list=cc_list
    )
