#!/usr/bin/env python
import time

import cv2 # OpenCV
from flask import Flask, render_template, Response # Flash web framework
from SmartCamera import SmartCamera

app = Flask(__name__)


def gen(sc):
    count = 1
    while True:
        frame = sc.getFrameWithDetections()
        count = count+1
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        time.sleep(0.07)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    print time.strftime("%Y-%m-%d %H:%M")

    return Response(gen(SmartCamera().start()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
