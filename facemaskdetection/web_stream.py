# Import neccessary libraries
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2

# Import the detection script
import drone_config 

outputFrame = None
lock = threading.Lock()

app = Flask(__name__)

vs = VideoStream(src=0).start()
time.sleep(2.0)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/notification')
def notify():
    return render_template('./notification.html')
