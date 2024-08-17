import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from datetime import datetime
import calendar
class EmailManager:
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password

    def construct_email(self, customer_name, invoices):
        current_month_number = datetime.now().month
        current_month_name = calendar.month_name[current_month_number]
        subject = f"Your Invoices for {current_month_name}"
        # Create the HTML content for the email body
        body = f"""
        <html>
            <body>
                <p>Hi {customer_name},</p>
                <p>Please find your invoice details below:</p>
        """

        # Loop through each invoice and add its details to the email body
        for invoice_info in invoices:
            body += f"""<hr>
                <p><strong>Invoice Number:</strong> {invoice_info['invoiceNumber']}</p>"""
            body += f"""               
                <p><strong>Last Viewed At:</strong> {invoice_info['lastViewedAt']}</p>"""
            overdue = int(invoice_info['daysOverdue'])
            if overdue > 0:
                subject = f"Action Required: Your Overdue Invoices as of {current_month_name}"
                body += f"""
                    <p><strong>Days Overdue:</strong> {invoice_info['daysOverdue']}</p>"""
            body += f"""
                <p><strong>Due Date:</strong> {invoice_info['dueDate']}</p>"""
            body += f"""
                <p><a href="{invoice_info['viewUrl']}" target="_blank" style="background-color: #007bff; color: white; padding: 10px 15px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; border-radius: 5px;">View Invoice</a></p>
       """
        # Add the small print for automated message
        body += """
                <p><small>This is an automated message.</small></p>
        """
        # Close the HTML content
        body += """
                <p>Best regards,<br>DevWorx LLC</p>
            </body>
        </html>
        """

        # Create the email message
        msg = MIMEMultipart('alternative')
        msg['From'] = self.sender_email
        msg['To'] = invoice_info['email']
        msg['Subject'] = subject
        msg['Bcc'] = self.sender_email
        # Attach both plain text and HTML versions of the email
        msg.attach(MIMEText(body, 'html'))

        return msg

    def send_email(self, msg):
        SMTP_SERVER = 'smtp.gmail.com'
        SMTP_PORT = 465

        try:
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
        except Exception as e:
            print(f"Failed to send email: {str(e)}")


