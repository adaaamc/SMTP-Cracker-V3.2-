Overview
SMTP Cracker V3.2 is a multithreaded Python tool designed for testing SMTP server credentials against email/password combinations. It automatically skips major email providers (Google, Microsoft, Yahoo, AOL) and focuses on smaller/independent mail servers.

Key Features
Multi-threaded cracking (300 concurrent threads)

Automatic SMTP server discovery - attempts multiple common prefixes (smtp., mail., webmail., etc.) on ports 587, 465, and 25

Smart filtering - automatically skips accounts from Google, Microsoft, Yahoo, and AOL

SSL/TLS support - handles both plain and encrypted connections

Real-time progress tracking - displays cracked count and queue status

Results logging - saves cracked credentials to cracked_smtps.txt and cracked_Mailaccess.txt

Notification system - sends cracked credentials to a specified email address

Technical Specifications
Language: Python 3

Threading: 300 concurrent workers

Timeout: 5 seconds per connection

Supported Ports: 25, 465 (SSL), 587 (TLS)

Dependencies: colorama (optional, for colored output)

⚠️ Disclaimer
This tool is intended for educational and authorized testing purposes only. Unauthorized access to email accounts is illegal and violates terms of service. Use only on systems you own or have explicit permission to test.
Usage
python3 smtp_cracker.py
Notification email address

Combo file path (format: email:password per line)

Output Files
cracked_smtps.txt - Full credentials with server details

cracked_Mailaccess.txt - Simplified email:password format

