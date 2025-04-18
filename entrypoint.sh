#!/bin/sh

# Add dynamically-mounted custom host entries
if [ -f /app/custom_hosts ]; then
    cat /app/custom_hosts >> /etc/hosts
fi

# Start the Flask application
exec python app.py
