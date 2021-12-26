from flask import Flask,render_template,Response,request
from flask_mysqldb import MySQL
import cv2
import time
import uuid
from datetime import datetime
import imutils
from imutils.video import WebcamVideoStream
from imutils.video import FPS
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,DateField,TimeField,SubmitField,IntegerField
from wtforms.validators import InputRequired,Length,NumberRange
import os



app=Flask(__name__)
num_cams = [0,1]
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


#MYSQL
app.config['MYSQL_HOST'] = os.getenv('DATABASE_HOST')
app.config['MYSQL_USER'] = os.getenv('DATABASE_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('DATABASE_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('DATABASE_NAME')
mysql = MySQL(app)




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
@app.route('/admin/cameras')
def admin():
    return render_template('admin_cameras.html',num_cams=num_cams)

@app.route('/admin/cameras/<int:id>')
def video(id):
    return( Response(gen(id),mimetype='multipart/x-mixed-replace; boundary=frame'))
    

class CreateUserForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(),Length(max=50)])
    surname = StringField('surname', validators=[InputRequired(),Length(max=50)])
    queue = DateField('queue',validators=[InputRequired()])
    queue_time = TimeField('queue_time',validators=[InputRequired()])
    pet_name = StringField('pet_name',validators=[InputRequired(),Length(max=20)])
    pet_age = IntegerField('pet_age',validators=[InputRequired(),NumberRange(min=0,max=999)])
    pet_type = StringField('pet_type',validators=[InputRequired(),Length(max=10)])
    note = TextAreaField('note')
    submit = SubmitField('submit')   

@app.route('/', methods= ['GET','POST'])
def submit():
    form = CreateUserForm()
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        queue_timestamp=str(form.queue.data)+" "+str(form.queue_time.data)
        pet_name = form.pet_name.data
        pet_age = form.pet_age.data
        pet_type = form.pet_type.data
        note = form.note.data
        token = uuid.uuid4()
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO `%s` ( `name`, `surname`, `queue_time`, `pet_name`, `pet_age`, `pet_type`, `note`, `token`)
        VALUES ('%s','%s','%s','%s','%s','%s','%s','%s');'''
        %(os.getenv('DATABASE_TABLE_NAME'),name,surname,queue_timestamp,pet_name,pet_age,pet_type,note,token))
        mysql.connection.commit()
        cursor.close()
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)

@app.route('/admin/queue')
def queue():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT  name, surname, queue_time,status,pet_name,pet_age,pet_type,note FROM %s'''%(os.getenv('DATABASE_TABLE_NAME')))
    mysql.connection.commit()
    data = cursor.fetchall()
    cursor.close()
    return render_template('queue_manager.html',table=data)

if __name__=="__main__":
    app.run(debug=True)
