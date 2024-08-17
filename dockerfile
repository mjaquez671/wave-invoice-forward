# Use an official AWS Lambda base image
FROM public.ecr.aws/lambda/python:3.8

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the function code
COPY app.py ${LAMBDA_TASK_ROOT}
COPY waveXtract.py ${LAMBDA_TASK_ROOT}
COPY emailConstruct.py ${LAMBDA_TASK_ROOT}
COPY overdue.gql ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler
CMD ["app.main"]
