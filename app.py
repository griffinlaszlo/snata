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

	# recent_snap = db.Column(db.String(50))
	# top3_snappers = db.Column(db.String(100))
	# most_received = db.Column(db.Text())
	# most_sent = db.Column(db.Text())

	media_types = db.Column(db.Text())
	top10_text = db.Column(db.Text())
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
@login_required
def testmap():

		with open('uploads/json/location_history.json', encoding="utf8") as loc_json:
			file = json.load(loc_json)
			coordinates = []		
			for point in file["Location History"]:
				x = (point["Latitude, Longitude"].split(" ")[0], point["Latitude, Longitude"].split(" ")[4])
				coordinates.append(x)

			# delete any duplicate coordinates
			coordinates = list(dict.fromkeys(coordinates))

			# delete coordinates that are within 100 meters of each other
			for x in coordinates:
				for y in coordinates:
					if x == y:
						coordinates.remove(y)
				

			start_coords = (41.71, -86.24)
			map = folium.Map(location=start_coords, tiles="Stamen Toner", zoom_start=3)
			for coord in coordinates:
				folium.Marker( location=[ coord[0], coord[1] ], fill_color='#43d9de', radius=8 ).add_to( map )
			return map._repr_html_()
			return render_template('testmap.html', map=map._repr_html_())





@app.route('/site', methods=['GET', 'POST'])
@login_required
def site():
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
									second += ' PM'
								elif int(hour) < 12:
									second += ' AM'
								month = months[int(month) - 1]
								ct = month + " " + day + ", " + year + " at exactly " + hour + ":" + minute + ":" + second

					if (key == 'Engagement'):
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
			# most_sent = ""
			media_types = ""
			top10_text = ""
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
			user.first_memory_string =  first_memory_string

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

	return render_template('site.html')


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
	try:
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
		engagement_string = post[0]['engagement'].split(",")

		first_friend = post[0]['first_friend'].split(",")
		first5_friends = post[0]['first5_friends'].split(",")
		story_array_string = post[0]['story_array'].split(",")

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

		conn.close()

		return render_template('query.html', post=post, recent_snaps=recent_snap, freq_locs=freq_locs, top3_snappers=top3_snappers, 
		most_received=most_received_list, media_types=media_types_list, top10_text=top10_text_list, first_friend_name= first_friend_name, 
		first_friend_username= first_friend_username, first5_friends=first5_array, story_string_list=story_string_list, story_array=story_array, 
		breakdown_list=breakdown_list, engagement_list=engagement_list, data=media_dict)
	except:
		error = "Sorry! We couldn't find your zip file please upload a new one"
		return render_template('site.html', error=error)

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
