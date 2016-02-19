import psycopg2
import sys

from secret import mysecretpassword


conn = psycopg2.connect(database='players', user='postgres',
						password=mysecretpassword)

cur = conn.cursor()

def route():
	"""Ask the user how he wants to interact with the db"""
	while True:
		decision = input("\nHello there! How do you want to interact with the "
						 "database? You can [S]earch it, [A]dd users "
						 "[D]isplay top performers or [Q]uit "
						 "Type a letter in the bracket. ").lower()
		if decision == 's':
			find_player()
		elif decision == 'a':
			add_players()
		elif decision == 'd':
			top_performers()
		elif decision == 'q':
			print("Thanks for querying!")
			sys.exit()
		else:
			print("Im sorry I did not understand")
			route()

def find_player():
	"""Search the db by player name"""
	print("Here is the current list of players in the db...\n")
	print(display_player_names())
	player_search = input("Which player do you want to search for? ")
	cur.execute("select * from player_stats where player_name = (%s);", (player_search,))
	row = cur.fetchall()
	print(row)
	return row

def display_player_names():
	"""Display player names so user knows who is in the db"""
	cur.execute("""SELECT player_name FROM player_stats""")
	rows = cur.fetchall()
	players = map(lambda x: x, rows)
	return list(players)

def add_players():
	"""Allow the user to add players to the db"""
	player = input("Enter Player Name: ")
	rec = input("Enter his receptions for the season: ")
	yds = input("Enter his totaly yards: ")
	yds_rec = input("Enter his average yards per reception: ")
	longest = input("Enter his longest yards for on catch ")
	td = input("Enter how many touchdowns he got: ")
	data = [player, rec, yds, yds_rec, longest, td]
	cur.executemany("""INSERT INTO player_stats VALUES
				(DEFAULT, %s, %s, %s, %s, %s, %s)""", (data,))
	return "Your player has been added!"

def top_performers():
	"""Allow user to search for top players in each category"""
	choice = input("See which players performed the best in each category, "
		  	  "You can search [R]ec, [Y]ds, [YR]ds_rec, [L]ong or [TD] "
		  	  "Type the letter(s) in the brackets for the listings\n ").lower()
	if choice == 'r':
		print(list_rec())
	elif choice == 'y':
		print(list_yds())
	elif choice == 'yr':
		print(list_yds_rec())
	elif choice == 'l':
		print(list_long())
	elif choice == 'td':
		print(list_td())

def list_rec():
	"""List the receptions by top performer"""
	cur.execute("""SELECT * FROM player_stats ORDER BY rec DESC""")
	return grab_data()

def list_yds():
	"""List the yards by top performer"""
	cur.execute("""SELECT * FROM player_stats ORDER BY yds DESC""")
	return grab_data()

def list_yds_rec():
	"""List the yards per reception by top performer"""
	cur.execute("""SELECT * FROM player_stats ORDER BY yds_rec DESC""")
	return grab_data()

def list_long():
	"""List the longest reception by the top performer"""
	cur.execute("""SELECT * FROM player_stats ORDER BY long DESC""")
	return grab_data()

def list_td():
	"""List the most tds by top performer"""
	cur.execute("""SELECT * FROM player_stats ORDER BY td DESC""")
	return grab_data()

def grab_data():
	"""Grab data from db"""
	rows = cur.fetchall()
	return rows

def update_record():
	"""Allow a user to update a record"""
	print("Alright first lets find who you want to update.")
	record = find_player()
	cur.execute("""SELECT ID FROM player_stats WHERE player_name = (%s)""", (record[0][1],))
	choice = input("\nDo you want to update his "
				   "[P]layer name, [R]ec, [Y]ds, [YR]ds_rec, "
				   "[L]ong, [TD] "
				   "Type a letter(s) in the bracket ").lower()
	if choice == 'p':
		update_name = input("What name do you want to change too? ")
		print(update_player(record, update_name))
	elif choice == 'r':
		update_reception = int(input("How many receptions are you changing it too? "))
		print(update_rec(record, update_reception))
	elif choice == 'y':
		update_yards = int(input("How many yards are you changing it too? "))
		print(update_yds(record, update_yards))
	elif choice == 'yr':
		update_yards_rec = float(input("How many yards/rec are you changing it too? "))
		print(update_yds_rec(record, update_yards_rec))
	elif choice == 'l':
		update_longest = int(input("What are you changing his longest run too? "))
		print(update_long(record, update_longest))
	elif choice == 'td':
		update_tds = int(input("How many tds are you changing it too? "))
		print(update_td(record, update_tds))

def update_player(record, update_name):
	cur.execute("""UPDATE player_stats SET player_name = (%s),
				WHERE ID = (%s)""", (update_name, record[0][0]))
	return success()

def update_rec(record, update_reception):
	cur.execute("""UPDATE player_stats SET rec = (%s) WHERE ID = (%s)""",
				(update_reception, record[0][0]))
	return success()

def update_yds(record, update_yards):
	cur.execute("""UPDATE player_stats SET yds = (%s) WHERE ID = (%s)""",
				(update_yards, record[0][0]))
	return success()

def update_yds_rec(record, update_yards_rec):
	cur.execute("""UPDATE player_stats SET yds_rec = (%s) WHERE ID = (%s)""",
				(update_yards_rec, record[0][0]))
	return success()

def update_long(record, update_longest):
	cur.execute("""UPDATE player_stats SET long = (%s) WHERE ID = (%s)""",
				(update_longest, record[0][0]))
	return success()

def update_td(record, update_tds):
	cur.execute("""UPDATE player_stats SET = (%s) WHERE ID = (%s)""",
				(update_tds, record[0][0]))
	return success()

def success():
	"""Let the user know they were successful"""
	return "Data successfully changed!"

route()

conn.commit()

cur.close()
conn.close()