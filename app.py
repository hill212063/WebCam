from flask import (
    Flask,
    render_template,
    Response,
    request,
    jsonify,
    redirect,
    send_file,
    flash,
    session,
)
from flask_session import Session
from flask_mysqldb import MySQL
from flask.helpers import url_for
import cv2
import time
from datetime import datetime, timedelta
import imutils
from imutils.video import WebcamVideoStream
from imutils.video import FPS
from flask_qrcode import QRcode
from flask_mail import Mail, Message
from threading import Thread
from werkzeug.utils import secure_filename
import os
import uuid
import re
from threading import Thread
import cv2

now = datetime.now()
app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
QRcode(app)
num_cams = [i for i in range(10)]


########################   MAIL   ##############################
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail = Mail(app)
########################   MAIL   ##############################
########################   MYSQL   ##############################
app.config["MYSQL_HOST"] = os.getenv("DATABASE_HOST")
app.config["MYSQL_USER"] = os.getenv("DATABASE_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("DATABASE_PASSWORD")
app.config["MYSQL_DB"] = os.getenv("DATABASE_NAME")
mysql = MySQL(app)
########################   MYSQL   ##############################


def check_officer(off):
    account = []
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT * FROM `%s` WHERE `username` = '%s' """
            % (os.getenv("DATABASE_TABLE_ADMIN_NAME"), off)
        )
        account = cursor.fetchone()
        mysql.connect.commit()
        cursor.close()
        if account == None:
            return False
        else:
            return True
    except Exception as e:
        flash(str(e))
        return False


def check_doc(dname):
    doc = []
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT * FROM `%s` WHERE `name` = '%s' """
            % (os.getenv("DATABASE_TABLE_DOC_NAME"), dname)
        )
        doc = cursor.fetchone()
        mysql.connect.commit()
        cursor.close()
        if doc == None:
            return False
        else:
            return True
    except Exception as e:
        flash(str(e))
        return False


# check user
def check_user(uname):
    account = []
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT * FROM `%s` WHERE `username` = '%s' """
            % (os.getenv("DATABASE_TABLE_USER_NAME"), uname)
        )
        account = cursor.fetchone()
        mysql.connect.commit()
        cursor.close()
        if account == None:
            return False
        else:
            return True
    except Exception as e:
        flash(str(e))
        return False


def check_owner(name_sur):
    account = []
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT name,surname FROM `%s` """
            % (os.getenv("DATABASE_TABLE_USER_NAME"))
        )
        account = cursor.fetchall()
        mysql.connect.commit()
        account = list(account)
        if len(account) == 0:
            return False
        for i in range(len(account)):
            account[i] = account[i][0] + " " + account[i][1]
        cursor.close()
        if name_sur in account:
            return True
        else:
            return False
    except Exception as e:
        flash(str(e) + "hello")
        return False


def check_user_from_name(name):
    name_sur = name.rsplit(" ", 1)
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT username FROM `%s` WHERE `name` = '%s' AND `surname` = '%s' """
            % (os.getenv("DATABASE_TABLE_USER_NAME"), name_sur[0], name_sur[1])
        )
        account = cursor.fetchone()
        mysql.connect.commit()
        cursor.close()
        if account == None:
            return False
        else:
            return account[0]
    except Exception as e:
        flash(str(e))
        return False


def check_pet(name):
    account = []
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT * FROM `%s` WHERE `pet_name` = '%s' """
            % (os.getenv("DATABASE_TABLE_PET_NAME"), name)
        )
        account = cursor.fetchone()
        mysql.connect.commit()
        cursor.close()
        if account == None:
            return False
        else:
            return True
    except Exception as e:
        flash(str(e))
        return False


# Overide the update method in WebcamVideoStream class
class webcam(WebcamVideoStream):
    def update(self):
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()
            # custom
            if not self.grabbed:
                self.stop()


@app.route("/")
def index():
    return render_template("index.html", user=session["username"], role=session["role"])


@app.route("/register", methods=["GET", "POST"])
def register():
    swal = []
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
        and "email" in request.form
        and "name" in request.form
        and "surname" in request.form
        and "tel" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        name = request.form["name"]
        surname = request.form["surname"]
        tel = request.form["tel"]
        if check_user(username):
            swal = ["Error!", "error"]
            flash("Username already exists!")
            return render_template("register.html", swal=swal)
        else:
            try:
                cursor = mysql.connection.cursor()
                cursor.execute(
                    """INSERT INTO `%s` (`username`,`password`,`name`,`surname`,`email`,`tel`)
                VALUES ('%s','%s','%s','%s','%s','%s');"""
                    % (
                        os.getenv("DATABASE_TABLE_USER_NAME"),
                        username,
                        password,
                        name,
                        surname,
                        email,
                        tel,
                    )
                )
                mysql.connection.commit()
                cursor.close()
                swal = ["Sign up success!", "success"]
                flash("You have successfully registered!")
            except Exception as e:
                swal = ["Error!", "error"]
                flash(str(e))
                return render_template("register.html", swal=swal)
    elif request.method == "POST":
        swal = ["Error!", "error"]
        flash("Please fill out the form!")
    return render_template("register.html", swal=swal)


