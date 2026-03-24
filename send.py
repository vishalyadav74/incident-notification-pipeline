#!/usr/bin/env python3
"""
send.py — Incident Notification Email Dispatcher
BusinessNext | ITSM Automation
"""

import smtplib
import argparse
import logging
import sys
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# ──────────────────────────────────────────────
# SMTP Configuration
# ──────────────────────────────────────────────
SMTP_SERVER   = 'smtp.office365.com'
SMTP_PORT     = 587
SMTP_USER     = 'incident@businessnext.com'
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', 'btxnzsrnjgjfjpqf')   # prefer env var

LOGO_PATH     = 'logo-fixed.png'
LOGO_CID      = 'businessnext_logo'

# ──────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s  [%(levelname)s]  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger(__name__)


def parse_recipients(raw: str) -> list[str]:
    """Split a comma-separated address string, drop blanks."""
    return [addr.strip() for addr in raw.split(',') if addr.strip()]


def attach_logo(msg: MIMEMultipart) -> None:
    """Attach the company logo as an inline CID image."""
    if not os.path.isfile(LOGO_PATH):
        log.warning("Logo file not found at '%s' — skipping attachment.", LOGO_PATH)
        return
    with open(LOGO_PATH, 'rb') as fh:
        img = MIMEImage(fh.read())
    img.add_header('Content-ID', f'<{LOGO_CID}>')
    img.add_header('Content-Disposition', 'inline', filename='logo.png')
    msg.attach(img)


def send_email(
    subject: str,
    body_html: str,
    to_list: list[str],
    cc_list: list[str]
) -> None:
    """Build and dispatch the HTML incident email."""

    if not to_list:
        raise ValueError("Recipient list (--to) cannot be empty.")

    # ── Build message ──────────────────────────
    msg = MIMEMultipart('related')
    msg['From']    = SMTP_USER
    msg['To']      = ', '.join(to_list)
    msg['Cc']      = ', '.join(cc_list)
    msg['Subject'] = subject

    # Wrap HTML in 'alternative' part for better client compatibility
    alternative = MIMEMultipart('alternative')
    alternative.attach(MIMEText(body_html, 'html', 'utf-8'))
    msg.attach(alternative)

    attach_logo(msg)

    recipients = to_list + cc_list

    # ── Send via SMTP ──────────────────────────
    log.info("Connecting to %s:%s ...", SMTP_SERVER, SMTP_PORT)
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, recipients, msg.as_string())
        log.info("Email sent to: %s", ', '.join(recipients))


# ──────────────────────────────────────────────
# CLI Entry Point
# ──────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        description='Dispatch a BusinessNext incident notification email.'
    )
    parser.add_argument('--subject', required=True,  help='Email subject line')
    parser.add_argument('--to',      required=True,  help='Comma-separated To addresses')
    parser.add_argument('--cc',      default='',     help='Comma-separated CC addresses')
    parser.add_argument('--body',    required=True,  help='Path to the HTML body file')
    args = parser.parse_args()

    if not os.path.isfile(args.body):
        log.error("HTML body file not found: %s", args.body)
        sys.exit(1)

    with open(args.body, encoding='utf-8') as fh:
        body_html = fh.read()

    try:
        send_email(
            subject   = args.subject,
            body_html = body_html,
            to_list   = parse_recipients(args.to),
            cc_list   = parse_recipients(args.cc),
        )
    except smtplib.SMTPAuthenticationError:
        log.error("SMTP authentication failed. Check credentials.")
        sys.exit(1)
    except smtplib.SMTPException as exc:
        log.error("SMTP error: %s", exc)
        sys.exit(1)
    except Exception as exc:
        log.error("Unexpected error: %s", exc)
        sys.exit(1)


if __name__ == '__main__':
    main()
