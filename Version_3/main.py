
import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
import MySQLdb as mdb

Builder.load_file('assassins.kv')

class UsersHomeScreen(FloatLayout):
        pass

class NewUserScreen(FloatLayout):
        def goback(self):
                root.remove_widget(newuser)
                root.add_widget(login)

class LoginScreen(FloatLayout):
        def changeScreen(self):
                root.remove_widget(login)
                root.add_widget(newuser)


        # Varifies the user login information
        def login_but(self):

                # gets the data from the text inputs on the login page
                username = self.ids['uname_input']
                password = self.ids['pass_input']

                # make sure that the values are not null
                if len(username.text) > 0:
                        if len(password.text) > 0:
                                query = root.retrieve("SELECT * FROM users WHERE username = \"%s\" AND password = \"%s\"" % (username.text, password.text))
                                if query == 1:
                                        popup = Popup(title='Invalid Credentials', content=Label(text='Username or Password is Incorrect'), size_hint=(None, None), size=(400, 100))
                                        popup.open()
                                elif query == 0:
                                        popup = Popup(title='Connection', content=Label(text='Could not connect to the database'), size_hint=(None, None), size=(400, 100))
                                        popup.open()
                                else:
                                        root.remove_widget(login)
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

        def create (self, sql):
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


                
root = RootWidget()
login = LoginScreen()
newuser = NewUserScreen()
home = UsersHomeScreen()
        
class assassinsApp (App):
	def build (self):
                root.add_widget(login)
                
		return root

	

if __name__ == '__main__':
	assassinsApp().run()
		