@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    if (
        (request.method == "POST")
        and ("username" in request.form)
        and ("password" in request.form)
    ):
        username = request.form["username"]
        password = request.form["password"]
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """SELECT * FROM `%s` WHERE `username` = '%s' AND `password` = '%s' """
                % (os.getenv("DATABASE_TABLE_ADMIN_NAME"), username, password)
            )
            account = cursor.fetchone()
            if not account:
                cursor.execute(
                    """SELECT * FROM `%s` WHERE `username` = '%s' AND `password` = '%s' """
                    % (os.getenv("DATABASE_TABLE_USER_NAME"), username, password)
                )
                account = cursor.fetchone()
            mysql.connect.commit()
            cursor.close()
        except Exception as e:
            flash(str(e))
            return render_template("login.html")

        if account != None:
            # name and username live in the same index from differrent table
            session["username"] = account[1]
            if account[-1] != "admin" and account[-1] != "officer":
                session["role"] = "user"
            else:
                session["role"] = account[-1]
            if session["role"] == "officer":
                session["password"] = account[2]
                return redirect(url_for("submit"))
            elif session["role"] == "user":
                session["password"] = account[2]
                return redirect(url_for("user_profile"))
        else:
            flash("Invalid username or password")
    if session["role"] == "admin":
        return redirect(url_for("submit"))
    elif session["role"] == "officer":
        return redirect(url_for("pet_table"))
    elif session["role"] == "user":
        return redirect(url_for("user_profile"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("role", None)
    return redirect(url_for("index"))


@app.route("/profile")
def profile():
    return render_template(
        "profile.html", user=session["username"], role=session["role"]
    )


@app.route("/about", methods=["GET", "POST"])
def about():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        msg = Message(name, sender=email, recipients=[os.getenv("MAIL_USERNAME")])
        msg.body = message + "\nfrom " + email
        mail.send(msg)
        flash("Success email has sent.")
        return redirect(url_for("about"))
    return render_template("about.html", user=session["username"], role=session["role"])


def gen(id):
    vs = webcam(src=id).start()
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=500)
        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()
        yield (b"--frame\r\n" b"Content-Type: image/jpg\r\n\r\n" + frame + b"\r\n")


@app.route("/news")
def client_news():
    data = []
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT id,subject,detail,img,type FROM `%s` ORDER BY create_time DESC """
            % (os.getenv("DATABASE_TABLE_NEWS_NAME"))
        )
        mysql.connection.commit()
        data = cursor.fetchall()
        data = list(data)
        if len(data) != 0:
            for i in range(len(data)):
                data[i] = list(data[i])
        cursor.close()
    except Exception as e:
        flash(str(e))
    if session["username"]:
        return render_template(
            "client_news.html",
            table=data,
            user=session["username"],
            role=session["role"],
        )
    else:
        return render_template("client_news.html", table=data, role=session["role"])


@app.route("/news/<int:id>")
def news_gen(id):
    data = []
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT subject,detail,create_time,modified_time,img,type FROM `%s` WHERE `id`='%s' """
            % (os.getenv("DATABASE_TABLE_NEWS_NAME"), id)
        )
        mysql.connection.commit()
        data = cursor.fetchall()
        cursor.close()
    except Exception as e:
        flash(str(e))

    return render_template("news.html", table=data, role=session["role"])


@app.route("/officer/chk_cam", methods=["GET"])
def check_cam_busy():
    if session["role"] != "officer":
        return redirect(url_for("login"))
    cam = {}
    for i in num_cams:
        cam[str(i)] = False
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT camera_id FROM `%s` WHERE `status`='Wait' """
            % (os.getenv("DATABASE_TABLE_CASES_NAME"))
        )
        mysql.connection.commit()
        data = cursor.fetchall()
        cursor.close()
    except Exception as e:
        return jsonify(cam)
    for i in data:
        key = str(i[0])
        if str(i[0]) == "None":
            continue
        cam[key] = True
    return jsonify(cam)


def check_cam_busy_invidual(cam_id):
    data = []
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT camera_id FROM `%s` WHERE `status`='Wait' AND `camera_id`='%s' """
            % (os.getenv("DATABASE_TABLE_CASES_NAME"), cam_id)
        )
        mysql.connection.commit()
        data = cursor.fetchall()
        cursor.close()
    except Exception as e:
        return False
    if data:
        return True
    else:
        return False


#######################################   ADMIN   #######################################


@app.route("/admin/cameras")
def admin_cameras():
    if session["role"] != "admin":
        return redirect(url_for("login"))
    return render_template("admin_cameras.html", num_cams=num_cams)


