# convert unzipped json files to sql to insert into database
import json
import sqlite3

connection = sqlite3.connect('../instance/site.db')
cursor = connection.cursor()
cursor.execute('Create Table if not exists snap_friends (username varchar(30) primary key not null, name varchar(30), date varchar(100), method_added varchar(50))')

friend_data = json.load(open('../json/friends.json'))
sql_columns = ['username', 'name', 'date', 'method_added']
columns = ["Username", "Display Name", "Creation Timestamp", "Last Modified Timestamp", "Source"]
query = "insert into friends values (?, ?, ?, ?, ?)"
months = months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
homies = []
for key, value in friend_data.items():
    print(key)
    if key == 'Friends':
        for friend in value:
            homie = {}
            for key, value in friend.items():
                if key == 'Username':
                    homie['username'] = value
                if key == 'Display Name':
                    homie['name'] = value
                if key == 'Source':
                    homie['method_added'] = value
                
                if key == 'Creation Timestamp':
                    year, month, day = value.split('-')
                    day = day.split(' ')[0]
                    hour, minute, second = value.split(' ')[1].split(':')
                    if int(hour) >= 12:
                        hour = str(int(hour) - 12)
                        second += ' PM'
                    elif int(hour) < 12:
                        second += ' AM'
                    month = months[int(month) - 1]
                    # print(f'you became friends with {friend["Username"]} on {month} {day}, {year}')
                    homie['date'] = value.split(' ')[0]
            homies.append(homie)
        print(homies)
        for homie in homies:
            cursor.execute('insert into snap_friends values (?, ?, ?, ?)', [homie['username'], homie['name'], homie['date'], homie['method_added']])  
        cursor.commit()
# for row in friend_data:
#     keys = tuple(row[c] for c in columns)