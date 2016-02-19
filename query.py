import psycopg2

from secret import mysecretpassword


conn = psycopg2.connect(database='players', user='postgres',
						password=mysecretpassword)

cur = conn.cursor()

def find_player():
	"""Search the db by player name"""
	print("Here is the current list of players in the db...\n")
	print(display_player_names())
	player_search = input("Which player do you want to search for? ")
	cur.execute("select * from player_stats where player_name = (%s);", (player_search,))
	row = cur.fetchall()
	print(row)
	return

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
				(%s, %s, %s, %s, %s, %s)""", data)
	return "Your player has been added!"

def top_performers():
	"""Allow user to search for top players in each category"""
	choice = ("See which players performed the best in each category, "
		  	  "You can search [R]ec, [Y]ds, [YR]ds_rec, [L]ong or [TD] "
		  	  "Type the letter(s) in the brackets for the listings\n ").lower()
	if choice == 'r':
		print(list_rec())
	elif choice == 'y':
		print(list_yds())
	elif choice == 'YR':
		print(list_yds_rec())
	elif choice == 'L':
		print(list_long())
	elif choice == 'td':
		print(list_td())
	else:
		print("What did you say? I did not understand that. \n\n")
		top_performers()

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

conn.commit()

cur.close()
conn.close()