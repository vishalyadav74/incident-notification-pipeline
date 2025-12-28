import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, body_html, to_list, cc_list=None):
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    smtp_user = 'incident@businessnext.com'
    smtp_password = 'password'   # 🔴 better: env variable use karo

    from_email = smtp_user

    # --------- Normalize recipients ----------
    if isinstance(to_list, str):
        to_list = [x.strip() for x in to_list.split(',') if x.strip()]

    if cc_list:
        if isinstance(cc_list, str):
            cc_list = [x.strip() for x in cc_list.split(',') if x.strip()]
    else:
        cc_list = []

    all_recipients = to_list + cc_list

    # --------- Build Email ----------
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ', '.join(to_list)
    if cc_list:
        msg['Cc'] = ', '.join(cc_list)

    msg['Subject'] = subject
    msg.attach(MIMEText(body_html, 'html'))

    # --------- Send Email ----------
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, all_recipients, msg.as_string())
        server.quit()
        print("✅ Email sent successfully")

    except Exception as e:
        print("❌ Failed to send email")
        raise e
