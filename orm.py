import psycopg2

from secret import mysecretpassword

conn = psycopg2.connect(database='players', user='postgres',
						password=mysecretpassword)
cur = conn.cursor()

'''cur.execute("""CREATE TABLE player_stats
			(ID SERIAL PRIMARY KEY, player_name VARCHAR(50), rec SMALLINT,
			yds SMALLINT, yds_rec REAL, long SMALLINT,
			TD SMALLINT)""")'''

stats = [
	('Julian Edleman', 17, 153, 9.0, 19, 0),
	('Rob Gronkowski', 15, 227, 15.1, 40, 3),
	('James White', 7, 84, 12.0, 29, 0),
	('Danny Amendola', 7, 57, 8.1, 16, 0),
	('Brandon Bolden', 3, 26, 8.7, 20, 0),
	('Brandon LaFell', 3, 6, 2.0, 9, 0),
	('Keshawn Martin', 2, 57, 28.5, 42, 0),
	('Steven Jackson', 1, 2, 2.0, 2, 0)
]

#cur.executemany("""INSERT INTO player_stats VALUES(DEFAULT, %s, %s, %s, %s, %s, %s)""", (stats))


conn.commit()

cur.close()
conn.close()