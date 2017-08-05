#https://software.intel.com/en-us/articles/opencv-at-the-edge-counting-people

#!/usr/bin/env python
from SmartCamera import SmartCamera
import cv2
import time

from flask import Flask, render_template, Response

app = Flask(__name__)

def gen(sc):
    count = 1
    while True:
        frame = sc.getFrameWidthDetections()
        count = count+1
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        time.sleep(0.1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    print time.strftime("%Y-%m-%d %H:%M")

    return Response(gen(SmartCamera().start()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
