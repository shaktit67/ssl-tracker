from flask import Flask, render_template, request, redirect, url_for
import ssl
import socket
import datetime
import smtplib
import json
import os
from email.mime.text import MIMEText
from apscheduler.schedulers.background import BackgroundScheduler
import certifi

app = Flask(__name__)
DATA_FILE = 'websites.json'


def load_websites():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []


def save_websites(websites):
    with open(DATA_FILE, 'w') as file:
        json.dump(websites, file, default=str, indent=4)


def check_ssl_expiry(host):
    context = ssl.create_default_context(cafile=certifi.where())

    # Parse hostname and port (default to 443)
    if ':' in host:
        hostname, port = host.split(':')
        port = int(port)
    else:
        hostname = host
        port = 443

    try:
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                ssl_info = ssock.getpeercert()
                expiry_date = datetime.datetime.strptime(ssl_info['notAfter'], '%b %d %H:%M:%S %Y %Z')
                expiry_date = expiry_date.replace(tzinfo=datetime.timezone.utc)
                days_left = (expiry_date - datetime.datetime.now(datetime.timezone.utc)).days
                return days_left, expiry_date
    except Exception as e:
        print(f"Error checking SSL for {host}: {e}")
        return None, None


def send_email_notification(receiver_email, hostname, days_left, expiry_date):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    subject = f"SSL Expiration Warning for {hostname}"
    body = f"SSL Certificate for {hostname} expires in {days_left} days, on {expiry_date}."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


websites = load_websites()


def schedule_checks():
    for site in websites:
        days_left, expiry_date = check_ssl_expiry(site['url'])
        if days_left is None:
            site['days_left'] = -1
            site['expiry_date'] = "Error"
        else:
            site['days_left'] = days_left
            site['expiry_date'] = expiry_date.strftime("%Y-%m-%d")

            if days_left in [30, 15, 10, 5]:
                send_email_notification(site['email'], site['url'], days_left, expiry_date.strftime("%Y-%m-%d"))
    save_websites(websites)


scheduler = BackgroundScheduler()
scheduler.add_job(schedule_checks, 'interval', hours=24)
scheduler.start()


@app.route('/', methods=['GET', 'POST'])
def index():
    categories = ['Production', 'Development', 'Internal', 'Stage']
    selected_category = request.args.get('category', 'All')

    if request.method == 'POST':
        url = request.form['url']
        email = request.form['email']
        category = request.form['category']
        days_left, expiry_date = check_ssl_expiry(url)

        if days_left is None:
            expiry_date_str = "Error"
            days_left_numeric = -1
        else:
            expiry_date_str = expiry_date.strftime("%Y-%m-%d")
            days_left_numeric = days_left

        updated = False
        for site in websites:
            if site['url'] == url:
                site['email'] = email
                site['category'] = category
                site['days_left'] = days_left_numeric
                site['expiry_date'] = expiry_date_str
                updated = True
                break

        if not updated:
            websites.append({
                'url': url,
                'email': email,
                'category': category,
                'days_left': days_left_numeric,
                'expiry_date': expiry_date_str
            })

        save_websites(websites)
        return redirect(url_for('index', category=category))

    # Filter by selected category
    filtered_websites = websites
    if selected_category != 'All':
        filtered_websites = [site for site in websites if site['category'] == selected_category]

    sorted_websites = sorted(filtered_websites, key=lambda x: (x['days_left'] == -1, x['days_left']))
    print("Selected category:", selected_category)
    return render_template(
        'index.html',
        websites=sorted_websites,
        categories=categories,
        selected_category=selected_category
    )


@app.route('/remove/<path:url>', methods=['POST'])
def remove_website(url):
    global websites
    websites = [site for site in websites if site['url'] != url]
    save_websites(websites)
    return redirect(url_for('index'))


if __name__ == '__main__':
    schedule_checks()
    app.run(host='0.0.0.0', debug=True)
