# Import all of the files need to run the Kivy application in Python.
import kivy

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.uix.widget import Widget
import pprint
import MySQLdb as mdb


# Set the default size of the window to the resolution of an iPhone5 Screen.
Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '1136')

class LoginPage(FloatLayout):

        def check_login_info(self, username, password):
                
                # create the database connection
                db = mdb.connect("localhost","assassins","checkout","assassins");

                # set the cursor to extract the data
                cur = db.cursor()
                
                # the statement to run in the database.
                sql = "SELECT * FROM users WHERE username=%s" % (username)
                
                #try the connection
                try:
                        cur.execute(sql)
        
                        results = cur.fetchall()
                           
                        uid = row[0]
                        sqlusername = row[1]
                        sqlpassword = row[2]

                        print "sqlusername = %s, sqlpassword= %s" % (sqlusername, sqlpassword)

                except:
                        db.close()
                        return 0


        
        # Varifies the user login information
                        def login_button_function(self):

                                #gets the data from the text inputs on the login page
                                username = self.ids['username']
                                password = self.ids['password']
                                invalid = self.ids['invalid_login']
                
                                # make sure that the values are not null
                                if len(username.text) > 0:
                                        invalid.text = ""
                                        if len(password.text) > 0:
                                                varify = self.check_login_info(username.text, password.text);
                                                #if(varify == 0):
                                                #    invalid.text = "Connection not Avalible"
                                                #elif(varify == 1):
                                                #   invalid.text = "Logged IN"
                                                #elif(varify == 2):
                                                #       invalid.text = "Invalid Username"
                                                #       username.text = ""
                                                #elif(varify == 3)
                                                #       invalid.text = "Invalid Password"
                                                #       password.text = ""
                                                #else:
                                                #    invalid.text = "Unable to login"
                                        else:
                                                invalid.text = "Please enter a password"
                                else:
                                        invalid.text = "Please enter a username"
                                print self.check_login_info(username.text, password.text)

class AssassinsApp(App):
        def build(self):
                return LoginPage()

if __name__ == '__main__':
        AssassinsApp().run()
