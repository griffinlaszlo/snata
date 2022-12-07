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
	creation_time = db.Column(db.String(50))
	recent_location = db.Column(db.String(50))
	frequent_locations = db.Column(db.Text())
	recent_snap = db.Column(db.String(50))
	top3_snappers = db.Column(db.String(100))
	most_received = db.Column(db.Text())
	# most_sent = db.Column(db.Text())
	media_types = db.Column(db.Text())
	top10_text = db.Column(db.Text())

	breakdown = db.Column(db.Text())
    engagement = db.Column(db.Text())
    num_of_interests = db.Column(db.Integer())

	name_changes =  db.Column(db.Text())

	link_to_memory = db.Column(db.Text())
	first_memory_string =  db.Column(db.Text())

	total_subs = db.Column(db.Integer())
	stories = db.Column(db.Integer())
	publishers = db.Column(db.Integer())
	public_users = db.Column(db.Integer())

	
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
	your_first_friend = db.Column(db.Text())

	def __repr__(self):
		return f'ID : {self.id}, Name : {self.username}'

class ChatHistory(db.Model):
	id = db.Column(db.Integer, unique=True, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	filename = db.Column(db.String(50))
	data = db.Column(db.PickleType)


	total_snaps_sent = db.Column(db.Integer())
	total_snaps_received = db.Column(db.Integer())
	total_snaps_saved = db.Column(db.Integer())
	text_snaps = db.Column(db.Integer())
	media_snaps = db.Column(db.Integer())
	note_snaps = db.Column(db.Integer())
	share_snaps = db.Column(db.Integer())

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

		if file.filename != "":
			with ZipFile(file, 'r') as zip:
				zip.extractall('uploads')
			# create a new username in the database
			db_username = "Grifff"

			# from the user_profile.json grab creation time
			months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
			with open('uploads/json/user_profile.json', encoding="utf8") as user_json:
				user_profile = json.load(user_json)
				for key, value in user_profile.items():
					if (key == 'App Profile'):
						for key, value in value.items():
							if (key == 'Creation Time'):
								year, month, day = value.split('-')
								day = day.split(' ')[0]
								hour, minute, second = value.split(' ')[1].split(':')
								if int(hour) >= 12:
									hour = str(int(hour) - 12)
									second += ' PM'
								elif int(hour) < 12:
									second += ' AM'
								month = months[int(month) - 1]
								ct = month + " " + day + ", " + year + " at exactly " + hour + ":" + minute + ":" + second


				def user_profile_info(file):

                    breakdown = "Breakdown of Time Spent on App\n"
                    for i in file["Breakdown of Time Spent on App"]:
                        breakdown += i + "\n"

                    engagement = "Engagement\n"
                    for i in file["Engagement"]:
                        engagement += f"{i['Event']}, {i['Occurences']}\n"

                    num_of_interest_categories = len(file["Interest Categories"])

                    return breakdown, engagement, num_of_interest_categories

                breakdown, engagement, num_of_interest_categories = user_profile_info(user_profile)

			with open('uploads/json/memories_profile.json', encoding="utf8") as memories_json:
				def first_memory(file):

					FILE = open('../mydata_1669823359244/json/memories_history.json')
					file = json.load(FILE)
					link_to_memory = file["Saved Media"][-1]["Download Link"]

					return link_to_memory, f"Your first memory was taken at {file['Saved Media'][-1]['Date']}, it was a {file['Saved Media'][-1]['Media Type']}"
					
				link_to_memory, first_memory_string = first_memory(memories_json)

			with open('uploads/json/subscriptions.json', encoding="utf8") as subscriptions_json:
				def num_of_subscriptions(file):

					public_users = len(file["Public Users"])
					publishers = len(file["Public Users"])
					stories = len(file["Stories"])
					total_subs = stories + public_users + publishers

					return total_subs, stories, publishers, public_users
				
				total_subs, stories, publishers, public_users = num_of_subscriptions(subscriptions_json)

			
			# latest and frequent locations
			with open('uploads/json/location_history.json', encoding="utf8") as loc_json:
				loc_history = json.load(loc_json)
				for key, value in loc_history.items():
					if (key == 'Latest Location'):
						city = value[0]['City'].capitalize()
						region = value[0]['Region'].upper()
						country = value[0]['Country'].upper()
						recent_location = city + ", " + region + " in " + country
					elif (key == 'Frequent Locations'):
						freq_loc = []
						for location in value:
							city = location['City'].split(" ")
							city_string = ""
							for term in city:
								city_string = city_string + term.capitalize() + " "

							freq_loc.append(city_string)
							freq_loc.append(location['Country'].upper())
							freq_loc.append(location['Region'].upper())
						freq_loc_string = ""
						i = 1
						for loc in freq_loc:
							if (i % 3 == 2):
								freq_loc_string = freq_loc_string + loc + ", "
							if (i % 3 == 1):
								freq_loc_string = freq_loc_string + loc + " in "
							if (i % 3 == 0):
								freq_loc_string = freq_loc_string + loc + " ; "
							i+=1
				
				
				
			# 3 most recent received snaps
			# do 3 people you snap the most next
			iter = 0
			recent_snap = []
			with open('uploads/json/snap_history.json', encoding="utf8") as snap_json:
				snap_history = json.load(snap_json)
				top3_dict = {}
				for key, value in snap_history.items():
					# loop thru value
					if (key == 'Received Snap History'):
						for val in value:
							if (iter < 3):
								recent_snap.append(val['From'])
								iter += 1
							if (not val['From'] in top3_dict):
								top3_dict[val['From']] = 1
							else:
								top3_dict[val['From']] += 1
				recent_snap_string = ""
				for snap in recent_snap:
					recent_snap_string = recent_snap_string + snap + ", "
				recent_snap_string = recent_snap_string[:-2]
				sorted_dict = sorted(top3_dict.items(), key=lambda x:x[1], reverse=True)
				converted_dict = dict(sorted_dict)
				i = 0
				top3_string = ""
				for username, value in converted_dict.items():
					if (i < 5):
						top3_string = top3_string + username + "  " + str(value) + ", "
						i += 1
				top3_string = top3_string[:-2]

			most_received = ""
			# most_sent = ""
			media_types = ""
			top10_text = ""
			with open('uploads/json/chat_history.json', encoding="utf8") as chat_json:
				chat_history = json.load(chat_json)
				for key, value in chat_history.items():
					if key == 'Received Saved Chat History':
						received = {}
						media = {}
						text = {}
						for n in value:
							for k, v in n.items():
								if k == 'From':
									# append v to received dict with count
									received[v] = received.get(v, 0) + 1
								elif k == 'Media Type':
									media[v] = media.get(v, 0) + 1
								elif k == 'Text':
									text[v] = text.get(v, 0) + 1
						# print()
						# print('Top 5 Received Saved Chat History:')
						# print()

						for k, v in sorted(received.items(), key=lambda x: x[1], reverse=True)[:10]:
							most_received = most_received + k + ": " + str(v) + ", "

						# rank media types by count

						# print('Media Types:')

						for k, v in sorted(media.items(), key=lambda x: x[1], reverse=True):
							media_types = media_types + k + ": " + str(v) + ", "

						# print('Top 10 Text Sayings:')

						count=0
						for k, v in sorted(text.items(), key=lambda x: x[1], reverse=True):
							if k != '':
								count += 1
								top10_text = top10_text + k + ": " + str(v) + ", "
							if count == 10:
								break
			
			user = Users(username=db_username, snap_username=snap_username, snap_email=snap_email, snap_phone=snap_phone, filename=file.filename, creation_time=ct, 
                recent_location=recent_location, frequent_locations=freq_loc_string, recent_snap=recent_snap_string, top3_snappers=top3_string, most_received=most_received, 
                media_types=media_types, top10_text=top10_text, story_string=story_string, engagement=engagement, num_of_interests=num_of_interests, breakdown=breakdown, 
				 name_changes = name_changes, first_memory_string = first_memory_string, link_to_memory = link_to_memory, total_subs = total_subs, stories = stories, publishers = publishers, public_users = public_users)



			with open('uploads/json/location_history.json', encoding="utf8") as json_file:
				loc = json.load(json_file)


			location = Location(username=db_username, filename="location_history.json", data=loc)

			with open('uploads/json/friends.json', encoding="utf8") as json_file:
				frien = json.load(json_file)


				def first_friend(file):

			
			
					the_min = [int(file["Friends"][0]["Creation Timestamp"][0:4]), int(file["Friends"][0]["Creation Timestamp"][5:7]), int(file["Friends"][0]["Creation Timestamp"][8:10]),  int(file["Friends"][0]["Creation Timestamp"][11:13]),  int(file["Friends"][0]["Creation Timestamp"][14:16]), int(file["Friends"][0]["Creation Timestamp"][17:19])]
					the_min_username = file["Friends"][0]["Username"]
					#print(the_min)
					for i in file["Friends"]:
						count = 0
						current = [int(i["Creation Timestamp"][0:4]), int(i["Creation Timestamp"][5:7]), int(i["Creation Timestamp"][8:10]), int(i["Creation Timestamp"][11:13]),  int(i["Creation Timestamp"][14:16]), int(i["Creation Timestamp"][17:19])]
						#print(current)
						
						for k, val in enumerate(current):
							if current[k] <= the_min[k]:
								count += 1
								continue
							else:
								break
						if count == 6:
							the_min = current
							the_min_username = i["Username"]
							the_min_time = i["Creation Timestamp"]
					
					return f"{the_min_username} was your friend. You added them back on {the_min_time}"

				your_first_friend = first_friend(frien)





			friends = Friends(username=db_username, filename='friends.json', data=frien, your_first_friend = your_first_friend)

			with open('uploads/json/chat_history.json', encoding="utf8") as json_file:
				chat = json.load(json_file)
				def total_snaps(file):

					snaps_received_saved = len(file["Received Saved Chat History"])
					snaps_received_unsaved = len(file["Received Unsaved Chat History"])
					total_snaps_received = snaps_received_unsaved + snaps_received_saved
					snaps_sent_saved = len(file["Sent Saved Chat History"])
					snaps_sent_unsaved = len(file["Sent Unsaved Chat History"])
					total_snaps_sent = snaps_received_unsaved + snaps_received_saved
					total_snaps_saved = snaps_received_saved + snaps_sent_saved
					text_snaps = 0
					media_snaps = 0
					share_snaps = 0
					note_snaps = 0


					for i in file["Received Saved Chat History"]:
						if i["Media Type"] == "TEXT":
							text_snaps += 1
						elif i["Media Type"] == "MEDIA":
							note_snaps += 1
						elif i["Media Type"] == "NOTE":
							note_snaps += 1
						elif i["Media Type"] == "SHARE":
							share_snaps += 1


					for i in file["Received Unsaved Chat History"]:
						if i["Media Type"] == "TEXT":
							text_snaps += 1
						elif i["Media Type"] == "MEDIA":
							note_snaps += 1
						elif i["Media Type"] == "NOTE":
							note_snaps += 1
						elif i["Media Type"] == "SHARE":
							share_snaps += 1

					for i in file["Sent Unsaved Chat History"]:
						if i["Media Type"] == "TEXT":
							text_snaps += 1
						elif i["Media Type"] == "MEDIA":
							note_snaps += 1
						elif i["Media Type"] == "NOTE":
							note_snaps += 1
						elif i["Media Type"] == "SHARE":
							share_snaps += 1

					for i in file["Sent Saved Chat History"]:
						if i["Media Type"] == "TEXT":
							text_snaps += 1
						elif i["Media Type"] == "MEDIA":
							note_snaps += 1
						elif i["Media Type"] == "NOTE":
							note_snaps += 1
						elif i["Media Type"] == "SHARE":
							share_snaps += 1

					return total_snaps_sent, total_snaps_received, total_snaps_saved, text_snaps, media_snaps, note_snaps, share_snaps

				total_snaps_sent, total_snaps_received, total_snaps_saved, text_snaps, media_snaps, note_snaps, share_snaps = total_snaps(chat)

			chat_history = ChatHistory(username=db_username, filename='chat_history.json', data=chat, total_snaps_sent = total_snaps_sent, total_snaps_received = total_snaps_received,
							 total_snaps_saved = total_snaps_saved, text_snaps = text_snaps, media_snaps = media_snaps, note_snaps = note_snaps, share_snaps=share_snaps,)

			with open('uploads/json/account.json', encoding="utf8") as json_file:
				acct = json.load(json_file)
			account = Account(username=db_username, filename='account', data=acct)
			
			with open('uploads/json/account_history.json', encoding="utf8") as json_file:
				acct_history = json.load(json_file)
				def display_name_changes(file):

					name_changes = "You had a name change on:"
					for i in file["Display Name Change"]:
						name_changes += f"{[i['Date']}, {i['Display Name']}"

    				return name_changes
				name_changes  = display_name_changes(acct_history)

			db.session.add(user)
			db.session.add(location)
			db.session.add(friends)
			db.session.add(chat_history)
			db.session.add(account)
			db.session.commit()

			return redirect(url_for('query'))

	return render_template('site.html')

@app.route('/query', methods=['GET', 'POST'])
def query():
	conn = get_db_connection()
	cursor = conn.cursor()
	post = cursor.execute('SELECT * FROM Users WHERE username = "Grifff"').fetchall()
	recent_snaps = post[0]['recent_snap'].split(",")
	recent_locs = post[0]['frequent_locations'].split(";")
	top3_snaps = post[0]['top3_snappers'].split(",")
	most_received = post[0]['most_received'].split(",")
	media_types = post[0]['media_types'].split(",")
	top10_text = post[0]['top10_text'].split(",")


	recent_snap = []
	for snap in recent_snaps:
		recent_snap.append(snap)
	freq_locs = []
	for loc in recent_locs:
		freq_locs.append(loc)
	top3_snappers = []
	for snapper in top3_snaps:
		top3_snappers.append(snapper)
	most_received_list = []
	for received in most_received:
		most_received_list.append(received)
	media_types_list = []
	for media in media_types:
		media_types_list.append(media)
	top10_text_list = []
	for text in top10_text:
		top10_text_list.append(text)

	conn.close()

	return render_template('query.html', post=post, recent_snaps=recent_snap, freq_locs=freq_locs, top3_snappers=top3_snappers, most_received=most_received_list, media_types=media_types_list, top10_text=top10_text_list)

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
