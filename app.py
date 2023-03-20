import sqlite3
from flask import Flask, request, url_for, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_migrate import Migrate, migrate
from zipfile import ZipFile
import os
import json
import folium
import random
from collections import defaultdict


app = Flask(__name__, template_folder='template')
app.debug = True

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

app.config['ZIP_UPLOAD_EXTENSION'] = ['.zip']
app.config['UPLOAD_PATH'] = 'uploads'
 
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

# create instance for password encryption model
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Settings for migrations
migrate = Migrate(app, db)

# Models go here
class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, unique=True, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(40), nullable=False)
	snap_username = db.Column(db.String(30))
	snap_email = db.Column(db.String(50))
	snap_phone = db.Column(db.String(15))
	filename = db.Column(db.String(50))
	creation_time = db.Column(db.String(50))
	recent_location = db.Column(db.String(50))
	frequent_locations = db.Column(db.Text())
	random_location = db.Column(db.Text())

	# recent_snap = db.Column(db.String(50))
	# top3_snappers = db.Column(db.String(100))
	# most_received = db.Column(db.Text())
	# most_sent = db.Column(db.Text())

	media_types = db.Column(db.Text())
	top10_text = db.Column(db.Text())
	sent_top10_text = db.Column(db.Text())
	sent_breakdown = db.Column(db.Text())
	received_top10_text = db.Column(db.Text())
	received_breakdown = db.Column(db.Text())
	story_string = db.Column(db.Text())
	top5story_string = db.Column(db.Text())
	
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

	# total_snaps_sent = db.Column(db.Integer())
	# total_snaps_received = db.Column(db.Integer())
	# total_snaps_saved = db.Column(db.Integer())

	first_friend = db.Column(db.Text())
	first5_friends = db.Column(db.Text())
	story_array = db.Column(db.Text())
	#data = db.Column(db.LargeBinary) -- data=file.read()

	def __repr__(self):
		return f'ID : {self.id}, Name : {self.username}'

class Chats(db.Model):
	user_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable=False, primary_key=True)
	recent_snap = db.Column(db.String(50))
	top3_snappers = db.Column(db.String(100))
	most_received = db.Column(db.Text())
	total_snaps_sent = db.Column(db.Integer())
	total_snaps_received = db.Column(db.Integer())
	total_snaps_saved = db.Column(db.Integer())
	sent_received_ratio = db.Column(db.Integer())
	received_sent_ratio = db.Column(db.Integer())

class Engagement(db.Model):
	users_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable=False, primary_key=True)
	opened_app = db.Column(db.Integer)
	discover_stories = db.Column(db.Integer)
	snaps_to_story = db.Column(db.Integer)
	total_snaps_viewed = db.Column(db.Integer)
	snaps_sent = db.Column(db.Integer)
	snaps_viewed = db.Column(db.Integer)
	chats_sent = db.Column(db.Integer)
	chats_viewed = db.Column(db.Integer)
	discover_editions = db.Column(db.Integer)
	discover_snaps = db.Column(db.Integer)
	direct_snaps_viewed = db.Column(db.Integer)
	direct_snaps_created = db.Column(db.Integer)
	geofilter_snaps = db.Column(db.Integer)
	geofilter_story = db.Column(db.Integer)
	geolens_snaps = db.Column(db.Integer)
	geofilter_used = db.Column(db.Integer)
	geofilter_swipes = db.Column(db.Integer)

# class Location(db.Model):
# 	id = db.Column(db.Integer, unique=True, primary_key=True)
# 	username = db.Column(db.String(20), unique=True, nullable=False)
# 	filename = db.Column(db.String(50))
# 	data = db.Column(db.PickleType)

# 	def __repr__(self):
# 		return f'ID : {self.id}, Name : {self.username}'

class SignupForm(FlaskForm):
	username = StringField(validators=[InputRequired(), Length(
	min=4, max=20)], render_kw={"placeholder": "Username"})
	password = PasswordField(validators=[InputRequired(), Length(
	min=4, max=20)], render_kw={"placeholder": "Password"})
	submit = SubmitField("Sign Up")

	def validate_username(self, username):
		existing_user_username = Users.query.filter_by(
			username=username.data).first()
		if existing_user_username:
			raise ValidationError(
				"That username already exists. Please choose another.")

