from flask import Flask, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate

app = Flask(__name__, template_folder='template')
app.debug = True

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
 
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

# Settings for migrations
migrate = Migrate(app, db)

# Models go here
class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)

	def __repr__(self):
		return f'ID : {self.id}, Name : {self.username}'

@app.route('/')
def site():
	return render_template('site.html')

@app.route('/homePage', methods=['GET', 'POST'])
def homePage():
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

if __name__ == '__main__':
    app.run()
