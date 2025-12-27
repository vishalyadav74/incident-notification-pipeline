import argparse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template

SMTP_SERVER = 'smtp.office365.com'
SMTP_PORT = 587
SMTP_USER = 'incident@businessnext.com'

def send_mail(args, smtp_password):
    with open("templates/incident_mail.html") as f:
        template = Template(f.read())

    html = template.render(
        title=args.title,
        start_time=args.start_time,
        end_time=args.end_time,
        azure_id=args.azure_id,
        description=args.description,
        priority=args.priority,
        severity=args.severity,
        status=args.status,
        reported_by=args.reported_by,
        teams=args.teams,
        latest_update=args.latest_update,
        rca=args.rca,
        resolution=args.resolution
    )

    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = args.to
    msg['Cc'] = args.cc
    msg['Subject'] = f"P{args.priority} Incident | {args.title}"

    msg.attach(MIMEText(html, 'html'))

    recipients = args.to.split(',') + args.cc.split(',')

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, smtp_password)
    server.sendmail(SMTP_USER, recipients, msg.as_string())
    server.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--to", required=True)
    parser.add_argument("--cc", default="")
    parser.add_argument("--title")
    parser.add_argument("--start_time")
    parser.add_argument("--end_time")
    parser.add_argument("--azure_id")
    parser.add_argument("--description")
    parser.add_argument("--priority")
    parser.add_argument("--severity")
    parser.add_argument("--status")
    parser.add_argument("--reported_by")
    parser.add_argument("--teams")
    parser.add_argument("--latest_update")
    parser.add_argument("--rca")
    parser.add_argument("--resolution")

    args = parser.parse_args()
    import os
    send_mail(args, os.environ["SMTP_PASSWORD"])
