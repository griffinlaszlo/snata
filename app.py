from flask import Flask, request, url_for, redirect, render_template

app = Flask(__name__, template_folder='template')

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
