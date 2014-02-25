import MySQLdb as mdb
import sys

uname = "rcarter"
pword = ""

db = mdb.connect("localhost","assassins","checkout","assassins");

cur = db.cursor()
    
sql = "SELECT * FROM users WHERE uid = 1"

try:
    cur.execute(sql)
    
    results = cur.fetchall()
    for row in results:
        uid = row[0]
        username = row[1]
        password = row[2]
        
        print "uid=%d, username=%s, password=%s" % \
             (uid, username, password )

	if uname == username:
		print "Username"
	if pword == password:
		print "password"
    
except:
  
    print "Error unable to fetch data"

db.close()


