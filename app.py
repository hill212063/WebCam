from flask import Flask,render_template,Response
import cv2
import time


import imutils
from imutils.video import WebcamVideoStream
from imutils.video import FPS


from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TimeField
from wtforms.validators import DataRequired

from flask_wtf.csrf import CSRFProtect
#import os
#SECRET_KEY = os.urandom(32)
#app.config['SECRET_KEY'] = SECRET_KEY


app=Flask(__name__)
num_cams = [0,1]
csrf = CSRFProtect(app)


class CreateUserForm(FlaskForm):
    fname = StringField('fname', validators=[DataRequired()])
    lname = StringField('lname', validators=[DataRequired()])
    time = TimeField('receive time',validators=[DataRequired()])


def gen(id):
    vs = WebcamVideoStream(src=id).start()
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=500)
        ret,buffer=cv2.imencode('.jpg',frame)
        frame=buffer.tobytes()
        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#ADMIN


@app.route('/admin')
def admin():
    return render_template('admin.html',num_cams=num_cams)

@app.route('/admin/<int:id>')
def video(id):
    return( Response(gen(id),mimetype='multipart/x-mixed-replace; boundary=frame'))
    
@app.route('/', methods=['GET', 'POST'])
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return "<h1>Success</h1>"
    return render_template('index.html', form=form)

if __name__=="__main__":
    app.run(threaded=True)
    csrf.init_app(app)