
import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
import mysql.connector
from mysql.connector import errorcode

Builder.load_file('assassins.kv')

class GameInfo(FloatLayout):
    def goback(self):
        root.remove_widget(gInfo)
        root.add_widget(sview)

class CreateGame(FloatLayout):
        def goback(self):
                root.remove_widget(create)
                root.add_widget(home)
        
        def clear(self):
            self.ids['name_input'].text = ""
            self.ids['location_input'].text = ""

        def createGame(self):
            name = self.ids['name_input'].text
            location = self.ids['location_input'].text

            if name == "" or location == "":
                popup = Popup(title='Error', content=Label(text='Please enter values'), size_hint=(None, None), size=(400, 100))
                popup.open()
            else:
                results = root.create("INSERT INTO Games (name, location) VALUES ('%s','%s')" % (name,location))

                if results == 1:
                        popup = Popup(title='Congratulations', content=Label(text='Thank you, game created'), size_hint=(None, None), size=(400, 100))
                        create.clear()
                        popup.open()
                elif results == 0:
                        popup = Popup(title='Sorry :(', content=Label(text='This game already exists.  Also, please do not include apostrophies'), size_hint=(None, None), size=(400, 100))
                        create.clear()
                        popup.open()
                elif results == 2:
                        popup = Popup(title='Sorry :(', content=Label(text='Didnt connect'), size_hint=(None, None), size=(400, 100))
                        create.clear()
                        popup.open()

class CurrentGame(FloatLayout):
        def goback(self):
                root.remove_widget(current)
                root.add_widget(home)

        def getName(self):
                uid = 17
                query = root.retrieve("SELECT name FROM Games WHERE uid = \"%s\"" % (uid))
                name = query[0]
                current.ids['currentgame_label'].text = name[0]

class AllGames(FloatLayout):
	def goback(self):
                layout.clear_widgets()
                sview.remove_widget(layout)
                root.clear_widgets()
                root.add_widget(home)

class UsersHomeScreen(FloatLayout):
        def logout(self):
                root.remove_widget(home)
                root.add_widget(login)
                login.ids['uname_input'].text = ""
                login.ids['pass_input'].text = ""
                login.loggedinuser = ""
                #login.uid = None
                login.firstname = ""
                login.lastname = ""
                login.username = ""
                login.password = ""
                login.game = ""

        def currentGameScreen(self):
            root.remove_widget(home)
            root.add_widget(current)
            current.getName()

        def createGameScreen(self):
            root.remove_widget(home)
            root.add_widget(create)

        def viewgames(self):
                root.remove_widget(home)
#               root.add_widget(games)
                
                # Make sure the height is such that there is something to scroll.
                layout.bind(minimum_height=layout.setter('height'))
                # Run sql query to get all available games
                availableGames = root.retrieve("SELECT * FROM Games")
                if availableGames == "":
                        popup = Popup(title='No Games', content=Label(text='There are currently no available games'), size_hint=(None, None), size=(400, 100))
                        popup.open()
                elif availableGames == 0:
                        popup = Popup(title='Connection', content=Label(text='Could not connect to the database'), size_hint=(None, None), size=(400, 100))
                        popup.open()
                else:
                    for tpl in availableGames:
                        uid, name, location = tpl
                        btn = Button(text=name, size_hint_y=None, height=40)
                        layout.add_widget(btn)

                sview.add_widget(layout)
                root.add_widget(sview)
                root.add_widget(games)

class NewUserScreen(FloatLayout):
        def goback(self):
                root.remove_widget(newuser)
                root.add_widget(login)
                login.ids['uname_input'].text = ""
                login.ids['pass_input'].text = ""

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
games = AllGames()
create = CreateGame()
current = CurrentGame()
gInfo = GameInfo()
sview = ScrollView(size_hint=(None, None), size=(400, 400))
layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
ip = '192.168.1.'

class assassinsApp (App):
	def build (self):
                root.add_widget(login)
                
		return root

	

if __name__ == '__main__':
	assassinsApp().run()
		