@app.route("/admin/cameras/<int:id>")
def video(id):
    return Response(gen(id), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/admin", methods=["GET", "POST"])
def submit():
    if session["role"] != "admin":
        return redirect(url_for("login"))
    if request.method == "POST":
        username = request.form["username"]
        if check_officer(username):
            flash("This officer username has been created!")
            return redirect(url_for("submit"))
        password = request.form["password"]
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        tel = request.form["tel"]
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """INSERT INTO `%s` ( `username`,`password`,`name`, `surname`,`email`,`tel`,`role`)
            VALUES ('%s','%s','%s','%s','%s','%s','officer');"""
                % (
                    os.getenv("DATABASE_TABLE_ADMIN_NAME"),
                    username,
                    password,
                    name,
                    surname,
                    email,
                    tel,
                )
            )
            mysql.connection.commit()
            cursor.close()
        except Exception as e:
            flash(str(e))
    return render_template("admin_create_officer.html")


@app.route("/admin/officer", methods=["GET", "POST"])
def officer():
    data = []
    if session["role"] != "admin":
        return redirect(url_for("login"))
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT  id,username,password,name, surname,email,tel FROM `%s` WHERE `role`='officer' """
            % (os.getenv("DATABASE_TABLE_ADMIN_NAME"))
        )
        mysql.connection.commit()
        data = cursor.fetchall()
        cursor.close()
    except Exception as e:
        flash(str(e))
    return render_template("admin_officer.html", table=data)


@app.route("/admin/officer/delete/<int:id>/", methods=["GET", "POST"])
def delete_row_officer(id):
    if session["role"] != "admin":
        return redirect(url_for("login"))
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """DELETE FROM `%s` WHERE `id`='%s' """
            % (os.getenv("DATABASE_TABLE_ADMIN_NAME"), id)
        )
        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        flash(str(e))
    return redirect(url_for("officer"))


@app.route("/admin/officer/update", methods=["GET", "POST"])
def update_officer():
    if session["role"] != "admin":
        return redirect(url_for("login"))
    if request.method == "POST":
        row_id = request.form["id"]
        username = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        tel = request.form["tel"]
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """UPDATE `%s` SET `username`='%s',`password`='%s',`name`='%s',`surname`='%s',`email`='%s',`tel`='%s' WHERE `id`='%s' """
                % (
                    os.getenv("DATABASE_TABLE_ADMIN_NAME"),
                    username,
                    password,
                    name,
                    surname,
                    email,
                    tel,
                    row_id,
                )
            )
            mysql.connection.commit()
            cursor.close()
        except Exception as e:
            flash(str(e))
    return redirect(url_for("officer"))


@app.route("/admin/user")
def admin_user_table():
    data = []
    if session["role"] != "admin":
        return redirect(url_for("login"))
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT * FROM `%s` """ % (os.getenv("DATABASE_TABLE_USER_NAME"))
        )
        mysql.connection.commit()
        data = cursor.fetchall()
        cursor.close()
    except Exception as e:
        flash(str(e))
    return render_template("admin_user_table.html", table=data)

@app.route("/admin/user/delete/<int:id>/", methods=["GET", "POST"])
def delete_row_user(id):
    if session["role"] != "admin":
        return redirect(url_for("login"))
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
                """SELECT `username` FROM `%s` WHERE `id` = '%s'"""
                % (os.getenv("DATABASE_TABLE_USER_NAME"), id)
            )
        olduname = cursor.fetchone()
        olduname = olduname[0]
        cursor.execute(
            """DELETE FROM `%s` WHERE `id`='%s' """
            % (os.getenv("DATABASE_TABLE_USER_NAME"), id)
        )
        mysql.connection.commit()
        # pet table
        cursor.execute(
            """DELETE FROM `%s` WHERE `username`='%s' """
            % (
                os.getenv("DATABASE_TABLE_PET_NAME"),
                olduname,
            )
        )
        mysql.connection.commit()
        # cases table
        cursor.execute(
            """DELETE FROM `%s` WHERE `username`='%s' """
            % (
                os.getenv("DATABASE_TABLE_CASES_NAME"),
                olduname,
            )
        )
        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        flash(str(e))
    return redirect(url_for("admin_user_table"))

