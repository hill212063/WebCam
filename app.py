from flask import Flask,render_template,Response,request,session,g,jsonify
from flask_mysqldb import MySQL
from flask.helpers import url_for
#from flask_socketio import SocketIO,emit
#from flask_cors import CORS
import cv2
import time
from datetime import datetime,timedelta
import imutils
from imutils.video import WebcamVideoStream
from imutils.video import FPS
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length,NumberRange
from wtforms import StringField,TextAreaField,DateField,TimeField,SubmitField,IntegerField, PasswordField
from werkzeug.utils import redirect
import os


now = datetime.now()
app=Flask(__name__)
#cors = CORS(app, resources={r"/*": {"origins": "*"}})
#socketio= SocketIO(app,cors_allowed_origins='*')
num_cams = [0,1]
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


########################   MYSQL   ##############################  
app.config['MYSQL_HOST'] = os.getenv('DATABASE_HOST')
app.config['MYSQL_USER'] = os.getenv('DATABASE_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('DATABASE_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('DATABASE_NAME')
mysql = MySQL(app)
########################   MYSQL   ##############################  

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[Length(max=20)])
    password = PasswordField("Password",validators=[Length(max=40)])
    submit = SubmitField('Login')

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=1)
    g.user = None

    if 'username' in session:
        g.user = session['username']


@app.route('/login')
def login():
    return render_template('login.html')

def gen(id):
    vs = WebcamVideoStream(src=id).start()
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=500)
        ret,buffer=cv2.imencode('.jpg',frame)
        frame=buffer.tobytes()
        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#######################################   ADMIN   #######################################  
@app.route('/admin/cameras')
def admin():
    return render_template('admin_cameras.html',num_cams=num_cams)

@app.route('/admin/cameras/<int:id>')
def video(id):
    return( Response(gen(id),mimetype='multipart/x-mixed-replace; boundary=frame'))
    
class CreateUserForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(),Length(max=50)])
    surname = StringField('surname', validators=[InputRequired(),Length(max=50)])
    password = StringField('password',validators=[InputRequired(),Length(max=40)])
    queue = DateField('queue',validators=[InputRequired()])
    queue_time = TimeField('queue_time',validators=[InputRequired()])
    pet_name = StringField('pet_name',validators=[InputRequired(),Length(max=20)])
    pet_age_year = IntegerField('pet_age_year',validators=[InputRequired(),NumberRange(min=0,max=99)])
    pet_age_month = IntegerField('pet_age_month',validators=[InputRequired(),NumberRange(min=0,max=11)])
    pet_type = StringField('pet_type',validators=[InputRequired(),Length(max=10)])
    note = TextAreaField('note')
    cam = IntegerField('cam',validators=[InputRequired(),NumberRange(min=0,max=1)])
    submit = SubmitField('submit')   

@app.route('/', methods= ['GET','POST'])
def submit():
    form = CreateUserForm()
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        pwd = form.password.data
        queue_timestamp=str(form.queue.data)+" "+str(form.queue_time.data)
        pet_name = form.pet_name.data
        pet_age = str(form.pet_age_year.data)+":"+str(form.pet_age_month.data)
        pet_type = form.pet_type.data
        note = form.note.data
        cam = form.cam.data
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO `%s` ( `name`, `surname`, `queue_time`, `pet_name`, `pet_age`, `pet_type`,`password`,`camera_id`, `note`)
        VALUES ('%s','%s','%s','%s','%s','%s','%s',%s,'%s');'''
        %(os.getenv('DATABASE_TABLE_CLIENT_NAME'),name,surname,queue_timestamp,pet_name,pet_age,pet_type, pwd,cam ,note))
        mysql.connection.commit()
        cursor.close()
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@app.route('/admin/queue')
def queue():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT  name, surname, queue_time,status,pet_name,pet_age,pet_type,camera_id,note FROM %s'''%(os.getenv('DATABASE_TABLE_CLIENT_NAME')))
    mysql.connection.commit()
    data = cursor.fetchall()
    cursor.close()
    return render_template('admin_queue.html',table=data)
#######################################   ADMIN   #######################################  


#######################################   user   ########################################
@app.route('/user/camera/<int:id>')
def user_video(id):
    return( Response(gen(id),mimetype='multipart/x-mixed-replace; boundary=frame'))
#######################################   user   ########################################



if __name__=="__main__":
    app.run(debug=True)