class LoginForm(FlaskForm):
	username = StringField(validators=[InputRequired(), Length(
	min=4, max=20)], render_kw={"placeholder": "Username"})
	password = PasswordField(validators=[InputRequired(), Length(
	min=4, max=20)], render_kw={"placeholder": "Password"})
	submit = SubmitField("Login")





# SITE FUNCTIONS app route matches the url bar




@app.route('/testmap', methods=['GET', 'POST'])
def testmap():

		with open('uploads/json/location_history.json', encoding="utf8") as loc_json:
			file = json.load(loc_json)
			dict2 = {
			"Longitude": '',
			"Latitude": '',
			"Statement": '',
			}

			coordinates = []		
			months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
			statement_dict = defaultdict(list)
			for point in file["Location History"]:
				x = (point["Latitude, Longitude"].split(" ")[0], point["Latitude, Longitude"].split(" ")[4])
				date = point["Time"].split(" ")[0]
				time = point["Time"].split(" ")[1]
				month = date.split("/")[1]
				month = months[int(month) - 1]
				day = date.split("/")[2]
				year = date.split("/")[0]
				date = month + " " + day + ", " + year
				statement = f'Your location was recorded at {time} on {date}'
				dict2["Longitude"] == x[0]
				dict2["Latitude"] == x[1]
				dict2["Statement"] == statement
				longstr = x[0]
				latstr = x[1]
				longstr = longstr[:len(longstr)-2]
				latstr = latstr[:len(latstr)-2]
				temp = {
					"Longitude": longstr,
					"Latitude": latstr,
				}

				if temp not in coordinates:
					coordinates.append(temp)

				tempkey = f'{longstr} {latstr}'
				statement_dict[tempkey].append(statement)

			for x in coordinates:
				tempkey = f'{x["Longitude"]} {x["Latitude"]}'

				
			start_coords = (41.71, -86.24)
			map = folium.Map(location=start_coords, tiles="Stamen Toner", zoom_start=3)

			for x in coordinates:
				tempkey = f'{x["Longitude"]} {x["Latitude"]}'
				html=f"""
        		<p> {statement_dict[tempkey][0]}</p>
        		
				"""
				iframe = folium.IFrame(html=html, width=420, height=40)
				popup = folium.Popup(iframe, max_width=2650)
				folium.Marker(location=[ x["Longitude"], x["Latitude"] ], popup=popup, fill_color='#43d9de', radius=8 ).add_to( map )


			return map._repr_html_()
			return render_template('testmap.html', map=map._repr_html_())



