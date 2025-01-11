# network_monitor
A simple python script to send an email alert if you have 2 connections and one of them fails.

The script pings google.com each 5-10 minutes, if one internet doesn't respond the script changes the connection and uses the up connection to send the email with the alert.

You must have an eth adapter on the computer to connect the backup connection.


