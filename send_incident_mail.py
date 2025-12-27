import argparse
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "YOUR_GMAIL_ID@gmail.com"   # 👈 apna gmail id

def send_mail(args, smtp_password):
    if not args.to.strip():
        raise ValueError("MAIL_TO cannot be empty")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_dir, "incident_mail.html")

    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())

    html = template.render(
        title=args.title,
        start_time=args.start_time,
        end_time=args.end_time,
        case_id=args.case_id,
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
    msg["From"] = SMTP_USER
    msg["To"] = args.to
    msg["Cc"] = args.cc
    msg["Subject"] = f"P{args.priority} Incident | {args.title}"
    msg.attach(MIMEText(html, "html"))

    recipients = []
    recipients.extend([r.strip() for r in args.to.split(",") if r.strip()])
    if args.cc:
        recipients.extend([r.strip() for r in args.cc.split(",") if r.strip()])

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.ehlo()
    server.starttls()
    server.ehlo()
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
    parser.add_argument("--case_id")
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
    send_mail(args, os.environ["SMTP_PASSWORD"])
