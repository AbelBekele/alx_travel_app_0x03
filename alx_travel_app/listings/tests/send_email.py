import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv()
import os

def send_email(sender_email, sender_password, recipient_email, subject, body):
    # Validate inputs
    if not all([sender_email, sender_password, recipient_email]):
        raise ValueError("Email addresses and password cannot be empty")

    # Create message container
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    # Add body to email
    message.attach(MIMEText(body, 'plain'))

    server = None
    try:
        # Create SMTP session with explicit debugging
        print("Attempting to connect to SMTP server...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)  # Add debugging
        
        print("Enabling TLS...")
        server.starttls()  # Enable TLS
        
        print(f"Attempting login for {sender_email}...")
        # Login to the server
        server.login(str(sender_email), str(sender_password))
        
        # Send email
        print("Sending email...")
        text = message.as_string()
        server.sendmail(sender_email, recipient_email, text)
        print("Email sent successfully!")
        
    except smtplib.SMTPAuthenticationError as e:
        print("Authentication failed! Please check your email and App Password.")
        print(f"Error details: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(f"Error type: {type(e)}")
    
    finally:
        if server:
            print("Closing server connection...")
            server.quit()

if __name__ == "__main__":
    # Replace these with your actual credentials and message
    sender_email = os.getenv('EMAIL_HOST_USER')
    sender_password = os.getenv('EMAIL_HOST_PASSWORD')  # Your 16-character App Password
    recipient_email = "itsabel77@gmail.com"
    subject = "Test Email"
    body = "This is a test email sent from Python!"
    
    # Verify that credentials have been updated
    if "your.email" in sender_email or "your-16-char-app-password" in sender_password:
        print("Error: Please replace the placeholder email and App Password with your actual credentials")
    else:
        send_email(sender_email, sender_password, recipient_email, subject, body)