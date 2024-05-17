import pymysql
try:
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        db="Online_wallet"
    )
    cursor = connection.cursor()
except:
    print("Connection Error!")