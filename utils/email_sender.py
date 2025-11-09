"""
Email sending utility functions using SMTP
"""

import smtplib
import re
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr


def parse_email(email_content):
    """
    Parse the generated email content to extract subject and body.
    
    Args:
        email_content (str): The full email content
        
    Returns:
        tuple: (subject, body) or (None, email_content) if parsing fails
    """
    lines = email_content.split('\n')
    
    # Try to find subject line
    subject = None
    body_start_idx = 0
    
    for i, line in enumerate(lines):
        if line.lower().startswith('subject:'):
            subject = line[8:].strip()  # Remove "Subject:"
            body_start_idx = i + 1
            break
    
    # If no subject found, extract first line or use default
    if subject is None and lines:
        # Check if first line looks like a subject
        first_line = lines[0].strip()
        if len(first_line) < 100 and ':' not in first_line:
            subject = first_line
            body_start_idx = 1
        else:
            subject = "Job Application"
    
    # Get body (everything after subject)
    body_lines = lines[body_start_idx:]
    body = '\n'.join(body_lines).strip()
    
    return subject, body


def validate_email(email):
    """
    Validate email address format.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def get_smtp_config(email_address):
    """
    Get SMTP configuration based on email provider.
    
    Args:
        email_address (str): User's email address
        
    Returns:
        dict: SMTP configuration with host and port, or None if provider not supported
    """
    email_domain = email_address.split('@')[1].lower()
    
    # Common email provider configurations
    smtp_configs = {
        'gmail.com': {
            'host': 'smtp.gmail.com',
            'port': 587,
            'provider': 'Gmail'
        },
        'outlook.com': {
            'host': 'smtp-mail.outlook.com',
            'port': 587,
            'provider': 'Outlook'
        },
        'hotmail.com': {
            'host': 'smtp-mail.outlook.com',
            'port': 587,
            'provider': 'Outlook'
        },
        'live.com': {
            'host': 'smtp-mail.outlook.com',
            'port': 587,
            'provider': 'Outlook'
        },
        'yahoo.com': {
            'host': 'smtp.mail.yahoo.com',
            'port': 587,
            'provider': 'Yahoo'
        },
        'yahoo.co.uk': {
            'host': 'smtp.mail.yahoo.com',
            'port': 587,
            'provider': 'Yahoo'
        },
        'aol.com': {
            'host': 'smtp.aol.com',
            'port': 587,
            'provider': 'AOL'
        }
    }
    
    return smtp_configs.get(email_domain)


def send_email(sender_email, app_password, recipient_email, email_content, custom_sender_name=None, attachment_path=None):
    """
    Send email using SMTP.
    
    Args:
        sender_email (str): Sender's email address
        app_password (str): App-specific password or regular password
        recipient_email (str): Recipient's email address
        email_content (str): Full email content (will be parsed for subject/body)
        custom_sender_name (str, optional): Custom sender name
        attachment_path (str, optional): Path to file to attach (e.g., resume PDF)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Validate email addresses
        if not validate_email(sender_email):
            return False, "Invalid sender email address format"
        
        if not validate_email(recipient_email):
            return False, "Invalid recipient email address format"
        
        # Get SMTP configuration
        smtp_config = get_smtp_config(sender_email)
        if not smtp_config:
            return False, f"Email provider not recognized. Supported providers: Gmail, Outlook, Yahoo, AOL"
        
        # Parse email content
        subject, body = parse_email(email_content)
        
        # Create email message
        msg = MIMEMultipart()
        
        # Set sender name
        sender_name = custom_sender_name if custom_sender_name else sender_email.split('@')[0]
        msg['From'] = formataddr((sender_name, sender_email))
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'plain'))
        
        # Add attachment if provided
        if attachment_path and os.path.exists(attachment_path):
            try:
                with open(attachment_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                
                # Get filename from path
                filename = os.path.basename(attachment_path)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {filename}'
                )
                
                msg.attach(part)
            except Exception as e:
                # Continue without attachment if there's an error
                pass
        
        # Connect to server and send email
        server = smtplib.SMTP(smtp_config['host'], smtp_config['port'])
        server.starttls()  # Enable encryption
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        
        return True, f"Email sent successfully to {recipient_email}!"
        
    except smtplib.SMTPAuthenticationError:
        return False, "Authentication failed. Please check your email and app password."
    
    except smtplib.SMTPRecipientsRefused:
        return False, "Recipient email address was refused by the server."
    
    except smtplib.SMTPException as e:
        return False, f"SMTP error: {str(e)}"
    
    except Exception as e:
        return False, f"Error sending email: {str(e)}"

