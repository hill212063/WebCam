from flask import Flask,render_template,Response,request,session,jsonify,redirect,send_file,flash
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
from flask_mail import Mail, Message
#import qrcode
#from io import BytesIO
import os


now = datetime.now()
app=Flask(__name__)
QRcode(app)
#cors = CORS(app, resources={r"/*": {"origins": "*"}})
#socketio= SocketIO(app,cors_allowed_origins='*')
num_cams = [0,1] #ใช้ได้จริง 0,1
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


########################   MAIL   ##############################  
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
########################   MAIL   ##############################  a
########################   MYSQL   ##############################  
app.config['MYSQL_HOST'] = os.getenv('DATABASE_HOST')
app.config['MYSQL_USER'] = os.getenv('DATABASE_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('DATABASE_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('DATABASE_NAME')
mysql = MySQL(app)
########################   MYSQL   ##############################  


@app.before_request
def before_request():
    #session.permanent = True
    #app.permanent_session_lifetime = timedelta(seconds=10)
    if 'username' not in session:
     session['username']= None
     if 'role' not in session:
        session['role']= None
     if 'cam_id' not in session:
        session['cam_id']= None
@app.route('/')
def index():
    return render_template('index.html',user = session['username'], role = session['role'])

@app.route('/login', methods = ["GET","POST"])
def login():
    msg = ''
    if ((request.method == 'POST') and ('username' in request.form) and ('password' in request.form)):
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM `%s` WHERE `username` = '%s' AND `password` = '%s' '''%(os.getenv('DATABASE_TABLE_ADMIN_NAME'),username,password))
        account = cursor.fetchone()
        if (not account):
            cursor.execute('''SELECT * FROM `%s` WHERE `name` = '%s' AND `password` = '%s' AND `status`='Wait' '''%(os.getenv('DATABASE_TABLE_CLIENT_NAME'),username,password))
            account = cursor.fetchone()
        mysql.connect.commit()
        cursor.close()
        print(account)
        if account != None:
            #name and username live in the same index from diferrent table
            session['username'] = account[1]
            if account[-1]!='admin':
                session['role'] = 'user'
            else:
                session['role'] = account[-1]
            if session['role'] == 'admin':
                return redirect(url_for('submit'))
            elif session['role'] == 'user':
                session['cam_id'] = account[10]
                return redirect(url_for('user_camera'))
        else:
            print("hello")
            flash("Invalid username or password")
    if session['role']=='admin':
        return redirect(url_for('submit'))
    elif session['role']=='user':
        return redirect(url_for('user_camera'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    session.pop('role',None)
    session.pop('cam_id',None)
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    return render_template('profile.html',user = session['username'], role = session['role'])

@app.route('/about', methods = ["GET","POST"])
def about():
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        message = request.form['message']
        msg = Message(name,sender=email, recipients=["04076@pccl.ac.th"])
        msg.body = message + "from " + email
        mail.send(msg)
        flash('Success email has sent.')
        return redirect(url_for('about'))
    return render_template('about.html',user = session['username'], role = session['role'])

@app.route('/contactprofile')
def contactprofile():
    return render_template('contactprofile.html',user = session['username'], role = session['role'])

@app.route('/contactprofile_2')
def contactprofile_2():
    return render_template('contactprofile_2.html',user = session['username'], role = session['role'])

@app.route('/contactprofile_3')
def contactprofile_3():
    return render_template('contactprofile_3.html',user = session['username'], role = session['role'])

def gen(id):
    vs = WebcamVideoStream(src=id).start()
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=500)
        ret,buffer=cv2.imencode('.jpg',frame)
        frame=buffer.tobytes()
        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/queue')
def client_queue():
    now = datetime.now()
    today = now.strftime("%d/%m/%Y")
    return render_template('client_queue.html',today=today,user = session['username'], role = session['role'])

@app.route('/queue/gen', methods= ['GET'])
def client_queue_gen():
    now = datetime.now()
    today = now.strftime("%Y-%m-%d 00:00:00")
    tomorrow = (now+timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT  name, surname, queue_time,pet_name,pet_age,pet_type,camera_id FROM `%s` 
    WHERE `queue_time` >= '%s' AND `queue_time` < '%s' AND `status`='Wait'    '''
    %(os.getenv('DATABASE_TABLE_CLIENT_NAME'),today,tomorrow))
    mysql.connection.commit()
    data = cursor.fetchall()
    data = list(data)
    for i in range(len(data)):
        data[i] = list(data[i])
        data[i][2]=data[i][2].strftime("%H:%M")
        petage = str(data[i][4]).split(":")
        data[i][4] = petage[0] + ' years '+petage[1]+' months '

    print(data)
    cursor.close()
    return jsonify(data)

#######################################   ADMIN   #######################################  
@app.route('/admin/chk_cam', methods= ['GET'])
def check_cam_busy():
    if session['role'] !='admin' :
        return redirect(url_for('login'))
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
    if(data): 
        return True
    else: 
        return False

@app.route('/admin/cameras')
def admin_cameras():
    if session['role'] !='admin' :
        return redirect(url_for('login'))
    return render_template('admin_cameras.html',num_cams=num_cams)

@app.route('/admin/cameras/<int:id>')
def video(id):
    return( Response(gen(id),mimetype='multipart/x-mixed-replace; boundary=frame'))

@app.route('/admin', methods= ['GET','POST'])
def submit():
    if session['role'] !='admin' :
        return redirect(url_for('login'))
    if request.method == 'POST':
        cam = request.form['cam_id']
        if(check_cam_busy_invidual(cam)):
            flash("This camera is Busy!")
            return render_template('admin_dashboard.html',num_cams=num_cams)
        name = request.form['name']
        surname = request.form['surname']
        pwd = request.form['password']
        queue_timestamp=request.form['queue']
        pet_name = request.form['pet_name']
        pet_age = str(request.form['pet_age_year'])+':'+str(request.form['pet_age_month']) 
        pet_type = request.form['pet_type']
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
    if session['role'] !='admin' :
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT  id,name, surname, queue_time,status,pet_name,pet_age,pet_type,camera_id,note FROM `%s`'''%(os.getenv('DATABASE_TABLE_CLIENT_NAME')))
    mysql.connection.commit()
    data = cursor.fetchall()
    cursor.close()
    return render_template('admin_queue.html',table=data,num_cams=num_cams)


@app.route('/admin/queue/update',methods = ['GET', 'POST'])
def update_table():
    if session['role'] !='admin' :
        return redirect(url_for('login'))
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

@app.route('/admin/queue/delete/<int:id>/',methods = ['GET', 'POST'])
def delete_row_table(id):
    if session['role'] !='admin' :
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor()
    cursor.execute('''DELETE FROM `%s` WHERE `id`='%s' '''%(os.getenv('DATABASE_TABLE_CLIENT_NAME'),id))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('queue'))
#######################################   ADMIN   #######################################  


#######################################   user   ########################################
@app.route('/user/camera')
def user_camera():
    if session['role'] !='user' :
        return redirect(url_for('login'))
    cam_id = session['cam_id']
    return render_template('user_cam.html',cam_id=cam_id,user = session['username'])


@app.route('/user/camera/cam')
def user_video():
    if session['role'] !='user' :
        return redirect(url_for('login'))
    cam_id = session['cam_id']
    return( Response(gen(int(cam_id)),mimetype='multipart/x-mixed-replace; boundary=frame'))

#######################################   user   ########################################


if __name__=="__main__":
    app.run(debug=True)

