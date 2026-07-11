"""
app/email_sender.py
Sends the drafted email to the customer via Gmail SMTP.
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


def send_email(
        to_email: str,
        subject: str,
        body: str,
        customer_name: str = "Customer"
) -> dict:
    """
    Sends email to customer via Gmail SMTP.

    Returns:
        {"success": True, "message": "Email sent"}
        {"success": False, "message": "Error details"}
    """

    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        return {
            "success": False,
            "message": "Gmail credentials not configured in .env"
        }

    try:
        # Create email
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"AI Support Agent <{GMAIL_ADDRESS}>"
        msg["To"] = to_email

        # Plain text version
        text_part = MIMEText(body, "plain", "utf-8")

        # HTML version — looks better in inbox
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px;">
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px;">
                <h2 style="color: #2c3e50;">Customer Support</h2>
                <hr style="border: 1px solid #dee2e6;">
                <div style="padding: 20px 0; white-space: pre-line; color: #333;">
                    {body}
                </div>
                <hr style="border: 1px solid #dee2e6;">
                <p style="color: #888; font-size: 12px;">
                    This email was sent by AI Complaint Resolution Agent.
                    Please do not reply to this email directly.
                </p>
            </div>
        </body>
        </html>
        """
        html_part = MIMEText(html_body, "html", "utf-8")

        # Attach both versions
        msg.attach(text_part)
        msg.attach(html_part)

        # Send via Gmail SMTP
        print(f"📧 Sending email to {to_email}...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, to_email, msg.as_string())

        print(f"✅ Email sent successfully to {to_email}")
        return {
            "success": True,
            "message": f"Email sent to {to_email}"
        }

    except smtplib.SMTPAuthenticationError:
        error = "Gmail authentication failed. Check your App Password in .env"
        print(f"❌ {error}")
        return {"success": False, "message": error}

    except smtplib.SMTPException as e:
        error = f"SMTP error: {str(e)}"
        print(f"❌ {error}")
        return {"success": False, "message": error}

    except Exception as e:
        error = f"Unexpected error: {str(e)}"
        print(f"❌ {error}")
        return {"success": False, "message": error}


# ── Test ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Testing email sender...")
    print(f"From: {GMAIL_ADDRESS}")

    # Send test email to yourself
    result = send_email(
        to_email=GMAIL_ADDRESS,  # sends to yourself for testing
        subject="Test - AI Complaint Resolution Agent",
        body="This is a test email from your AI Complaint Resolution Agent.\n\nIf you receive this, email sending is working correctly!\n\nRegards,\nAI Support Agent",
        customer_name="Tejas"
    )

    print(f"Result: {result}")