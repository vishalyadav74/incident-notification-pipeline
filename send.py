import smtplib
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os


def send_email(subject, body_html, to_list, cc_list=None):
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    smtp_user = 'incident@businessnext.com'
    smtp_password = 'btxnzsrnjgjfjpqf'   # 🔴 PROD me Jenkins credential use karna

    msg = MIMEMultipart('related')
    msg['From'] = smtp_user
    msg['To'] = ', '.join(to_list)
    if cc_list:
        msg['Cc'] = ', '.join(cc_list)
    msg['Subject'] = subject

    # ---------- HTML BODY ----------
    alt_part = MIMEMultipart('alternative')
    alt_part.attach(MIMEText(body_html, 'html'))
    msg.attach(alt_part)

    # ---------- LOGO (CID ATTACHMENT) ----------
    logo_path = 'logo-fixed.png'
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as f:
            logo = MIMEImage(f.read())
            logo.add_header('Content-ID', '<businessnext_logo>')
            logo.add_header('Content-Disposition', 'inline', filename='logo-fixed.png')
            msg.attach(logo)
    else:
        print("⚠️ logo-fixed.png not found, skipping logo")

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
    parser.add_argument('--body', default='incident_mail.html')

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