@app.route("/admin/user/update", methods=["GET", "POST"])
def update_user():
    if session["role"] != "admin":
        return redirect(url_for("login"))
    if request.method == "POST":
        row_id = request.form["id"]
        username = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        tel = request.form["tel"]
        fullname = str(name) + " " + str(surname)
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """SELECT `username` FROM `%s` WHERE `id` = '%s'"""
                % (os.getenv("DATABASE_TABLE_USER_NAME"), row_id)
            )
            olduname = cursor.fetchone()
            olduname = olduname[0]
            cursor.execute(
                """UPDATE `%s` SET `username`='%s',`password`='%s',`name`='%s',`surname`='%s',`email`='%s',`tel`='%s' WHERE `username`='%s' """
                % (
                    os.getenv("DATABASE_TABLE_USER_NAME"),
                    username,
                    password,
                    name,
                    surname,
                    email,
                    tel,
                    olduname,
                )
            )
            mysql.connection.commit()
            # pet table
            cursor.execute(
                """UPDATE `%s` SET `username`='%s',`owner`='%s' WHERE `username`='%s' """
                % (
                    os.getenv("DATABASE_TABLE_PET_NAME"),
                    username,
                    fullname,
                    olduname,
                )
            )
            mysql.connection.commit()
            # cases table
            cursor.execute(
                """UPDATE `%s` SET `username`='%s',`owner`='%s' WHERE `username`='%s' """
                % (
                    os.getenv("DATABASE_TABLE_CASES_NAME"),
                    username,
                    fullname,
                    olduname,
                )
            )
            mysql.connection.commit()
            # not update the tel to pet and case table because tel can change whatever you want
            cursor.close()
        except Exception as e:
            flash(str(e))
    return redirect(url_for("admin_user_table"))


#######################################   ADMIN   #######################################

#######################################   officer   #####################################


