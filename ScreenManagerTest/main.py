import kivy

from kivy.app import App
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import MySQLdb as mdb

Builder.load_file('ScreenManager.kv')

class NewUserScreen(Screen):
    pass

class LoginScreen(Screen):
        def check_login_info(self, uname, pword):
                # create the database connection
                db = mdb.connect("localhost", "assassins", "checkout", "assassins");
                
                # set the cursor to extract the data
                cur = db.cursor()
                
                # the statement to run in the database.
                sql = "SELECT * FROM users WHERE username = \"%s\"" % (uname)
                
                # try the connection
                try:
                        cur.execute(sql)
        
                        results = cur.fetchall()
                        for row in results:
                            uid = row[0]
                            username = row[1]
                            password = row[2]

                        if uname == username:
                            if pword == password:
                                return(1)
                            else:
                                return(3)
                        else:
                            return(2)

                except:
                        db.close()
                        return(1)
        
        # Varifies the user login information
        def login_button_function(self):

                # gets the data from the text inputs on the login page
                username = self.ids['username']
                password = self.ids['password']
                invalid = self.ids['invalid_login']

                # make sure that the values are not null
                if len(username.text) > 0:
                        invalid.text = ""
                        if len(password.text) > 0:
                                varify = self.check_login_info(username.text, password.text);
                                if(varify == 0):
                                        invalid.text = "Connection not Avalible"
                                elif(varify == 1):
                                        invalid.text = "Logged in"
                                elif(varify == 2):
                                        invalid.text = "Invalid Username"
                                        username.text = ""
                                elif(varify == 3):
                                        invalid.text = "Invalid Password"
                                        password.text = ""
                                else:
                                        invalid.text = "Unable to login"
                        else:
                                invalid.text = "Please enter a password"
                else:
                        invalid.text = "Please enter a username"

class ScreenManagerApp (App):
    def build (self):
        root = ScreenManager()
        root.add_widget(LoginScreen(name='Login'))
        root.add_widget(NewUserScreen(name='NewUser'))
        
        return root

if __name__ == '__main__':
    ScreenManagerApp().run()
        

