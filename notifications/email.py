import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
import aiosmtplib
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", "")
SAFETY_OFFICER_EMAILS = os.getenv("SAFETY_OFFICER_EMAILS", "").split(",")

_smtp_configured = bool(SMTP_HOST and SMTP_USER and SMTP_PASSWORD and EMAIL_FROM)


async def send_email(recipients: List[str], subject: str, body: str):
    """Send an HTML email. Silently skips if SMTP is not configured."""
    if not _smtp_configured:
        print(f"[Email] SMTP not configured. Would send to {recipients}: {subject}")
        return

    try:
        message = MIMEMultipart("alternative")
        message["From"] = EMAIL_FROM
        message["To"] = ", ".join(recipients)
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))

        await aiosmtplib.send(
            message,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            username=SMTP_USER,
            password=SMTP_PASSWORD,
            start_tls=True,
        )
    except Exception as error:
        print(f"[Email] Failed to send email: {error}")


async def send_task_assignment_email(assignee_email: str, task_name: str, batch_title: str):
    """Send email notification when a user is assigned to a task."""
    subject = f"Task Assignment: {task_name}"
    body = f"""
    <h3>You have been assigned to a task</h3>
    <p><strong>Task:</strong> {task_name}</p>
    <p><strong>Batch:</strong> {batch_title}</p>
    <p>Please log in to PlanSafe360 to view the details.</p>
    """
    await send_email([assignee_email], subject, body)


async def send_incident_notification_email(incident_name: str, severity: str, location: str = None):
    """Send email notification to safety officers when an incident is created."""
    officers = [e.strip() for e in SAFETY_OFFICER_EMAILS if e.strip()]
    if not officers:
        print("[Email] No safety officer emails configured. Skipping incident notification.")
        return

    subject = f"New Incident Report: {incident_name} [{severity or 'unknown'}]"
    body = f"""
    <h3>New Incident Reported</h3>
    <p><strong>Incident:</strong> {incident_name}</p>
    <p><strong>Severity:</strong> {severity or 'Not specified'}</p>
    <p><strong>Location:</strong> {location or 'Not specified'}</p>
    <p>Please log in to PlanSafe360 to review and investigate.</p>
    """
    await send_email(officers, subject, body)
