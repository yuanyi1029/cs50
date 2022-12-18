from cs50 import SQL

db = SQL("sqlite:///favorites.db")

favorite = input("Favorite: ")

# db.execute returns a list of dictionaries that matches the query
# If there are no matches, an empty list returns
# This query returns a list of 1 dictionary with key of n and a value of 1
rows = db.execute("SELECT COUNT(*) AS n FROM favorites WHERE problem = ?", favorite)

row = rows[0]
print(row["n"])

