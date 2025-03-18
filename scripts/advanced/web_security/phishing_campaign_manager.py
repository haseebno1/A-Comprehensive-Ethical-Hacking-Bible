#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phishing Campaign Manager
Author: Abdul Haseeb (@h4x33b)
Version: 1.0.0
Description: A comprehensive tool for managing ethical phishing campaigns for security
             awareness training. This tool helps security professionals create, manage,
             and track phishing simulations to educate users about phishing threats.
             For educational and authorized security testing purposes only.
"""

import argparse
import os
import sys
import time
import json
import csv
import smtplib
import random
import string
import hashlib
import sqlite3
import datetime
import re
import base64
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.utils import formatdate
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import threading
import ssl
import jinja2

# ASCII Art Banner
BANNER = """
 ____  _     _     _     _                 ____ __  __ 
|  _ \\| |__ (_)___| |__ (_)_ __   __ _    / ___|  \\/  |
| |_) | '_ \\| / __| '_ \\| | '_ \\ / _` |  | |   | |\\/| |
|  __/| | | | \\__ \\ | | | | | | | (_| |  | |___| |  | |
|_|   |_| |_|_|___/_| |_|_|_| |_|\\__, |   \\____|_|  |_|
                                 |___/                 
                                                                By: Abdul Haseeb (@h4x33b)
"""

# Default database file
DEFAULT_DB_FILE = "phishing_campaign.db"

# Default templates directory
DEFAULT_TEMPLATES_DIR = "templates"

# Default tracking URL
DEFAULT_TRACKING_URL = "http://localhost:8080"

# Default SMTP settings
DEFAULT_SMTP_SERVER = "localhost"
DEFAULT_SMTP_PORT = 25
DEFAULT_SMTP_USE_TLS = False

# Email template placeholders
EMAIL_PLACEHOLDERS = {
    "{{first_name}}": "Recipient's first name",
    "{{last_name}}": "Recipient's last name",
    "{{full_name}}": "Recipient's full name",
    "{{email}}": "Recipient's email address",
    "{{company}}": "Recipient's company name",
    "{{department}}": "Recipient's department",
    "{{position}}": "Recipient's job position",
    "{{tracking_url}}": "Tracking URL for click tracking",
    "{{current_date}}": "Current date",
    "{{current_time}}": "Current time",
    "{{random_code}}": "Random code (for password reset simulations)",
    "{{sender_name}}": "Sender's display name",
    "{{sender_email}}": "Sender's email address",
    "{{sender_position}}": "Sender's job position",
    "{{sender_company}}": "Sender's company name",
    "{{sender_phone}}": "Sender's phone number"
}

# Sample phishing templates
SAMPLE_TEMPLATES = [
    {
        "name": "Password Reset",
        "subject": "Urgent: Your {{company}} Account Password Reset",
        "sender_name": "{{company}} IT Support",
        "sender_email": "it-support@{{company}}.com",
        "html_content": """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; }
                .container { width: 600px; margin: 0 auto; }
                .header { background-color: #0078D4; color: white; padding: 10px; text-align: center; }
                .content { padding: 20px; }
                .footer { font-size: 12px; color: #666; text-align: center; padding: 10px; }
                .button { background-color: #0078D4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>{{company}} IT Department</h2>
                </div>
                <div class="content">
                    <p>Dear {{first_name}},</p>
                    <p>We have received a request to reset your {{company}} account password. If you did not make this request, please ignore this email.</p>
                    <p>To reset your password, please click the link below:</p>
                    <p style="text-align: center;">
                        <a href="{{tracking_url}}?id={{email}}&action=password_reset" class="button">Reset Password</a>
                    </p>
                    <p>Alternatively, you can copy and paste the following URL into your browser:</p>
                    <p>{{tracking_url}}?id={{email}}&action=password_reset</p>
                    <p>This link will expire in 24 hours.</p>
                    <p>Thank you,<br>{{company}} IT Support Team</p>
                </div>
                <div class="footer">
                    <p>This email was sent to {{email}}. If you have questions, please contact IT support at it-support@{{company}}.com.</p>
                </div>
            </div>
        </body>
        </html>
        """
    },
    {
        "name": "Document Share",
        "subject": "Important Document Shared with You",
        "sender_name": "{{sender_name}}",
        "sender_email": "{{sender_email}}",
        "html_content": """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; }
                .container { width: 600px; margin: 0 auto; }
                .header { background-color: #0078D4; color: white; padding: 10px; text-align: center; }
                .content { padding: 20px; }
                .footer { font-size: 12px; color: #666; text-align: center; padding: 10px; }
                .button { background-color: #0078D4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Document Sharing Notification</h2>
                </div>
                <div class="content">
                    <p>Hi {{first_name}},</p>
                    <p>I've shared an important document with you that requires your review.</p>
                    <p>Please click the link below to access the document:</p>
                    <p style="text-align: center;">
                        <a href="{{tracking_url}}?id={{email}}&action=document_access" class="button">View Document</a>
                    </p>
                    <p>This document contains important information regarding our upcoming project.</p>
                    <p>Best regards,<br>{{sender_name}}<br>{{sender_position}}<br>{{sender_company}}</p>
                </div>
                <div class="footer">
                    <p>This email was sent to {{email}}. If you have questions, please contact {{sender_email}}.</p>
                </div>
            </div>
        </body>
        </html>
        """
    },
    {
        "name": "Invoice Payment",
        "subject": "Invoice #INV-{{random_code}} Payment Required",
        "sender_name": "{{company}} Accounting",
        "sender_email": "accounting@{{company}}.com",
        "html_content": """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; }
                .container { width: 600px; margin: 0 auto; }
                .header { background-color: #0078D4; color: white; padding: 10px; text-align: center; }
                .content { padding: 20px; }
                .footer { font-size: 12px; color: #666; text-align: center; padding: 10px; }
                .button { background-color: #0078D4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; }
                .invoice-table { width: 100%; border-collapse: collapse; }
                .invoice-table th, .invoice-table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                .invoice-table th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>{{company}} Accounting Department</h2>
                </div>
                <div class="content">
                    <p>Dear {{first_name}},</p>
                    <p>This is a reminder that invoice #INV-{{random_code}} is due for payment.</p>
                    <p>Invoice details:</p>
                    <table class="invoice-table">
                        <tr>
                            <th>Invoice #</th>
                            <th>Date</th>
                            <th>Amount</th>
                            <th>Due Date</th>
                        </tr>
                        <tr>
                            <td>INV-{{random_code}}</td>
                            <td>{{current_date}}</td>
                            <td>$1,299.99</td>
                            <td>{{current_date}}</td>
                        </tr>
                    </table>
                    <p>Please process this payment as soon as possible by clicking the link below:</p>
                    <p style="text-align: center;">
                        <a href="{{tracking_url}}?id={{email}}&action=invoice_payment" class="button">Process Payment</a>
                    </p>
                    <p>Thank you for your prompt attention to this matter.</p>
                    <p>Regards,<br>{{company}} Accounting Team</p>
                </div>
                <div class="footer">
                    <p>This email was sent to {{email}}. If you have questions, please contact accounting@{{company}}.com.</p>
                </div>
            </div>
        </body>
        </html>
        """
    }
]

# Landing page templates
LANDING_PAGE_TEMPLATES = {
    "password_reset": """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Password Reset</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f5f5f5; }
            .container { width: 400px; padding: 20px; background-color: white; border-radius: 5px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); }
            h2 { text-align: center; color: #0078D4; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input[type="password"] { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
            .button { background-color: #0078D4; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; width: 100%; }
            .button:hover { background-color: #005a9e; }
            .alert { padding: 10px; background-color: #f8d7da; color: #721c24; border-radius: 4px; margin-bottom: 15px; display: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Reset Your Password</h2>
            <div class="alert" id="alert">This is a security awareness test. In a real scenario, this could have been a phishing attempt.</div>
            <div id="form-container">
                <div class="form-group">
                    <label for="current-password">Current Password:</label>
                    <input type="password" id="current-password" name="current-password">
                </div>
                <div class="form-group">
                    <label for="new-password">New Password:</label>
                    <input type="password" id="new-password" name="new-password">
                </div>
                <div class="form-group">
                    <label for="confirm-password">Confirm New Password:</label>
                    <input type="password" id="confirm-password" name="confirm-password">
                </div>
                <button class="button" onclick="showAlert()">Reset Password</button>
            </div>
        </div>
        <script>
            function showAlert() {
                document.getElementById('alert').style.display = 'block';
                document.getElementById('form-container').style.opacity = '0.5';
                setTimeout(function() {
                    window.location.href = '{{redirect_url}}';
                }, 5000);
            }
        </script>
    </body>
    </html>
    """,
    
    "document_access": """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Document Access</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f5f5f5; }
            .container { width: 400px; padding: 20px; background-color: white; border-radius: 5px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); }
            h2 { text-align: center; color: #0078D4; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input[type="email"], input[type="password"] { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
            .button { background-color: #0078D4; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; width: 100%; }
            .button:hover { background-color: #005a9e; }
            .alert { padding: 10px; background-color: #f8d7da; color: #721c24; border-radius: 4px; margin-bottom: 15px; display: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Document Access</h2>
            <div class="alert" id="alert">This is a security awareness test. In a real scenario, this could have been a phishing attempt.</div>
            <div id="form-container">
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" value="{{email}}">
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password">
                </div>
                <button class="button" onclick="showAlert()">Access Document</button>
            </div>
        </div>
        <script>
            function showAlert() {
                document.getElementById('alert').style.display = 'block';
                document.getElementById('form-container').style.opacity = '0.5';
                setTimeout(function() {
                    window.location.href = '{{redirect_url}}';
                }, 5000);
            }
        </script>
    </body>
    </html>
    """,
    
    "invoice_payment": """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Invoice Payment</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f5f5f5; }
            .container { width: 400px; padding: 20px; background-color: white; border-radius: 5px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); }
            h2 { text-align: center; color: #0078D4; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input[type="text"], input[type="number"] { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
            .button { background-color: #0078D4; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; width: 100%; }
            .button:hover { background-color: #005a9e; }
            .alert { padding: 10px; background-color: #f8d7da; color: #721c24; border-radius: 4px; margin-bottom: 15px; display: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Invoice Payment</h2>
            <div class="alert" id="alert">This is a security awareness test. In a real scenario, this could have been a phishing attempt.</div>
            <div id="f<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>