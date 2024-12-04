import subprocess
import time
import smtplib
from email.mime.text import MIMEText
from datetime import datetime


def ping(host):
    try:
        subprocess.check_output(['ping', '-c', '1', host], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False


def get_provider_name(ip):
    providers = {
        '192.168.0.173': 'CLARO',
        '192.168.0.196': 'LIGGA'
    }
    return providers.get(ip, ip)


def send_alert(failed_ip):
    smtp_server = "smtp.office365.com"
    port = 587
    sender = "no-reply@funtefpr.org.br"
    password = "Tam16289"
    recipients = ["ti@funtefpr.org.br", "aldrinstori@gmail.com"]

    provider_name = get_provider_name(failed_ip)
    msg = MIMEText(f"Network connection failed for {provider_name} (IP: {failed_ip})\nTimestamp: {datetime.now()}")
    msg['Subject'] = f'Network Alert - {provider_name} is unreachable'
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipients, msg.as_string())
        server.quit()
        print(f"Alert sent for {provider_name}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")


def monitor_networks():
    networks = ['192.168.0.173', '192.168.0.196']

    while True:
        for ip in networks:
            provider_name = get_provider_name(ip)
            if not ping(ip):
                print(f"Network {provider_name} is down")
                send_alert(ip)
            else:
                print(f"Network {provider_name} is up - {datetime.now()}")

        time.sleep(600)  # Wait 10 minutes


if __name__ == "__main__":
    try:
        monitor_networks()
    except KeyboardInterrupt:
        print("\nMonitoring stopped")