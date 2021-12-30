from flask import Flask,render_template,Response,request,session,g,jsonify,redirect
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
#from flask_wtf import FlaskForm
#from wtforms.validators import InputRequired, Length,NumberRange
#from wtforms import StringField,TextAreaField,DateField,TimeField,SubmitField,IntegerField, PasswordField
from flask_qrcode import QRcode
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
@app.route('/admin/chk_cam', methods= ['GET'])
def check_cam_busy():
    cam={}
    for i in num_cams:
        cam[str(i)]=False
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT camera_id FROM `%s` WHERE `status`='Wait' '''%(os.getenv('DATABASE_TABLE_CLIENT_NAME')))
    mysql.connection.commit()
    data = cursor.fetchall()
    cursor.close()
    for i in data:
        key = str(i[0])
        cam[key]=True
    return jsonify(cam)

def check_cam_busy_invidual(cam_id):
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT camera_id FROM `%s` WHERE `status`='Wait' AND `camera_id`='%s' '''%(os.getenv('DATABASE_TABLE_CLIENT_NAME'),cam_id))
    mysql.connection.commit()
    data = cursor.fetchall()
    cursor.close()
    if(data): return True
    else: return False

@app.route('/admin/cameras')
def admin_cameras():
    return render_template('admin_cameras.html',num_cams=num_cams)

@app.route('/admin/cameras/<int:id>')
def video(id):
    return( Response(gen(id),mimetype='multipart/x-mixed-replace; boundary=frame'))

@app.route('/', methods= ['GET','POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        pwd = request.form['password']
        queue_timestamp=request.form['queue']
        pet_name = request.form['pet_name']
        pet_age = str(request.form['pet_age_year'])+':'+str(request.form['pet_age_month']) 
        pet_type = request.form['pet_type']
        cam = request.form['cam_id']
        if(check_cam_busy_invidual(cam)):
            flash("This camera is Busy!!")
            return render_template('admin_dashboard.html',num_cams=num_cams)
        note = request.form['note']
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO `%s` ( `name`, `surname`, `queue_time`, `pet_name`, `pet_age`, `pet_type`,`password`,`camera_id`, `note`)
        VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s');'''
        %(os.getenv('DATABASE_TABLE_CLIENT_NAME'),name,surname,queue_timestamp,pet_name,pet_age,pet_type, pwd,cam ,note))
        mysql.connection.commit()
        cursor.close()
    return render_template('admin_dashboard.html',num_cams=num_cams)


@app.route('/admin/queue', methods= ['GET','POST'])
def queue():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT  id,name, surname, queue_time,status,pet_name,pet_age,pet_type,camera_id,note FROM `%s`'''%(os.getenv('DATABASE_TABLE_CLIENT_NAME')))
    mysql.connection.commit()
    data = cursor.fetchall()
    cursor.close()
    return render_template('admin_queue.html',table=data,num_cams=num_cams)


@app.route('/admin/queue/update',methods = ['GET', 'POST'])
def update_table():
    if request.method == 'POST':
        row_id=request.form['id']
        name = request.form['name']
        surname=request.form['surname']
        queue_timestamp = request.form['queue']
        pet_name = request.form['pet_name']
        pet_age = str(request.form['pet_age_year'])+':'+str(request.form['pet_age_month']) 
        pet_type = request.form['pet_type']
        note = request.form['note']
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE `%s` SET `name`='%s',`surname`='%s',`queue_time`='%s',
        `pet_name`='%s',`pet_age`='%s',`pet_type`='%s',`note`='%s' WHERE `id`='%s' '''
        %(os.getenv('DATABASE_TABLE_CLIENT_NAME'),name,surname,queue_timestamp,pet_name,pet_age,pet_type ,note,row_id))
        mysql.connection.commit()
        cursor.close()
    return redirect(url_for('queue'))

@app.route('/admin/queue/delete/<id>/',methods = ['GET', 'POST'])
def delete_table(id):
    print("Hello")
    cursor = mysql.connection.cursor()
    cursor.execute('''DELETE FROM `%s` WHERE `id`='%s' '''%(os.getenv('DATABASE_TABLE_CLIENT_NAME'),id))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('queue'))
#######################################   ADMIN   #######################################  


#######################################   user   ########################################
@app.route('/user/camera/<int:id>')
def user_video(id):
    return( Response(gen(id),mimetype='multipart/x-mixed-replace; boundary=frame'))
#######################################   user   ########################################



if __name__=="__main__":
    app.run(debug=True)

