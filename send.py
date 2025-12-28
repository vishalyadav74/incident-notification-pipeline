import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body_html, to_list, cc_list=None):
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    smtp_user = "incident@businessnext.com"
    smtp_password = "password"  # 🔴 Jenkins env variable better

    if isinstance(to_list, str):
        to_list = [x.strip() for x in to_list.split(",") if x.strip()]
    if cc_list:
        cc_list = [x.strip() for x in cc_list.split(",") if x.strip()]
    else:
        cc_list = []

    recipients = to_list + cc_list

    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = ", ".join(to_list)
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)

    msg["Subject"] = subject
    msg.attach(MIMEText(body_html, "html"))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(smtp_user, recipients, msg.as_string())
    server.quit()

    print("✅ Email sent successfully")


if __name__ == "__main__":
    subject = sys.argv[1]
    body = sys.argv[2]
    to_addr = sys.argv[3]
    cc_addr = sys.argv[4] if len(sys.argv) > 4 else ""

    send_email(subject, body, to_addr, cc_addr)
