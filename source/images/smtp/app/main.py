#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, make_response
from email.message import EmailMessage
from smtplib import SMTP_SSL

app = Flask(__name__, static_url_path="")


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/sendemail', methods=['GET'])
def sendemail():
    smtp_server = 'smtp.mail.ru'
    username = 'SmartHR@inbox.ru'
    password = 'greenatomhackathon'

    sender = 'SmartHR Notify Service <SmartHR@inbox.ru>'
    content = request.json

    if 'to' not in content:
        return make_response(
            jsonify({'error': 'parameter \'to\' is missing'}), 400)
    if 'subject' not in content:
        return make_response(
            jsonify({'error': 'parameter \'subject\' is missing'}), 400)
    if 'msg' not in content:
        return make_response(
            jsonify({'error': 'parameter \'msg\' is missing'}), 400)

    destination = content['to']
    subject = content['subject']
    content = content['msg']

    emsg = EmailMessage()
    emsg.set_content(content)

    emsg['Subject'] = subject
    emsg['From'] = sender
    emsg['To'] = destination

    try:
        s = SMTP_SSL(smtp_server)
        s.login(username, password)
        try:
            s.send_message(emsg)
        finally:
            s.quit()
    except Exception as E:
        return make_response(
            jsonify({'error': str(E)}), 502)
    return make_response(
        jsonify({'result': {'to': destination, 'subject': subject, 'message': content}}), 200)


def main():
    app.run(debug=True)
