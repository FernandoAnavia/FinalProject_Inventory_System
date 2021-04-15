import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="F3rn4nd0An4v142019",
  database="InvSystem"
)

print(mydb)