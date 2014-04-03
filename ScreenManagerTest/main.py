
import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
import MySQLdb as mdb

Builder.load_file('assassins.kv')

class UsersScreen(Screen):
	pass

class NewUserScreen(Screen):

	
	def GetStarted(self):
		first = self.ids['fname_input'].text
		last = self.ids['lname_input'].text
		uname = self.ids['uname_input'].text
		pword= self.ids['pword_input'].text

		results = create("INSERT INTO users (firstname, lastname, username, password) VALUES ('%s','%s','%s','%s')" % (first,last,uname,pword))
		
                if results == 1:
                        popup = Popup(title='Congratulations', content=Label(text='Thank you, please sign in'), size_hint=(None, None), size=(400, 100))
                        root.switch_to(LoginScreen())
                        popup.open()
                elif results == 0:
                        popup = Popup(title='Sorry :(', content=Label(text='Didnt register'), size_hint=(None, None), size=(400, 100))
                        self.ids['uname_input'].text = ""
                        popup.open()
                elif results == 2:
					popup = Popup(title='Sorry :(', content=Label(text='Didnt connect'), size_hint=(None, None), size=(400, 100))
					popup.open()
                        
                
class LoginScreen(Screen):
		
		# Varifies the user login information
		def login_button_function(self):

				# gets the data from the text inputs on the login page
				username = self.ids['username']
				password = self.ids['password']
				invalid = self.ids['invalid_login']

				# make sure that the values are not null
                                if len(username.text) > 0:
                                        if len(password.text) > 0:
                                                query = retrieve("SELECT * FROM users WHERE username = \"%s\" AND password = \"%s\"" % (username.text, password.text))
                                                if query == 1:
                                                        popup = Popup(title='Invalid Credentials', content=Label(text='Username or Password is Incorrect'), size_hint=(None, None), size=(400, 100))
                                                        popup.open()
                                                elif query == 0:
                                                        popup = Popup(title='Connection', content=Label(text='Could not connect to the database'), size_hint=(None, None), size=(400, 100))
                                                        popup.open()
                                                else:
                                                        root.switch_to(UsersScreen())
                                        else:
                                                popup = Popup(title='Invalid Credentials', content=Label(text='Please Enter a Password'), size_hint=(None, None), size=(400, 100))
                                                popup.open()
                                else:
                                        popup = Popup(title='Invalid Credentials', content=Label(text='Please Enter a Username'), size_hint=(None, None), size=(400, 100))
                                        popup.open()
                                                        


root = ScreenManager()
root.add_widget(LoginScreen(name='Login'))
root.add_widget(NewUserScreen(name='NewUser'))
root.add_widget(UsersScreen(name='UsersScreen'))

def retrieve (sql):
        try:
                db = mdb.connect("localhost", "assassins", "checkout", "assassins");
                # set the cursor to extract the data
                cur = db.cursor()

                try:
                        cur.execute(sql)
                        results = cur.fetchall()
                        if len(results) == 0:
                                return (1)
                        else:
                                return cur.fetchall()
                except:
                        return(1)
        except:
                return(0)

def create (sql):
        try:
                db = mdb.connect("localhost", "assassins", "checkout", "assassins");
                cur = db.cursor()
                try:
                        cur.execute(sql)
			db.commit()
                        return(1)
                except:
			db.rollback()
                        return(0)
        except:
                return(2)

class ScreenManagerApp (App):
	def build (self):   
		return root

	

if __name__ == '__main__':
	ScreenManagerApp().run()
		

