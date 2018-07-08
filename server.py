from flask import Flask, render_template, Response
from flask_basicauth import BasicAuth

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'change-me'
app.config['BASIC_AUTH_PASSWORD'] = 'change-me'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

camera = None
def start(video_camera):
    global camera
    camera = video_camera
    app.run(host='0.0.0.0', debug=False)

@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_jpeg_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