@app.route('/site', methods=['GET', 'POST'])
@login_required
def site():
	conn = get_db_connection()
	cursor = conn.cursor()
	post = cursor.execute(f'SELECT * FROM Users JOIN Chats ON Users.id=Chats.user_id JOIN Engagement ON Chats.user_id=Engagement.users_id WHERE username = "{current_user.username}"').fetchall()
	conn.close()
	if request.method == 'POST':
		file = request.files['data_zip_file']

		if file.filename != "":
			with ZipFile(file, 'r') as zip:
				zip.extractall('uploads')
			# create a new username in the database
			db_username = current_user.username

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
									second += ' pm'
								elif int(hour) < 12:
									second += ' am'
								month = months[int(month) - 1]
								ct = month + " " + day + ", " + year + " at exactly " + hour + ":" + minute + ":" + second

					if (key == 'Engagement'):
						geofilter_used = ""
						snaps_to_story = ""
						for n in value:
							event = n["Event"]
							occurrences = n["Occurrences"]
							if event == 'Application Opens':
								opened_app = occurrences
            				    #print('In the last month or two, you have...\n...opened the app ' + str(occurrences) + ' times')
							if event == 'Story Views':
								discover_stories = occurrences
            				    #print('...viewed ' + str(occurrences) + ' Discover Stories.')
							if event == 'Snaps Posted to Story':
									snaps_to_story = occurrences
            				    #print('...posted ' + str(occurrences) + ' Snaps to your Story.')
							if event == 'Snaps Viewed in a Story':
								total_snaps_viewed = occurrences
            				    #print('...viewed ' + str(occurrences) + ' Snaps in a Story.')
							if event == 'Snap Views':
								snaps_viewed = occurrences
            				    #print('...viewed ' + str(occurrences) + ' Snaps.')
							if event == 'Snap Sends':
								snaps_sent = occurrences
            				    #print('...sent ' + str(occurrences) + ' Snaps.')
							if event == 'Chats Sent':
								chats_sent = occurrences
            				    #print('...sent ' + str(occurrences) + ' Chats.')
							if event == 'Chats Viewed':
								chats_viewed = occurrences
            				    #print('...viewed ' + str(occurrences) + ' Chats.')
							if event == 'Discover Editions Viewed':
								discover_editions = occurrences
            				    #print('...viewed ' + str(occurrences) + ' Discover Editions.')
							if event == 'Discover Snap Views':
								discover_snaps = occurrences
            				    #print('...viewed ' + str(occurrences) + ' Discover Snaps.')
							if event == 'Direct Snaps Created':
								direct_snaps_created = occurrences
            				    #print('...created ' + str(occurrences) + ' Direct Snaps.')
							if event == 'Direct Snaps Viewed':
								direct_snaps_viewed = occurrences
            				    #print('...viewed ' + str(occurrences) + ' Direct Snaps.')
							if event == 'Geofilter Snap Sends':
								geofilter_snaps = occurrences
            				    #print('...sent ' + str(occurrences) + ' Geofilter Snaps.')
							if event == 'Geofilter Story Snaps Viewed':
								geofilter_story = occurrences
            				    #print('...viewed ' + str(occurrences) + ' Geofilter Story Snaps.')
							if event == 'Geolens Swipes':
								geolens_snaps = occurrences
            				    #print('...swiped ' + str(occurrences) + ' Geolens Snaps.')
							if event == 'Geofilter Snaps Posted to Story':
								geofilter_used = occurrences

            				    #print('...posted ' + str(occurrences) + ' Geofilter Snaps to your Story.')
							if event == 'Geofilter Swipes':
								geofilter_swipes = occurrences
            				    #print('...swiped ' + str(occurrences) + ' Geofilter Snaps.')

				def user_profile_info(file):
					
					breakdown = "Breakdown of Time Spent on App,\n"
					for i in file["Breakdown of Time Spent on App"]:
						breakdown += i + ",\n"
						
					engagement = "Engagement\n"
					for i in file["Engagement"]:
						engagement += f"{i['Event']}, {i['Occurrences']}\n"
						
					num_of_interest_categories = len(file["Interest Categories"])
					return breakdown, engagement, num_of_interest_categories
					
				breakdown, engagement, num_of_interest_categories = user_profile_info(user_profile)

			# latest and frequent locations
			with open('uploads/json/location_history.json', encoding="utf8") as loc_json:
				months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
				loc_history = json.load(loc_json)
				for key, value in loc_history.items():
					if (key == 'Latest Location'):
						city = value[0]['City'].split(" ")
						city_str = ""
						for string in city:
							city_str = city_str + string.capitalize() + " "
						region = value[0]['Region'].upper()
						country = value[0]['Country'].upper()
						recent_location = city_str.rstrip() + ", " + region + " in " + country
					elif (key == 'Frequent Locations'):
						freq_loc = []
						for location in value:
							city = location['City'].split(" ")
							city_string = ""
							for term in city:
								city_string = city_string + term.capitalize() + " "

							freq_loc.append(city_string.rstrip())
							freq_loc.append(location['Region'].upper())
							freq_loc.append(location['Country'].upper())
						freq_loc_string = ""
						i = 1
						for loc in freq_loc:
							if (i % 3 == 2):
								freq_loc_string = freq_loc_string + loc + " in "
							if (i % 3 == 1):
								freq_loc_string = freq_loc_string + loc + ", "
							if (i % 3 == 0):
								freq_loc_string = freq_loc_string + loc + " ; "
							i+=1
					elif key == 'Businesses and public places you may have visited':
						dictionary = {
    				    	'date': "",
    				    	'name': "",
    					}
						random_location = ""
						for n in value:
							for x,y in n.items():
								if x == 'Name':
									dictionary['name'] = y
								if x == 'Date':
									y = y.split("-")
									year = y[0]
									month = months[int(y[1])-1]
									day = y[2]
									dictionary['date'] = month + " " + day + ", " + year
									
								random_location = random_location + dictionary['name'] + " on " + dictionary['date'] + ";"
						
			# 3 most recent received snaps
			# do 3 people you snap the most next
			iter = 0
			recent_snap = []

			with open('uploads/json/memories_history.json', encoding="utf8") as memories_json:

				#def first_memory(file):
				json_memories = json.load(memories_json)
				the_list = json_memories["Saved Media"]
				link_to_memory = the_list[-1]["Download Link"]
				first_memory_string = f"Your first memory was taken at {json_memories['Saved Media'][-1]['Date']}, it was a {json_memories['Saved Media'][-1]['Media Type']}"
		
			with open('uploads/json/subscriptions.json', encoding="utf8") as subscriptions_json:
				#def num_of_subscriptions(file):
				json_subscriptions = json.load(subscriptions_json)
				public_users = len(json_subscriptions["Public Users"])
				publishers = len(json_subscriptions["Public Users"])
				stories = len(json_subscriptions["Stories"])
				total_subs = stories + public_users + publishers
				
				#total_subs, stories, publishers, public_users = num_of_subscriptions(subscriptions_json)

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
			media_types = ""
			sent_top10_text = ""
			top10_text=""
			sent_breakdown=""
			received_top10_text=""
			received_breakdown=""

			with open('uploads/json/chat_history.json', encoding="utf8") as chat_json:
				chat_history = json.load(chat_json)
				def total_snaps(file): 

					snaps_received_saved = len(file["Received Saved Chat History"])
					snaps_received_unsaved = len(file["Received Unsaved Chat History"])
					total_snaps_received = snaps_received_unsaved + snaps_received_saved
					snaps_sent_saved = len(file["Sent Saved Chat History"])
					snaps_sent_unsaved = len(file["Sent Unsaved Chat History"])
					total_snaps_sent = snaps_sent_unsaved + snaps_sent_saved
					total_snaps_saved = snaps_received_saved + snaps_sent_saved
					sent_received_ratio = round((total_snaps_sent/total_snaps_received) * 100, 2)
					received_sent_ratio = round((total_snaps_received/total_snaps_sent) * 100, 2)

					return total_snaps_sent, total_snaps_received, total_snaps_saved, sent_received_ratio, received_sent_ratio

				total_snaps_sent, total_snaps_received, total_snaps_saved, sent_received_ratio, received_sent_ratio = total_snaps(chat_history)	


				sent_saved_list = chat_history['Sent Saved Chat History']
				sent_text_dict = {}
				sent_media_dict = {}
				for i in sent_saved_list:
					if i["Media Type"] == "TEXT":
						sent_text_dict[i["Text"]] = sent_text_dict.get(i["Text"], 0) + 1
						
					sent_media_dict[i["Media Type"]] = sent_media_dict.get(i["Media Type"], 0) + 1

				#print('Top 10 Text Sayings:')
				count=0
				for k, v in sorted(sent_text_dict.items(), key=lambda x: x[1], reverse=True):
					if k != '':
						count += 1
						sent_top10_text = sent_top10_text + str(k) + " " + str(v) + "; "
						#print(k, v)
					if count == 10:
						break
				#print("Sent Media Break Down")
				#print(sent_media_dict)
				for i, j in sent_media_dict.items():
					sent_breakdown = sent_breakdown + str(i) + " " + str(j) + "; "

				received_saved_list = chat_history['Received Saved Chat History']
				received_text_dict = {}
				received_media_dict = {}
				for i in received_saved_list:
					if i["Media Type"] == "TEXT":
						received_text_dict[i["Text"]] = received_text_dict.get(i["Text"], 0) + 1
						
					received_media_dict[i["Media Type"]] = received_media_dict.get(i["Media Type"], 0) + 1

				#print('Top 10 Received Text Sayings:')
				count=0
				for k, v in sorted(received_text_dict.items(), key=lambda x: x[1], reverse=True):
					if k != '':
						count += 1
						received_top10_text = received_top10_text + str(k) + " " + str(v) + "; "
					if count == 10:
						break
				#print("Received Media Break Down")
				#print(received_media_dict)
				for i, j in received_media_dict.items():
					received_breakdown = received_breakdown + str(i) + " " + str(j) + "; "

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

						for k, v in sorted(received.items(), key=lambda x: x[1], reverse=True)[:10]:
							most_received = most_received + k + ": " + str(v) + ", "

						# rank media types by count

						for k, v in sorted(media.items(), key=lambda x: x[1], reverse=True):
							media_types = media_types + k + ": " + str(v) + ", "

						count=0
						for k, v in sorted(text.items(), key=lambda x: x[1], reverse=True):
							if k != '':
								count += 1
								top10_text = top10_text + k + ": " + str(v) + "; "
							if count == 10:
								break
			with open('uploads/json/account.json', encoding="utf8") as json_file:
				acct = json.load(json_file)
				snap_username = acct["Basic Information"]["Username"]

			with open('uploads/json/account_history.json', encoding="utf8") as json_file:
				acct_hist = json.load(json_file)
				# snap_email = acct_hist["Email Change"][0]["Email Address"]
				snap_phone = acct_hist["Mobile Number Change"][0]["Mobile Number"]
				def display_name_changes(file):

					name_changes = "You had a name change on:"
					for i in file["Display Name Change"]:
						name_changes += f"{i['Date']}, {i['Display Name']}"
						
					return name_changes	
				name_changes  = display_name_changes(acct_hist)

			with open('uploads/json/story_history.json', encoding="utf8") as json_file:
				story_hist = json.load(json_file)

				total_story_views = 0
				total_story_replies = 0
				story_count = 0
				for x in story_hist["Your Story Views"]:
					story_views = x["Story Views"]
					story_replies = x["Story Replies"]
					total_story_views = total_story_views + story_views
					total_story_replies = total_story_replies + story_replies
					story_count += 1

				if story_count <= 100:
					story_string = f"You like to keep things lowkey..., You've only posted to your story {story_count} times, Still racking up the views though!, You have {total_story_views} views across all your stories"

				elif story_count >= 100 and story_count <= 300:
					story_string = f"You could write a book with all these stories..., You've posted to your story {story_count} times, Lotta eyes on them too!, You have {total_story_views} views across all your stories"

				elif story_count >= 300 and story_count <= 500:
					story_string = f"You're a story teller!, You've posted to your story {story_count} times, Lotta eyes on them too!, You have {total_story_views} views across all your stories"

				elif story_count > 500:
					story_string = f"You're an open book!, You've posted to your story {story_count} times, with {total_story_views} total views across all your stories"

			with open('uploads/json/friends.json', encoding="utf8") as json_file:
				friends = json.load(json_file)
				min_array = []
				for i in friends["Friends"]:
					current = [int(i["Creation Timestamp"][0:4]), int(i["Creation Timestamp"][5:7]), int(i["Creation Timestamp"][8:10]), int(i["Creation Timestamp"][11:13]),  int(i["Creation Timestamp"][14:16]), int(i["Creation Timestamp"][17:19]), i["Username"], i["Display Name"]]
					min_array.append(current)

				min_array = sorted(min_array)
				first_friend = min_array[2]
				first_friend = first_friend[7] + "," + first_friend[6]
				min_array = min_array[3:7] # first two are you and teamsnap get other first 5 friends added
				first_friend_string = ""
				for friend in min_array:
					first_friend_string = first_friend_string + friend[6] + ","
				first_friend_string = first_friend_string[:-1]

			with open('uploads/json/story_history.json', encoding="utf8") as json_file:
				story_hist = json.load(json_file)

				viewer = {}
				count = 0
				for x in story_hist["Friend and Public Story Views"]:
					for key, value in x.items():
						if key == 'View':
							viewer[value] = viewer.get(value, 0) + 1

				story_array = []
				for k, v in sorted(viewer.items(), key=lambda x: x[1], reverse=True):
					if k != '' and k != 'no name':
						count += 1
						story_array.append(f"@{k}'s story {v} times")
					if count == 5:
						break
				story_array_string = ""
				for story in story_array:
					story_array_string = story_array_string + story + ","
				story_array_string = story_array_string[:-1]
					
			user = Users.query.filter_by(username=current_user.username).first()
			user.snap_username = snap_username
			user.snap_email = "dshield2@nd.edu"
			user.snap_phone = snap_phone
			user.filename = file.filename
			user.creation_time = ct
			user.recent_location = recent_location
			user.frequent_locations=freq_loc_string
			user.random_location=random_location

			# user.recent_snap=recent_snap_string
			# user.top3_snappers=top3_string
			# user.most_received=most_received 

			user.media_types=media_types
			user.top10_text=top10_text
			user.story_string=story_string

			user.breakdown = breakdown
			user.engagement = engagement
			user.num_of_interests = num_of_interest_categories
			
			user.name_changes = name_changes

			user.link_to_memory = link_to_memory
			user.first_memory_string = first_memory_string

			user.total_subs = total_subs
			user.stories = stories
			user.publishers = publishers
			user.public_users = public_users

			# user.total_snaps_sent = total_snaps_sent
			# user.total_snaps_received = total_snaps_received
			# user.total_snaps_saved = total_snaps_saved

			user.first_friend = first_friend
			user.first5_friends = first_friend_string
			user.story_array = story_array_string

			user.sent_top10_text=sent_top10_text
			user.received_top10_text=received_top10_text
			user.sent_breakdown=sent_breakdown
			user.received_breakdown=received_breakdown


			try:
				chats = Chats.query.filter_by(user_id=user.id).first()
				chats.recent_snap = recent_snap_string
				chats.top3_snappers = top3_string
				chats.most_received = most_received
				chats.total_snaps_sent = total_snaps_sent
				chats.total_snaps_received = total_snaps_received
				chats.total_snaps_saved = total_snaps_saved
				chats.sent_received_ratio = sent_received_ratio
				chats.received_sent_ratio = received_sent_ratio
			except:
				chats = Chats(
					user_id = user.id,
					recent_snap = recent_snap_string,
					top3_snappers = top3_string,
					most_received = most_received,
					total_snaps_sent = total_snaps_sent,
					total_snaps_received = total_snaps_received,
					total_snaps_saved = total_snaps_saved,
					sent_received_ratio = sent_received_ratio,
					received_sent_ratio = received_sent_ratio
				)

			try:
				engagement_table = Engagement.query.filter_by(users_id=user.id).first()
				engagement_table.opened_app = opened_app
				engagement_table.discover_stories = discover_stories
				engagement_table.snaps_to_story = snaps_to_story
				engagement_table.total_snaps_viewed = total_snaps_viewed
				engagement_table.snaps_sent = snaps_sent
				engagement_table.snaps_viewed = snaps_viewed
				engagement_table.chats_sent = chats_sent
				engagement_table.chats_viewed = chats_viewed
				engagement_table.discover_editions = discover_editions
				engagement_table.discover_snaps = discover_snaps
				engagement_table.direct_snaps_viewed = direct_snaps_viewed
				engagement_table.direct_snaps_created = direct_snaps_created
				engagement_table.geofilter_snaps = geofilter_snaps
				engagement_table.geofilter_story = geofilter_story
				engagement_table.geolens_snaps = geofilter_snaps
				engagement_table.geofilter_used = geofilter_used
				engagement_table.geofilter_swipes = geofilter_swipes
			except:
				engagement_table = Engagement(
					users_id = user.id,
					opened_app = opened_app,
					discover_stories = discover_stories,
					snaps_to_story = snaps_to_story,
					total_snaps_viewed = total_snaps_viewed,
					snaps_sent = snaps_sent,
					snaps_viewed = snaps_viewed,
					chats_sent = chats_sent,
					chats_viewed = chats_viewed,
					discover_editions = discover_editions,
					discover_snaps = discover_snaps,
					direct_snaps_viewed = direct_snaps_viewed,
					direct_snaps_created = direct_snaps_created,
					geofilter_snaps = geofilter_snaps,
					geofilter_story = geofilter_story,
					geolens_snaps = geofilter_snaps,
					geofilter_used = geofilter_used,
					geofilter_swipes = geofilter_swipes
				)

			db.session.add(user)
			db.session.add(chats)
			db.session.add(engagement_table)
			db.session.commit()
			return redirect(url_for('query'))

	return render_template('site.html', post=post)


