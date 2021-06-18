import mysql.connector

post_monitoring_db = mysql.connector.connect(
    host = "192.168.86.23",
    user  = "raspberry",
    password = "password"
)

print(post_monitoring_db)
