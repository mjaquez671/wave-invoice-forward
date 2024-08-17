import imaplib
import os
import smtplib
import email
import waveXtract as w
import emailConstruct as e
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email credentials and server details
IMAP_SERVER = 'imap.gmail.com'
SMTP_SERVER = 'smtp.gmail.com'
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASS')#'hbnl slne mwvn wvst'
SEND_EMAIL = os.getenv('SENDBOOL')

# Assuming you've set environment variables for your business ID, authorization token, and Twilio credentials
business_id = os.getenv("BUSINESS_ID")
auth_token = "Bearer " + os.getenv("AUTHORIZATION_TOKEN")
query_path = "./overdue.gql"

# Function to search for the email and get its ID
def search_email(sender_email):
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    mail.select('inbox')

    result, data = mail.search(None, f'(UNSEEN FROM "{sender_email}")')
    email_ids = data[0].split()

    mail.close()
    mail.logout()

    return email_ids


# Function to fetch the email using IMAP
def fetch_email(email_id):
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    mail.select('inbox')

    result, data = mail.fetch(email_id, '(RFC822)')
    raw_email = data[0][1]
    # Mark the email as read
    # mail.store(email_id, '+FLAGS', '\\Seen')
    mail.close()
    mail.logout()

    return raw_email


# Function to forward the email using SMTP
def forward_email(raw_email, customer_email):
    original_email = email.message_from_bytes(raw_email)

    # Create a new email
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = customer_email
    msg['Subject'] = original_email['Subject']

    # Optional: Add a personal message at the beginning
    personal_message = "Hi [Customer Name],\n\nPlease find your invoice attached below.\n\nBest regards,\n[Your Name]\n\n"

    # Get the body of the original email
    original_body = ""
    if original_email.is_multipart():
        for part in original_email.get_payload():
            if part.get_content_type() == 'text/plain':
                original_body = part.get_payload(decode=True).decode('utf-8')
                break
    else:
        original_body = original_email.get_payload(decode=True).decode('utf-8')

    # Combine the personal message and the original body
    combined_body = personal_message + original_body

    # Attach the combined body to the new email
    msg.attach(MIMEText(combined_body, 'plain'))

    # Send the email
    with smtplib.SMTP_SSL(SMTP_SERVER) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

# Main script
def main(event,context):
    overdue = ""
    business_id = os.getenv("BUSINESS_ID")
    auth_token = "Bearer " + os.getenv("AUTHORIZATION_TOKEN")
    invoiceManager = w.WaveInvoiceManager(auth_token, business_id)
    statuses = ["OVERDUE", "SENT"]
    for status in statuses:
        vars = {
            "businessId": business_id,
            "page": 1,
            "pageSize": 10,
            "status": status
        }
        with open("./overdue.gql", "r") as gql_file:
            overdue = gql_file.read()
        invoice_data = invoiceManager.fetch_invoice_data(overdue, variables=vars)
        organized_data = invoiceManager.organize_invoice_data()
        email_manager = e.EmailManager(EMAIL_ADDRESS, EMAIL_PASSWORD)

        for customer_name, invoices in organized_data.items():
            first_name = invoices[0]['firstName']
            email_message = email_manager.construct_email(first_name, invoices)

            if SEND_EMAIL == 'True':
                email_manager.send_email(email_message)
            else:
                print("Not Sending")
            print(f"Email sent to {customer_name} for invoice {invoices[0]['invoiceNumber']}")


if __name__ == "__main__":
   main(None,None)