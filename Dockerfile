FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables (use placeholders, set real values during docker run)
ENV SMTP_SERVER=smtp.office365.com
ENV SMTP_PORT=587
ENV SENDER_EMAIL=helpdesk@easternenterprise.com
ENV SENDER_PASSWORD=yourpassword

# Ensure the entrypoint script is executable
RUN chmod +x entrypoint.sh

# Expose port
EXPOSE 5000

# Start the application via entrypoint
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
