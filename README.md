# Invoice Email Forwarder

This Python application automates the process of fetching overdue invoices and forwarding them to customers via email. It integrates with Gmail for email handling and uses Wave Invoice Manager and Email Manager classes for invoice data retrieval and email construction. The application can be run locally or deployed as an AWS Lambda function using Docker.

## Architecture

### Overview

1. **AWS Lambda**: The core component that executes the invoice processing logic. It runs the Python application in a serverless environment, scaling automatically based on demand.
2. **Amazon EventBridge (Scheduler)**: Triggers the Lambda function at scheduled intervals to process overdue invoices. You can configure it to run the function daily, weekly, or at any other interval as required.
3. **Amazon ECR**: Stores the Docker image of the application, which Lambda uses to run the function.
4. **Gmail**: Used for sending and receiving emails related to invoices.
5. **Wave API**: Provides invoice data, which is retrieved and processed by the application.

### Architecture Diagram

+---------------------+ +-----------------------+ +-----------------+
| Amazon EventBridge | ------> | AWS Lambda | -----> | Gmail |
| (Scheduler) | | (Invoice Processing) | | (Email Sending)|
+---------------------+ +-----------------------+ +-----------------+
|
|
v
+-------------------+
| Wave API |
| (Invoice Data) |
+-------------------+

## Prerequisites

Before running the application, ensure you have the following:

1. **Python 3.x**: Ensure Python 3.x is installed on your machine if running locally.
2. **Docker**: Ensure Docker is installed and running if you plan to use Docker.
3. **AWS CLI**: Ensure AWS CLI is installed and configured with the appropriate credentials and region if deploying to AWS Lambda.

### Environment Variables

Set the following environment variables:
- `EMAIL_ADDRESS`: Your Gmail email address.
- `EMAIL_PASS`: Your Gmail email password (or app-specific password).
- `SENDBOOL`: Set to `'True'` to send emails or `'False'` to disable email sending.
- `BUSINESS_ID`: Your Wave business ID.
- `AUTHORIZATION_TOKEN`: Your authorization token for Wave API.

### Required Python Packages

- `imaplib` (standard library)
- `smtplib` (standard library)
- `email` (standard library)
- `waveXtract`: Custom module for Wave Invoice Manager.
- `emailConstruct`: Custom module for Email Manager.

Install required packages using:
```bash
pip install waveXtract emailConstruct
```

## Running With Docker
```
docker build -t invoice-email-forwarder .
docker run -e EMAIL_ADDRESS=<your-email> -e EMAIL_PASS=<your-password> -e SENDBOOL=True -e BUSINESS_ID=<your-business-id> -e AUTHORIZATION_TOKEN=<your-token> invoice-email-forwarder
