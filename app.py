import sqlite3
from flask import Flask, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from zipfile import ZipFile
import os
import json

app = Flask(__name__, template_folder='template')
app.debug = True

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['ZIP_UPLOAD_EXTENSION'] = ['.zip']
app.config['UPLOAD_PATH'] = 'uploads'
 
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

# Settings for migrations
migrate = Migrate(app, db)

# Models go here
class Users(db.Model):
	id = db.Column(db.Integer, unique=True, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	filename = db.Column(db.String(50))
	data = db.Column(db.LargeBinary)

	def __repr__(self):
		return f'ID : {self.id}, Name : {self.username}'

class Location(db.Model):
	id = db.Column(db.Integer, unique=True, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	filename = db.Column(db.String(50))
	data = db.Column(db.PickleType)

	def __repr__(self):
		return f'ID : {self.id}, Name : {self.username}'

class Friends(db.Model):
	id = db.Column(db.Integer, unique=True, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	filename = db.Column(db.String(50))
	data = db.Column(db.PickleType)

	def __repr__(self):
		return f'ID : {self.id}, Name : {self.username}'

class ChatHistory(db.Model):
	id = db.Column(db.Integer, unique=True, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	filename = db.Column(db.String(50))
	data = db.Column(db.PickleType)

	def __repr__(self):
		return f'ID : {self.id}, Name : {self.username}'

class Account(db.Model):
	id = db.Column(db.Integer, unique=True, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	filename = db.Column(db.String(50))
	data = db.Column(db.PickleType)

	def __repr__(self):
		return f'ID : {self.id}, Name : {self.username}'

@app.route('/', methods=['GET', 'POST'])
def site():
	if request.method == 'POST':
		file = request.files['data_zip_file']

		user = Users(username="new_user_26", filename=file.filename, data=file.read())
		if user.filename != "":
			with ZipFile(file, 'r') as zip:
				zip.extractall('uploads')

			with open('uploads/json/location_history.json', encoding="utf8") as json_file:
				loc = json.load(json_file)
			location = Location(username="new_user_26", filename="location_history.json", data=loc)

			with open('uploads/json/friends.json', encoding="utf8") as json_file:
				frien = json.load(json_file)
			friends = Friends(username="new_user_26", filename='friends.json', data=frien)

			with open('uploads/json/chat_history.json', encoding="utf8") as json_file:
				chat = json.load(json_file)
			chat_history = ChatHistory(username="new_user_26", filename='chat_history.json', data=chat)

			with open('uploads/json/account.json', encoding="utf8") as json_file:
				acct = json.load(json_file)
			account = Account(username="new_user_26", filename='account', data=acct)

			db.session.add(user)
			db.session.add(location)
			db.session.add(friends)
			db.session.add(chat_history)
			db.session.add(account)
			db.session.commit()

			# conn = get_db_connection()
			# cursor = conn.cursor()
			# post = cursor.execute('SELECT username FROM Users WHERE username = "new_user_15"').fetchall()
			# print(post[0]['username'])
			# conn.close()

			return redirect(url_for('query'))

	return render_template('site.html')

@app.route('/query', methods=['GET', 'POST'])
def query():
	conn = get_db_connection()
	cursor = conn.cursor()
	post = cursor.execute('SELECT * FROM Users WHERE username = "new_user_26"').fetchall()
	conn.close()

	return render_template('query.html', post=post)

def get_db_connection():
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "instance/site.db")
	conn = sqlite3.connect(db_path)
	conn.row_factory = sqlite3.Row
	return conn

@app.route('/homePage', methods=['GET', 'POST'])
def homePage():
	# conn = get_db_connection()
	# post = conn.execute('SELECT * FROM Users').fetchall()
	# conn.close()
	#if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
		#return redirect(url_for('site'))

    # show the form, it wasn't submitted
	return render_template('homePage.html')

@app.route('/instructions', methods=['GET', 'POST'])
def instructions():
	if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
		return redirect(url_for('site'))

    # show the form, it wasn't submitted
	return render_template('instructions.html')

# FUNCTION TO GET THE ZIP FILE
# @app.route("/",methods=["GET"])
# def page_name_get(): 
#     return """<form action="." method="post" enctype=multipart/form-data>
#         <input type="file" accept="application/zip" name="data_zip_file" accept="application/zip" required>
#          <button type="submit">Send zip file!</button>
#         </form>"""

# @app.route("/",methods=["POST"])
# def page_name_post():
#     file = request.files['data_zip_file'] 
#     file_like_object = file.stream._file  
#     zipfile_ob = zipfile.ZipFile(file_like_object)
#     file_names = zipfile_ob.namelist()
#     # Filter names to only include the filetype that you want:
#     file_names = [file_name for file_name in file_names if file_name.endswith(".txt")]
#     files = [(zipfile_ob.open(name).read(),name) for name in file_names]
#     return str(files)

@app.route('/add', methods=['POST'])
def upload_file():
	uploaded_file = request.form.get("data_zip_file")
	if upload_file.filename != '':
		file_ext = os.path.splitext(uploaded_file.filename)[1]
		if file_ext not in app.config['UPLOAD_EXTENSIONS']:
			os.abort(400)
		uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], upload_file.filename))
		user = Users(username="test_user")

	return redirect(url_for('site'))

if __name__ == '__main__':
    app.run()