@app.route("/officer")
def pet_table():
    data = []
    userlist = []
    if session["role"] != "officer":
        return redirect(url_for("login"))
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT id,pet_name,pet_age,pet_type,owner,tel,username FROM `%s`"""
            % (os.getenv("DATABASE_TABLE_PET_NAME"))
        )
        mysql.connection.commit()
        data = cursor.fetchall()
        cursor.execute(
            """SELECT name,surname FROM `%s`"""
            % (os.getenv("DATABASE_TABLE_USER_NAME"))
        )
        mysql.connection.commit()
        userlist = cursor.fetchall()
        userlist = list(userlist)
        for i in range(len(userlist)):
            userlist[i] = userlist[i][0] + " " + userlist[i][1]
        data = list(data)
        cursor.close()
    except Exception as e:
        flash(str(e))
    return render_template(
        "officer_pet.html",
        table=data,
        num_cams=num_cams,
        userlist=userlist,
        user=session["username"],
    )


@app.route("/officer/pet/add", methods=["GET", "POST"])
def pet_table_add():
    if session["role"] != "officer":
        return redirect(url_for("login"))
    if request.method == "POST":
        owner = request.form["owner"]
        if not check_owner(owner):
            flash("Owner not found!")
            return redirect(url_for("pet_table"))
        tel = request.form["tel"]
        pet_name = request.form["pet_name"]
        if check_pet(pet_name):
            flash("Pet's name already exists!")
            return redirect(url_for("pet_table"))
        pet_age = (
            str(request.form["pet_age_year"]) + ":" + str(request.form["pet_age_month"])
        )
        pet_type = request.form["pet_type"]
        try:
            account = check_user_from_name(owner)
            if not account:
                flash("Username not found!")
                return redirect(url_for("pet_table"))
            cursor = mysql.connection.cursor()
            cursor.execute(
                """INSERT INTO `%s` (  `pet_name`, `pet_age`, `pet_type`,`owner`,`tel`,`username`)
            VALUES ('%s','%s','%s','%s','%s','%s');"""
                % (
                    os.getenv("DATABASE_TABLE_PET_NAME"),
                    pet_name,
                    pet_age,
                    pet_type,
                    owner,
                    tel,
                    account,
                )
            )
            mysql.connection.commit()
            cursor.close()
        except Exception as e:
            flash(str(e))
    return redirect(url_for("pet_table"))


@app.route("/officer/pet/delete/<int:id>/", methods=["GET", "POST"])
def delete_row_pet(id):
    if session["role"] != "officer":
        return redirect(url_for("login"))
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """DELETE FROM `%s` WHERE `id`='%s' """
            % (os.getenv("DATABASE_TABLE_PET_NAME"), id)
        )
        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        flash(str(e))
    return redirect(url_for("pet_table"))


@app.route("/officer/pet/update", methods=["GET", "POST"])
def update_pet():
    if session["role"] != "officer":
        return redirect(url_for("login"))
    if request.method == "POST":
        row_id = request.form["id"]
        owner = request.form["owner"]
        if not check_owner(owner):
            flash("Owner not found!")
            return redirect(url_for("pet_table"))
        tel = request.form["tel"]
        pet_name = request.form["pet_name"]
        if check_pet(pet_name):
            flash("Pet's name already exists!")
            return redirect(url_for("pet_table"))
        pet_age = (
            str(request.form["pet_age_year"]) + ":" + str(request.form["pet_age_month"])
        )
        pet_type = request.form["pet_type"]
        try:
            account = check_user_from_name(owner)
            if not account:
                flash("Username not found!")
                return redirect(url_for("pet_table"))
            cursor = mysql.connection.cursor()
            cursor.execute(
                """UPDATE `%s` SET `pet_name`='%s',`pet_age`='%s',`pet_type`='%s',`owner`='%s',`tel`='%s',`username`='%s' WHERE `id`='%s' """
                % (
                    os.getenv("DATABASE_TABLE_PET_NAME"),
                    pet_name,
                    pet_age,
                    pet_type,
                    owner,
                    tel,
                    account,
                    row_id,
                )
            )
            mysql.connection.commit()
            cursor.close()
        except Exception as e:
            flash(str(e))
    return redirect(url_for("pet_table"))


@app.route("/officer/cases")
def cases_table():
    data = []
    datalist = []
    userlist = []
    doclist = []
    if session["role"] != "officer":
        return redirect(url_for("login"))
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """UPDATE %s SET `status`='wait' WHERE `queue_time`> NOW();"""
            % (os.getenv("DATABASE_TABLE_CASES_NAME"))
        )
        mysql.connection.commit()
        cursor.execute(
            """SELECT `id`,`subject`,`pet_name`,`queue_time`,`status`,`camera_id`,`note`,`owner`,`username`,`doctor` FROM `%s` ORDER BY
    queue_time=NOW() DESC,
    queue_time<NOW() DESC,
    queue_time>NOW() ASC """
            % (os.getenv("DATABASE_TABLE_CASES_NAME"))  # sort by near now
        )
        mysql.connection.commit()
        data = cursor.fetchall()
        cursor.execute(
            """SELECT pet_name FROM `%s`""" % (os.getenv("DATABASE_TABLE_PET_NAME"))
        )
        mysql.connection.commit()
        datalist = cursor.fetchall()
        cursor.execute(
            """SELECT name,surname FROM `%s`"""
            % (os.getenv("DATABASE_TABLE_USER_NAME"))
        )
        mysql.connection.commit()
        userlist = cursor.fetchall()
        userlist = list(userlist)
        for i in range(len(userlist)):
            userlist[i] = userlist[i][0] + " " + userlist[i][1]
        cursor.execute(
            """SELECT name FROM `%s`""" % (os.getenv("DATABASE_TABLE_DOC_NAME"))
        )
        mysql.connection.commit()
        doclist = cursor.fetchall()
        cursor.close()
    except Exception as e:
        flash(str(e))
    return render_template(
        "officer_cases.html",
        table=data,
        num_cams=num_cams,
        datalist=datalist,
        userlist=userlist,
        doclist=doclist,
        user=session["username"],
    )


@app.route("/officer/cases/add", methods=["GET", "POST"])
def cases_table_add():
    if session["role"] != "officer":
        return redirect(url_for("login"))
    if request.method == "POST":
        cam = request.form["cam_id"]
        doc_name = request.form["doc_name"]
        # owner = request.form["owner"]
        subject = request.form["subject"]
        queue_timestamp = request.form["queue"]
        pet_name = request.form["pet_name"]
        note = request.form["note"]
        if not check_pet(pet_name):
            flash("Pet's name not found!")
            return redirect(url_for("cases_table"))
        if not check_doc(doc_name):
            flash("Doctor's name not found!")
            return redirect(url_for("cases_table"))
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """ SELECT owner,username FROM %s WHERE pet_name = '%s' """
                % (
                    os.getenv("DATABASE_TABLE_PET_NAME"),
                    pet_name,
                )
            )
            tmp = cursor.fetchone()

            if cam == "None":
                cursor.execute(
                    """INSERT INTO `%s` ( `subject`, `pet_name`,`queue_time`,`camera_id`, `note`,`owner`,`username,`doctor`)
                 VALUES ('%s','%s','%s',NULL,'%s','%s','%s','%s');"""
                    % (
                        os.getenv("DATABASE_TABLE_CASES_NAME"),
                        subject,
                        pet_name,
                        queue_timestamp,
                        note,
                        tmp[0],
                        tmp[1],
                        doc_name,
                    )
                )
            else:
                cursor.execute(
                    """INSERT INTO `%s` ( `subject`, `pet_name`,`queue_time`,`camera_id`, `note`,`owner`,`username`,`doctor`)
                VALUES ('%s','%s','%s','%s','%s','%s','%s','%s');"""
                    % (
                        os.getenv("DATABASE_TABLE_CASES_NAME"),
                        subject,
                        pet_name,
                        queue_timestamp,
                        cam,
                        note,
                        tmp[0],
                        tmp[1],
                        doc_name,
                    )
                )
            mysql.connection.commit()
            cursor.close()
        except Exception as e:
            flash(str(e))
    return redirect(url_for("cases_table"))


@app.route("/officer/cases/delete/<int:id>/", methods=["GET", "POST"])
def delete_row_cases(id):
    if session["role"] != "officer":
        return redirect(url_for("login"))
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """DELETE FROM `%s` WHERE `id`='%s' """
            % (os.getenv("DATABASE_TABLE_CASES_NAME"), id)
        )
        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        flash(str(e))
    return redirect(url_for("cases_table"))


@app.route("/officer/cases/update", methods=["GET", "POST"])
def update_cases():
    if session["role"] != "officer":
        return redirect(url_for("login"))
    if request.method == "POST":
        row_id = request.form["id"]
        subject = request.form["subject"]
        queue_timestamp = request.form["queue"]
        pet_name = request.form["pet_name"]
        note = request.form["note"]
        cam_id = request.form["cam_id_edit"]
        doc_name = request.form["doc_name"]
        # owner = request.form["owner"]
        if not check_pet(pet_name):
            flash("Pet's name not found!")
            return redirect(url_for("cases_table"))
        if not check_doc(doc_name):
            flash("Doctor's name not found!")
            return redirect(url_for("cases_table"))

        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """ SELECT owner,username FROM %s WHERE pet_name = '%s' """
                % (
                    os.getenv("DATABASE_TABLE_PET_NAME"),
                    pet_name,
                )
            )
            tmp = cursor.fetchone()
            if cam_id == "None":
                cursor.execute(
                    """UPDATE `%s` SET `subject`='%s',`pet_name`='%s',`queue_time`='%s',`camera_id`=NULL,`note`='%s',`owner`='%s',`username`='%s',`doctor`='%s' WHERE `id`='%s' """
                    % (
                        os.getenv("DATABASE_TABLE_CASES_NAME"),
                        subject,
                        pet_name,
                        queue_timestamp,
                        note,
                        tmp[0],
                        tmp[1],
                        doc_name,
                        row_id,
                    )
                )
            else:
                cursor.execute(
                    """UPDATE `%s` SET `subject`='%s',`pet_name`='%s',`queue_time`='%s',`camera_id`='%s',`note`='%s',`owner`='%s',`username`='%s',`doctor`='%s' WHERE `id`='%s' """
                    % (
                        os.getenv("DATABASE_TABLE_CASES_NAME"),
                        subject,
                        pet_name,
                        queue_timestamp,
                        cam_id,
                        note,
                        tmp[0],
                        tmp[1],
                        doc_name,
                        row_id,
                    )
                )
            mysql.connection.commit()
            cursor.close()
        except Exception as e:
            flash(str(e))
    return redirect(url_for("cases_table"))


@app.route("/officer/news")
def news_table():
    data = []

    if session["role"] != "officer":
        return redirect(url_for("login"))

    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT id,subject,detail,create_time,modified_time,img,type FROM `%s` ORDER BY create_time DESC"""
            % (os.getenv("DATABASE_TABLE_NEWS_NAME"))
        )
        mysql.connection.commit()
        data = cursor.fetchall()
        data = list(data)
        if len(data) != 0:
            for i in range(len(data)):
                data[i] = list(data[i])
        cursor.close()
    except Exception as e:
        flash(str(e))
    return render_template("officer_news.html", table=data, user=session["username"])


@app.route("/officer/news_create")
def news_create_page():
    if session["role"] != "officer":
        return redirect(url_for("login"))
    return render_template("officer_create_news.html")


@app.route("/news_edit/<int:id>", methods=["GET", "POST"])
def news_edit_page(id):
    data = []
    if session["role"] != "officer":
        return redirect(url_for("login"))
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT id,subject,detail,img,type FROM `%s` WHERE id = '%s'"""
            % (os.getenv("DATABASE_TABLE_NEWS_NAME"), id)
        )
        mysql.connection.commit()
        data = cursor.fetchall()
        data = list(data)
        if len(data) != 0:
            for i in range(len(data)):
                data[i] = list(data[i])
        cursor.close()
    except Exception as e:
        flash(str(e))
    return render_template("officer_edit_news.html", table=data)


ALLOWED_EXTENSIONS = set(
    [
        "apng",
        "avif",
        "gif",
        "ico",
        "cur",
        "jpg",
        "jpeg",
        "jfif",
        "pjpeg",
        "pjp",
        "png",
        "svg",
        "webp",
        "bmp",
        "tif",
        "tiff",
    ]
)
img_path = os.path.dirname(__file__) + "\static\imgs_news"
app.config["UPLOAD_FOLDER"] = img_path


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/officer/news/add", methods=["GET", "POST"])
def news_table_add():
    if session["role"] != "officer":
        return redirect(url_for("login"))
    if request.method == "POST":
        subject = request.form["subject"]
        detail = request.form["detail"]
        type_data = request.form["type"]
        img = ""
        if "img" not in request.files:
            flash("No file part")
            return redirect(url_for("news_table"))
        file = request.files["img"]
        if file.filename == "":
            flash("No selected file")
            return redirect(url_for("news_table"))
        if file and allowed_file(file.filename):
            filext = secure_filename(file.filename).split(".")[-1]
            filename = str(uuid.uuid4()) + "." + filext
            img = filename
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        else:
            flash("Wrong image type.")
            return redirect(url_for("news_table"))
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """INSERT INTO `%s` ( `subject`, `detail`, `img`,`type`)
            VALUES ('%s','%s','%s','%s');"""
                % (
                    os.getenv("DATABASE_TABLE_NEWS_NAME"),
                    subject,
                    detail,
                    img,
                    type_data,
                )
            )
            mysql.connection.commit()
            cursor.close()
        except Exception as e:
            flash(str(e))
    return redirect(url_for("news_table"))


@app.route("/officer/news/delete/<int:id>/", methods=["GET", "POST"])
def delete_row_news(id):
    oldimg = ""
    if session["role"] != "officer":
        return redirect(url_for("login"))
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT `img` FROM `%s` WHERE `id`='%s' """
            % (os.getenv("DATABASE_TABLE_NEWS_NAME"), id)
        )
        mysql.connection.commit()
        oldimg = cursor.fetchone()  # will be none when get nothing
        if oldimg != None:
            if os.path.exists(os.path.join(app.config["UPLOAD_FOLDER"], oldimg[0])):
                os.remove(os.path.join(app.config["UPLOAD_FOLDER"], oldimg[0]))
        cursor.execute(
            """DELETE FROM `%s` WHERE `id`='%s' """
            % (os.getenv("DATABASE_TABLE_NEWS_NAME"), id)
        )
        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        flash(str(e))
    return redirect(url_for("news_table"))


@app.route("/officer/news/update", methods=["GET", "POST"])
def update_news():
    if session["role"] != "officer":
        return redirect(url_for("login"))
    if request.method == "POST":
        row_id = request.form["id"]
        subject = request.form["subject"]
        detail = request.form["detail"]
        type_data = request.form["type"]
        oldimg = ""
        img = ""
        if "img" not in request.files:
            flash("No file part")
            return redirect(url_for("news_table"))
        file = request.files["img"]
        if file.filename != "":
            if file and allowed_file(file.filename):
                filext = secure_filename(file.filename).split(".")[-1]
                filename = str(uuid.uuid4()) + "." + filext
                img = filename
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            else:
                flash("Wrong image type.")
                return redirect(url_for("news_table"))
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """SELECT `img` FROM `%s` WHERE `id`='%s' """
                % (os.getenv("DATABASE_TABLE_NEWS_NAME"), row_id)
            )
            mysql.connection.commit()
            oldimg = cursor.fetchone()
            if img != "":
                if oldimg != None:
                    if os.path.exists(
                        os.path.join(app.config["UPLOAD_FOLDER"], oldimg[0])
                    ):
                        os.remove(os.path.join(app.config["UPLOAD_FOLDER"], oldimg[0]))
                cursor.execute(
                    """UPDATE `%s` SET `subject`='%s',`detail`='%s',`img`='%s',`type`='%s' WHERE `id`='%s' """
                    % (
                        os.getenv("DATABASE_TABLE_NEWS_NAME"),
                        subject,
                        detail,
                        img,
                        type_data,
                        row_id,
                    )
                )
            else:
                cursor.execute(
                    """UPDATE `%s` SET `subject`='%s',`detail`='%s',`type`='%s' WHERE `id`='%s' """
                    % (
                        os.getenv("DATABASE_TABLE_NEWS_NAME"),
                        subject,
                        detail,
                        type_data,
                        row_id,
                    )
                )
            mysql.connection.commit()
            cursor.close()
        except Exception as e:
            flash(str(e))
    return redirect(url_for("news_table"))


#######################################   officer   #####################################

#######################################   user   ########################################


@app.route("/user")
def user_case_list():
    data = []
    pet = []
    if session["role"] != "user":
        return redirect(url_for("login"))
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """ SELECT pet_name FROM %s WHERE username = '%s' """
            % (os.getenv("DATABASE_TABLE_PET_NAME"), session["username"])
        )
        mysql.connection.commit()
        pet = cursor.fetchall()
        for i in pet:
            for j in i:
                cursor.execute(
                    """SELECT subject,pet_name,queue_time,status,camera_id,note,doctor FROM `%s` WHERE `pet_name`='%s' AND status = 'wait' """
                    % (
                        os.getenv("DATABASE_TABLE_CASES_NAME"),
                        j,
                    )
                )
                mysql.connection.commit()
                for i in cursor.fetchall():
                    data.append(i)
                    data = list(data)
        cursor.close()
    except Exception as e:
        flash(str(e))
    return render_template("user_case_list.html", table=data, user=session["username"])


@app.route("/user/pet")
def user_pet_list():
    data = []
    if session["role"] != "user":
        return redirect(url_for("login"))
    username = session["username"]
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """ SELECT `pet_name`, `pet_age`, `pet_type`, `regis_time` FROM %s WHERE `username` = '%s' """
            % (os.getenv("DATABASE_TABLE_PET_NAME"), username)
        )
        mysql.connection.commit()
        data = cursor.fetchall()
        data = list(data)
        if len(data) != 0:
            for i in range(len(data)):
                data[i] = list(data[i])
                tmp = data[i][1].split(":")
                y = " years"
                m = " months"
                if int(tmp[0]) <= 1:
                    y = " year"
                if int(tmp[1]) <= 1:
                    m = " month"
                data[i][1] = tmp[0] + y + " " + tmp[1] + m
        cursor.close()
    except Exception as e:
        flash(str(e))
    return render_template("user_pet_list.html", table=data, user=username)


@app.route("/user/camera")
def user_cam():
    data = []
    if session["role"] != "user":
        return redirect(url_for("login"))
    username = session["username"]
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """ SELECT `id`,`subject`,`pet_name`, `queue_time`, `note`, `camera_id`,`doctor` FROM %s WHERE `username` = '%s' AND status='wait' """
            % (os.getenv("DATABASE_TABLE_CASES_NAME"), username)
        )
        mysql.connection.commit()
        data = cursor.fetchall()
        cursor.close()
    except Exception as e:
        flash(str(e))
    return render_template("user_camera.html", data=data, user=username)


@app.route("/user/camera/<int:id>")
def user_video(id):
    if session["role"] != "user":
        return redirect(url_for("login"))
    return Response(gen(id), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/user/profile")
def user_profile():
    if session["role"] != "user":
        return redirect(url_for("login"))
    data = []
    username = session["username"]
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT * FROM %s WHERE `username` = '%s' """
            % (os.getenv("DATABASE_TABLE_USER_NAME"), username)
        )
        mysql.connection.commit()
        data = cursor.fetchone()
        cursor.close()
    except Exception as e:
        flash(str(e))
    return render_template("user_profile.html", data=data, user=username)


@app.route("/user/profile/edit", methods=["GET", "POST"])
def update_profile():
    if session["role"] != "user":
        return redirect(url_for("login"))
    if request.method == "POST":
        row_id = request.form["id"]
        username = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        tel = request.form["tel"]
        fullname = str(name) + " " + str(surname)
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """UPDATE `%s` SET `username`='%s',`password`='%s',`name`='%s',`surname`='%s',`email`='%s',`tel`='%s' WHERE `id`='%s' """
                % (
                    os.getenv("DATABASE_TABLE_USER_NAME"),
                    username,
                    password,
                    name,
                    surname,
                    email,
                    tel,
                    row_id,
                )
            )
            mysql.connection.commit()
            # pet table
            cursor.execute(
                """UPDATE `%s` SET `username`='%s',`owner`='%s' WHERE `username`='%s' """
                % (
                    os.getenv("DATABASE_TABLE_PET_NAME"),
                    username,
                    fullname,
                    session["username"],
                )
            )
            mysql.connection.commit()
            # cases table
            cursor.execute(
                """UPDATE `%s` SET `username`='%s',`owner`='%s' WHERE `username`='%s' """
                % (
                    os.getenv("DATABASE_TABLE_CASES_NAME"),
                    username,
                    fullname,
                    session["username"],
                )
            )
            mysql.connection.commit()
            # not update the tel to pet and case table because tel can change whatever you want

            cursor.close()
            session["username"] = username
        except Exception as e:
            flash(str(e))
    return redirect(url_for("user_profile"))


#######################################   user   ########################################

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    cv2.destroyAllWindows()
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.before_request
def before_request():
    if "username" not in session:
        session["username"] = None
    if "role" not in session:
        session["role"] = None
    if "cam_id" not in session:
        session["cam_id"] = None
    if "password" not in session:
        session["password"] = None


@app.before_first_request
def beforeStart():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""SET GLOBAL event_scheduler = ON;""")
        mysql.connect.commit()
        cursor.execute(
            """CREATE EVENT IF NOT EXISTS statusUpdate_comp 
                        ON SCHEDULE EVERY 1 SECOND DO 
                        UPDATE %s SET `status`='complete',`camera_id`=NULL WHERE `queue_time`<= NOW();"""
            % (os.getenv("DATABASE_TABLE_CASES_NAME"))
        )
        mysql.connect.commit()
        cursor.execute(
            """CREATE EVENT IF NOT EXISTS statusUpdate_wait 
                        ON SCHEDULE EVERY 1 SECOND DO 
                        UPDATE %s SET `status`='wait' WHERE `queue_time`> NOW();"""
            % (os.getenv("DATABASE_TABLE_CASES_NAME"))
        )
        mysql.connect.commit()
        cursor.close()
    except Exception as e:
        flash(str(e))
        return False


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
