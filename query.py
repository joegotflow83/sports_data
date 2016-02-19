import psycopg2

from secret import mysecretpassword


conn = psycopg2.connect(database='players', user='postgres',
						password=mysecretpassword)

cur = conn.cursor()

cur.execute("select * from player_stats")
rows = cur.fetchall()
player_search = input("Which player do you want to search for? ")
cur.execute("select * from player_stats where player_name = (%s);", (player_search,))
row = cur.fetchall()
print(row)

conn.commit()

cur.close()
conn.close()