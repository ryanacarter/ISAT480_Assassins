def SQLDBConnect(self):

		
    # Open database connection
    db = MySQL.connect("localhost", "kivy", "checkout", "checkout")
    
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    
    # Prepare SQL query to GET the database information
    sql = "SELECT * FROM Login_Information WHERE User_Name = " + username
    
    # use try to keep the program from crashing if it cannot connect to the database.
    try:
    
        #execute the SQL command
        cursor.execute(sql)
    
        #put the results in a list
        results = cursor.fetchall()
        for row in results:
            uid = row[0]
            User = row[1]
            Pass = row [2]
        
        if User == username:
            if Pass == password:
                return True
            else:
                return False
        else:
            return False
            
    except:
        return False
            

