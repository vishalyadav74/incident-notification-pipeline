📢 Incident Notification Automation (Jenkins + Python)

This project automates incident notification emails using Jenkins Pipeline, HTML email templates, and Python SMTP.
It is designed for ITSM / Ops teams to send P1 / P2 / P3 incident alerts with dynamic content, status-based behavior, and a professional email layout.

🚀 Features

🔁 Fully automated via Jenkins

📧 HTML email notifications

🔴 OPEN incidents

Red OPEN status badge

JOIN BRIDGE CALL button

🟢 RESOLVED incidents

Green RESOLVED status badge

Message: “Check case for complete detail.”

🧠 Dynamic intro message (changes for OPEN vs RESOLVED)

📱 Mobile & Outlook friendly layout

🏷️ CID embedded BusinessNext logo

🔐 Secure email sending via Python SMTP (Office365)

🧩 Clean separation of:

Jenkins logic

HTML template

Email sending logic

📂 Project Structure
incident-notification-pipeline/
│
├── Jenkinsfile
├── incident_mail.html
├── send.py
├── requirements.txt
├── logo-fixed.png
└── README.md

🧰 Tech Stack

Jenkins (Declarative Pipeline)

Python 3

SMTP (Office365)

HTML (Email-safe tables & inline styles)

⚙️ Jenkins Parameters
Parameter	Description
MAIL_TO	Primary recipients
MAIL_CC	CC recipients
TITLE	Incident title
START_TIME	Incident start time
END_TIME	Incident end time
CASE_ID	Case number
DESCRIPTION	Incident description
PRIORITY	P1 / P2 / P3
SEVERITY	Critical / High / Medium / Low
STATUS	In Analysis / Identified / Monitoring / Resolved
REPORTED_BY	Reporting team
TEAMS	Teams involved
LATEST_UPDATE	Latest update
RCA	Root cause analysis
RESOLUTION	Resolution
BRIDGE_CALL_URL	Bridge call link (only for OPEN)
📄 Email Behavior Logic
🔴 When STATUS ≠ Resolved

Status badge: OPEN (Red)

Shows JOIN BRIDGE CALL button

Subject:

INCIDENT | P1 | MY PROD | Unable to login

🟢 When STATUS = Resolved

Status badge: RESOLVED (Green)

Bridge button hidden

Shows text:

Check case for complete detail.


Subject:

RESOLVED | P1 | MY PROD | Unable to login

🖼️ Logo Handling

Logo is embedded using CID (cid:businessnext_logo)

Works reliably across:

Outlook

Mobile mail apps

Webmail

No external image dependency

🐍 Python Email Sender (send.py)

Uses smtplib

Office365 SMTP

Sends:

HTML email body

To + CC recipients

Reads final rendered HTML (final_mail.html)

Credentials should be stored securely (Jenkins credentials recommended)

🧪 Tested On

✅ Outlook Desktop

✅ Outlook Web

✅ Mobile (Android / iOS)

✅ Jenkins Docker setup