@app.route('/loading', methods=['GET', 'POST'])
@login_required
def loading():
	if request.method == "POST":
		return redirect(url_for('query'))

	return render_template('loading.html')



@app.route('/query', methods=['GET', 'POST'])
@login_required
def query():
	error = None
	# try:
	conn = get_db_connection()
	cursor = conn.cursor()
	post = cursor.execute(f'SELECT * FROM Users JOIN Chats ON Users.id=Chats.user_id JOIN Engagement ON Chats.user_id=Engagement.users_id WHERE username = "{current_user.username}"').fetchall()
	recent_snaps = post[0]['recent_snap'].split(",")
	recent_locs = post[0]['frequent_locations'].split(";")
	top3_snaps = post[0]['top3_snappers'].split(",")
	most_received = post[0]['most_received'].split(",")
	media_types = post[0]['media_types'].split(",")
	media_dict = {}
	media_dict['Media Type'] = 'Amount Sent'
	for media in media_types:
		if ':' in media:
			split = media.split(":")
			media_dict[split[0].strip()] = int(split[1])
	top10_text = post[0]['top10_text'].split(";")
	story_string = post[0]['story_string'].split(",")

	breakdown_string = post[0]['breakdown'].split(",")
	breakdown_dict = {}
	breakdown_dict['App Feature'] = 'Percentage of Time Spent'
	for feature in breakdown_string:
		if ':' in feature:
			split = feature.split(":")
			print(float(split[1][:-1]))
			breakdown_dict[split[0].strip()] = float(split[1][:-1])
	engagement_string = post[0]['engagement'].split(",")

	first_friend = post[0]['first_friend'].split(",")
	first5_friends = post[0]['first5_friends'].split(",")
	story_array_string = post[0]['story_array'].split(",")

	random_location_string = post[0]['random_location'].split(";")

	sent_sayings = post[0]['sent_top10_text'].split(";")
	received_sayings = post[0]['received_top10_text'].split(";")
	sent_breakdown = post[0]['sent_breakdown'].split(";")
	received_breakdown = post[0]['received_breakdown'].split(";")

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
	story_string_list = []
	for string in story_string:
		story_string_list.append(string)

	breakdown_list = []
	for breakdown in breakdown_string:
		breakdown_list.append(breakdown)
	engagement_list = []
	for engagement in engagement_string:
		engagement_list.append(engagement)

	first_friend_name = first_friend[0]
	first_friend_username = first_friend[1]

	first5_array = []
	for friend in first5_friends:
		first5_array.append(friend)

	story_array = []
	for friend in story_array_string:
		story_array.append(friend)

	random_location_array = []
	for location in random_location_string:
		random_location_array.append(location)

	sent_top10_sayings = []
	for saying in sent_sayings:
		sent_top10_sayings.append(saying)

	received_top10_sayings = []
	for saying in received_sayings:
		received_top10_sayings.append(saying)

	sent_breakdowns = []
	for breakdown in sent_breakdown:
		sent_breakdowns.append(breakdown)

	received_breakdowns = []
	for breakdown in received_breakdown:
		received_breakdowns.append(breakdown)

	
	rand_int = random.randrange(len(random_location_array))


	# get location values across the database
	cursor2 = conn.cursor()
	query = cursor2.execute(f'SELECT username, creation_time FROM Users JOIN Chats ON Users.id=Chats.user_id JOIN Engagement ON Chats.user_id=Engagement.users_id').fetchall()
	creation_times = query
	sort_creation = {}
	for time in creation_times:
		sort_creation[f'{time[0]}'] = f'{time[1]}'

	conn.close()

	for key, value in sort_creation.items():
		if value[0] == " ":
			value = value[1:]
		string = value.split(" at exactly ")
		print(string[0])
		print(string[1])

	return render_template('query.html', post=post, recent_snaps=recent_snap, freq_locs=freq_locs, top3_snappers=top3_snappers, 
	most_received=most_received_list, media_types=media_types_list, top10_text=top10_text_list, first_friend_name= first_friend_name, 
	first_friend_username= first_friend_username, first5_friends=first5_array, story_string_list=story_string_list, story_array=story_array, 
	breakdown_list=breakdown_list, engagement_list=engagement_list, data=media_dict, breakdown_data=breakdown_dict, random_location=random_location_array[rand_int], 
	sent_top10_sayings=sent_top10_sayings, received_top10_sayings=received_top10_sayings, sent_breakdowns=sent_breakdowns, received_breakdowns=received_breakdowns)
# except:
	# flash("Sorry! We couldn't find your zip file please upload a new one", 'error')
	# return redirect(url_for('site'))

def get_db_connection():
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "instance/site.db")
	conn = sqlite3.connect(db_path)
	conn.row_factory = sqlite3.Row
	return conn

@app.route('/instructions', methods=['GET', 'POST'])
def instructions():
	if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
		return redirect(url_for('site'))

    # show the form, it wasn't submitted
	return render_template('instructions.html')

@app.route('/', methods=['GET', 'POST'])
def login():
	conn = get_db_connection()
	cursor = conn.cursor()
	post = cursor.execute(f'SELECT count(*) as cnt FROM Users').fetchall()
	conn.close()
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(username=form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user)
			return redirect(url_for('site'))
		else:
			flash('Username or password incorrect.', 'danger')
	return render_template('login.html', form=form, post=post[0]['cnt'])

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()

	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data)
		new_user = Users(username=form.username.data, password=hashed_password)
		db.session.add(new_user)
		db.session.commit()
		return redirect(url_for('login'))

	return render_template('signup.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
