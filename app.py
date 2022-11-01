from flask import Flask, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
import zipfile
import os

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

@app.route('/', methods=['GET', 'POST'])
def site():
	print('SITE PAGE')
	if request.method == 'POST':
		file = request.files['data_zip_file']

		user = Users(username="test_user", filename=file.filename, data=file.read())
		db.session.add(user)
		db.session.commit()

		return f'Uploaded: {file.filename}'
	return render_template('site.html')

@app.route('/homePage', methods=['GET', 'POST'])
def homePage():
	print('HELLO')
	if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
		return redirect(url_for('site'))

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
