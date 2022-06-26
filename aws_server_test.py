import pymysql
import mysql.connector

host = 'database-2.cji0mokilyxv.us-west-1.rds.amazonaws.com'
user = 'admin'
password = '12345678'
database_id = 'database-2'

'''
cnx = mysql.connector.connect(user=user, password=password,
                                host=host, database=database_id)
print('yee connected')
cnx.close()
'''

db = pymysql.connect(host=host1, user=user, password='cakecake',
    db='database-1', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)



host = 'database-1.cji0mokilyxv.us-west-1.rds.amazonaws.com'
host1 = 'database-1.cji0mokilyxv.us-west-1.rds.amazonaws.com'
user = 'admin'
password = 'cakecake'
database_id = 'database-1'


cnx = mysql.connector.connect(user=user, password=password, host=host, database=database_id)

print('yee connected')
cnx.close()


db = pymysql.connect(host=host, user=user, password=password)

#db = pymysql.connect(host=host1, user=user, password='cakecake',
#    db='database-1', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)



'''
connection = pymysql.connect(host=host, user=user, password=password)
with connection:
    cur = connection.cursor()
    cur.execute("SELECT VERSION()")
    version = cur.fetchone()
    print("Database version: {} ".format(version[0]))
'''
