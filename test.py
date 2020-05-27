#!/usr/bin/python3.7
import asyncio
import random
import flask
app = flask.Flask(__name__,template_folder="templates", static_folder="static")
@app.route('/')
def button():
    return '''<a href="/download_pdf">choose folder</a> <br> <a href="/send_pdf">download</a>'''
@app.route('/download_pdf')
def download_pdf():
    return flask.send_file("main.pdf")
@app.route('/send_pdf')
def send_pdf():
    return flask.send_file("main.pdf")
def main():
    app.run(host= '0.0.0.0', port = 80)
if __name__ == "__main__":
    main()
