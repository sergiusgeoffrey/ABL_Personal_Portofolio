import json
from flask import Flask, render_template, redirect, session
from flask_session import Session
import redis

app = Flask(__name__,template_folder="templates/")

if __name__ == "__main__":
    app.run(debug=True)

app.config["SESSION_PERMANENT"] = False
app.config['SESSION_USE_SIGNER'] = True
app.config["SESSION_TYPE"] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url('redis://redis:6379')
app.secret_key = 'Secret_Key'
app.config['UPLOAD_FOLDER'] = 'files'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'student_papers'
app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_PORT'] = 3306

from .gateway.services import mysql, blueprint
mysql.init_app(app) 
conn = mysql.connect()

from .gateway import services

app.register_blueprint(blueprint(conn))

Session(app)
app.logger.info(app.url_map)

@app.route("/")
def index():
    return redirect ("/user/login")


