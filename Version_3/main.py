
import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
import mysql.connector
from mysql.connector import errorcode

Builder.load_file('assassins.kv')

class UsersHomeScreen(FloatLayout):
        pass

class NewUserScreen(FloatLayout):
        def goback(self):
                root.remove_widget(newuser)
                root.add_widget(login)

        def GetStarted(self):
		first = self.ids['first_input'].text
		last = self.ids['last_input'].text
		uname = self.ids['uname_input'].text
		pword= self.ids['pass_input'].text

		results = root.create("INSERT INTO users (firstname, lastname, username, password) VALUES ('%s','%s','%s','%s')" % (first,last,uname,pword))
		
                if results == 1:
                        popup = Popup(title='Congratulations', content=Label(text='Thank you, please sign in'), size_hint=(None, None), size=(400, 100))
                        root.remove_widget(newuser)
                        root.add_widget(login)
                        popup.open()
                elif results == 0:
                        popup = Popup(title='Sorry :(', content=Label(text='Your username is already in use'), size_hint=(None, None), size=(400, 100))
                        self.ids['uname_input'].text = ""
                        popup.open()
                elif results == 2:
                        popup = Popup(title='Sorry :(', content=Label(text='Didnt connect'), size_hint=(None, None), size=(400, 100))
                        popup.open()

class LoginScreen(FloatLayout):
        def changeScreen(self):
                root.remove_widget(login)
                root.add_widget(newuser)


        # Varifies the user login information
        def login_but(self):

                # gets the data from the text inputs on the login page
                uname = self.ids['uname_input']
                pword = self.ids['pass_input']

                # make sure that the values are not null
                if len(uname.text) > 0:
                        if len(pword.text) > 0:
                                query = root.retrieve("SELECT * FROM users WHERE username = \"%s\" AND password = \"%s\"" % (uname.text, pword.text))
                                if query == "":
                                        popup = Popup(title='Invalid Credentials', content=Label(text='Username or Password is Incorrect'), size_hint=(None, None), size=(400, 100))
                                        popup.open()
                                elif query == 0:
                                        popup = Popup(title='Connection', content=Label(text='Could not connect to the database'), size_hint=(None, None), size=(400, 100))
                                        popup.open()
                                else:
                                        uid, firstname, lastname, username, password, game = query[0]
                                        loggedinuser = username
                                        root.remove_widget(login)
                                        home.ids['uname_label'].text = "Welcome back %s" % (firstname)
                                        root.add_widget(home)
                        else:
                                popup = Popup(title='Invalid Credentials', content=Label(text='Please Enter a Password'), size_hint=(None, None), size=(400, 100))
                                popup.open()
                else:
                        popup = Popup(title='Invalid Credentials', content=Label(text='Please Enter a Username'), size_hint=(None, None), size=(400, 100))
                        popup.open()

        def signup(self):
                root.remove_widget(login)
                root.add_widget(newuser)

class RootWidget(FloatLayout):

        def retrieve (self, sql):
                try:

                        cnx = mysql.connector.connect(user='assassins', password='checkout', host=ip, database='assassins')

                        # set the cursor to extract the data
                        cur = cnx.cursor()
                        cur.execute(sql)
                        
                        return cur.fetchall()

                except mysql.connector.Error as err:
                        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                                print("Something is wrong with your user name or password")
                                return(0)
                        elif err.errno == errorcode.ER_BAD_DB_ERROR:
                                print("Database does not exists")
                                return(0)
                        else:
                                print(err)
                else:
                        cnx.close()
                        return(0)

        def create (self, sql):
                try:
                        cnx = mysql.connector.connect(user='assassins', password='checkout', host=ip, database='assassins')

                        cur = cnx.cursor()        
                        cur.execute(sql)
                        cnx.commit()

                        cur.close()
                        cnx.close()
                        return(1)

                except mysql.connector.Error as err:
                        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                                print("Something is wrong with your user name or password")
                                return(2)
                        elif err.errno == errorcode.ER_BAD_DB_ERROR:
                                print("Database does not exists")
                                return(2)
                        else:
                                print(err)
                                return(0)

root = RootWidget()
login = LoginScreen()
newuser = NewUserScreen()
home = UsersHomeScreen()
ip = '192.168.1.111'

class assassinsApp (App):
	def build (self):
                root.add_widget(login)
                
		return root

	

if __name__ == '__main__':
	assassinsApp().run()
		

