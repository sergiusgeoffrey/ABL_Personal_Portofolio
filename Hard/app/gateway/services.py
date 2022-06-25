from fileinput import filename
from turtle import title
from flask import Blueprint, render_template, redirect, request, session, jsonify, current_app, url_for, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flaskext.mysql import MySQL
import uuid, logging, os
import pymysql

accepted_extension = {'pdf'}
filepath = 'files/papers'
#MySQL
mysql = MySQL(cursorclass=pymysql.cursors.DictCursor) 

def blueprint(conn):
    blueprint = Blueprint("student_paper_storage",__name__,template_folder="templates/",url_prefix='/user')
    
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in accepted_extension
    
    @blueprint.route("/login", methods=["POST", "GET"])
    def Login():
        if request.method == "POST":
            _email = request.form['email']
            _password = request.form['password']
            if _email and _password:
                cursor = conn.cursor()
                sql = "SELECT * FROM user WHERE email = '{}'".format(_email)
                cursor.execute(sql)
                rows = cursor.fetchone()
                if rows is None:
                    return '<h2>No Email Found</h2>'
                else:
                    if check_password_hash(pwhash=rows['password'], password=_password):
                        session['key'] = uuid.uuid1()
                        session['name'] = rows['name']
                        session['id'] = rows['id']
                        return redirect("/user")
                    else:
                        return '<h2>Wrong Password</h2>'                
            else:
                return '<h2>No Input</h2>'
        return render_template("login.html")

    @blueprint.route("/register", methods=["POST", "GET"])
    def Register():
        if request.method == "POST":
            _name = request.form['name']
            _id = request.form['id']
            _email = request.form['email']
            _password = request.form['password']
            # current_app.logger.info(request.form['email'])
            
            if _email and _password and _name and _id:
                cursor = conn.cursor()
                sql = "SELECT * FROM user WHERE email = '{}'".format(_email)
                cursor.execute(sql)
                if cursor.rowcount > 0:
                    return '<h2>Email Already Exists</h2>'
                else:
                    _hashedpassword = generate_password_hash(_password)
                    sql = "INSERT INTO user VALUES ('{}', '{}', '{}', '{}')".format(_id,_name,_email,_hashedpassword)
                    try:
                        cursor.execute(sql)
                        conn.commit()
                    except Exception as e:
                        current_app.logger.info("Failed To Insert" + str(e))
                        
                    cursor.close()
                    return redirect("/user")    
            else:
                return '<h2>Empty Fields Found</h2>'
            
        return render_template("register.html")

    @blueprint.route("/")
    def Index():
        return render_template('index.html')

    @blueprint.route("/logout")
    def Logout():
        session.pop('key', None)
        return redirect("/")
        
    @blueprint.route("/upload", methods=["POST", "GET"])
    def Upload():
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                _abs = request.form['abstract']
                _title = request.form['title']
                filename = secure_filename(file.filename)
                cursor = conn.cursor()
                sql = "INSERT INTO paper VALUES ('{}', '{}', '{}', '{}')".format(session['id'],_title,filename,_abs)
                try:
                    cursor.execute(sql)
                    conn.commit()
                except Exception as e:
                    current_app.logger.info("Failed To Insert" + str(e))
                cursor.close()
                    
                file.save(os.path.join(current_app.root_path,filepath, filename))
                current_app.logger.info(os.path.join(current_app.root_path,filepath, filename))
                return '<h2>id_uploader : {} Uploaded new file</h2>'.format(session['id'])
        return render_template("upload_paper.html")


    @blueprint.route('/<name>', methods=["POST", "GET"])
    def PaperCheck(name):
        if request.method == 'POST':
            return redirect(url_for('student_paper_storage.Download', name=name))
        current_app.logger.info(os.path.join(current_app.root_path,filepath, name))
        cursor = conn.cursor()
        sql = "SELECT * FROM paper WHERE path = '{}'".format(name)
        cursor.execute(sql)
        if cursor.rowcount > 0:
            rows = cursor.fetchone()
            return render_template("paper_display.html",title= rows['title'], abstract=rows['abstract'], name=name )    
        return '<h2>FILE NOT AVAILABLE</h2>'
    
    @blueprint.route('/download/<name>')
    def Download(name):
        filename = secure_filename(name)
        cursor = conn.cursor()
        sql = "SELECT * FROM paper WHERE path = '{}'".format(filename)
        cursor.execute(sql)
        if cursor.rowcount > 0:
            rows = cursor.fetchone()
            if rows['id_uploader'] == session['id']:
                return send_from_directory(os.path.join(current_app.root_path,filepath), filename)
            else:
                return '<h2>id_uploader: {} Different User detected</h2>'.format(rows['id_uploader'])
        return '<h2>FILE NOT AVAILABLE</h2>'
    return blueprint