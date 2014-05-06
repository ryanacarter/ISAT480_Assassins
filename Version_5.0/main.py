
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
from jnius import autoclass
from jnius import cast
from android.broadcast import BroadcastReceiver

Builder.load_file('assassins.kv')

#########################################################################
# User Information --Logged IN
######################################################################### 
uid = ""
firstName = ""
lastName = ""
username = ""
gameID = ""
bt_ID = ""

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

#######################################################################################
# CurrentGameScreen Widget
#######################################################################################
class CurrentGameScreen(Screen, FloatLayout):
    def __init__ (self, *args, **kwargs):
        super(CurrentGameScreen, self).__init__(*args, **kwargs)

    def goback(self):
        sm.current = "Home"

    def getName(self):
            game_id = 17
            query = root.retrieve("SELECT name FROM Games WHERE game_id = \"%s\"" % (game_id))
            name = query[0]
            current.ids['currentgame_label'].text = name[0]


#######################################################################################
# AllGamesScreen Widget
#######################################################################################
class AllGames(FloatLayout):
	def goback(self):
                layout.clear_widgets()
                sview.remove_widget(layout)
                root.clear_widgets()
                root.add_widget(home)

#######################################################################################
# UserHomeScreen Widget
#######################################################################################
class UsersHomeScreen(Screen, FloatLayout):
    def __init__ (self, *args, **kwargs):
        super(UsersHomeScreen, self).__init__(*args, **kwargs)
    
    def logout(self):
        logoutUser()

    def currentGameScreen(self):
        sm.current = "Current"

    def createGameScreen(self):
        pass
##        root.remove_widget(home)
##        root.add_widget(create)

    def viewgames(self):
        pass
##        root.remove_widget(home)
##       
##        # Make sure the height is such that there is something to scroll.
##        layout.bind(minimum_height=layout.setter('height'))
##        # Run sql query to get all available games
##        availableGames = root.retrieve("SELECT * FROM Games")
##        if availableGames == "":
##            popup = Popup(title='No Games', content=Label(text='There are currently no available games'), size_hint=(None, None), size=(400, 100))
##            popup.open()
##        elif availableGames == 0:
##            popup = Popup(title='Connection', content=Label(text='Could not connect to the database'), size_hint=(None, None), size=(400, 100))
##            popup.open()
##        else:
##            for tpl in availableGames:
##                uid, name, location = tpl
##                btn = Button(text=name, size_hint_y=None, height=40)
##                layout.add_widget(btn)
##
##        sview.add_widget(layout)
##        root.add_widget(sview)
##        root.add_widget(games)

#######################################################################################
# NewUserScreen Widget
#######################################################################################
class NewUserScreen(Screen, FloatLayout):
        def __init__(self, *args, **kwargs):
		super(NewUserScreen, self).__init__(*args, **kwargs)
		
        def goback(self):
                sm.current = "Login"

        def GetStarted(self):
		first = self.ids['first_input'].text
		last = self.ids['last_input'].text
		uname = self.ids['uname_input'].text
		pword= self.ids['pass_input'].text
                if first == "" or last == "" or uname == "" or pword == "":
                    popup = Popup(title='Error', content=Label(text='Please enter values'), size_hint=(None, None), size=(400, 100))
                    popup.open()
                else:
                    gameID = 0
                    bt_ID = myBTA.getAddress()
		    results = create("INSERT INTO users (firstname, lastname, username, password, game_id, bt_ID) VALUES ('%s','%s','%s','%s', '%i', '%s')" % (first,last,uname,pword, gameID, bt_ID))
		
                    if results == 1:
                            popup = Popup(title='Congratulations', content=Label(text='Thank you, please sign in'), size_hint=(None, None), size=(400, 100))
                            sm.current = "Login"
                            popup.open()
                    elif results == 0:
                            popup = Popup(title='Sorry :(', content=Label(text='Your username is already in use'), size_hint=(None, None), size=(400, 100))
                            self.ids['uname_input'].text = ""
                            popup.open()
                    elif results == 2:
                            popup = Popup(title='Sorry :(', content=Label(text='Didnt connect'), size_hint=(None, None), size=(400, 100))
                            popup.open()



                            
###########################################################################################
# Widget to login, This is the first screen that the user will see and it will be where the
# logon to the application. It gets the bluetooth MAC ID and the user that is logged in, it
# passes that back to the App to store the values
###########################################################################################
class LoginScreen(Screen, FloatLayout):
    
        def __init__(self, *args, **kwargs):
		super(LoginScreen, self).__init__(*args, **kwargs)

        # Varifies the user login information
        def login_but(self):

                # gets the data from the text inputs on the login page
                uname = self.ids['uname_input']
                pword = self.ids['pass_input']

                # make sure that the values are not null
                if len(uname.text) > 0:
                        if len(pword.text) > 0:
                                popup = Popup(title='', content=Label(text='Loading . . .'), size_hint=(None, None), size=(400, 100))
                                popup.open()
                                query = retrieve("SELECT * FROM users WHERE username = \"%s\" AND password = \"%s\"" % (uname.text, pword.text))
                                popup.dismiss()
                                if query == 0:
                                        popup = Popup(title='Connection', content=Label(text='Could not connect to the database'), size_hint=(None, None), size=(400, 100))
                                        popup.open()
                                elif len(query) < 1:
                                        popup = Popup(title='Invalid Credentials', content=Label(text='Username or Password is Incorrect'), size_hint=(None, None), size=(400, 100))
                                        popup.open()
                                else:
                                        uid, firstname, lastname, username, password, game, bt_ID = query[0]
                                        bt_ID = myBTA.getAddress()
                                        results = create("UPDATE users SET bt_ID = '%s' WHERE uid = '%s'" % (bt_ID, uid))
                                        uname.text = ""
                                        pword.text = ""
                                        sm.current = "Home"
                        else:
                                popup = Popup(title='Invalid Credentials', content=Label(text='Please Enter a Password'), size_hint=(None, None), size=(400, 100))
                                popup.open()
                else:
                        popup = Popup(title='Invalid Credentials', content=Label(text='Please Enter a Username'), size_hint=(None, None), size=(400, 100))
                        popup.open()

        # This changes to screen to the new user page.
        def signup(self):
                sm.current = "NewUser"

def retrieve (sql):
        try:
            cnx = mysql.connector.connect(user='assassins', password='checkout', host=ip, database='assassins')

            # set the cursor to extract the data
            cur = cnx.cursor()
            cur.execute(sql)
            return cur.fetchall()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                    return("")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exists")
                    return(0)
            else:
                    print(err)
                    return(0)
        else:
            cnx.close()
            return(0)

def create (sql):
    print (sql)
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
    return root

def update (sql):
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
            return("")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exists")
            return(0)
        else:
            print(err)
            return(0)

def logoutUser():
    uid = ""
    firstName = ""
    lastName = ""
    username = ""
    gameID = ""
    bt_ID = ""
    sm.current = "Login"



#########################################################################
# Screen Manager
#########################################################################              
sm = ScreenManager()
sm.add_widget(LoginScreen(name='Login'))
sm.add_widget(NewUserScreen(name='NewUser'))
sm.add_widget(UsersHomeScreen(name='Home'))
sm.add_widget(CurrentGameScreen(name='Current'))

#########################################################################
# Variables
######################################################################### 
sview = ScrollView(size_hint=(None, None), size=(400, 400))
layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
ip = '192.168.1.116'

#########################################################################
# Bluetooth
#########################################################################
BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
UUID = autoclass('java.util.UUID')
Bundle = autoclass('android.os.Bundle')
Intent = autoclass('android.content.Intent')
IntentFilter = autoclass('android.content.IntentFilter')
Context = autoclass('android.content.Context')
Toast = autoclass('android.widget.Toast')
PythonActivity = autoclass('org.renpy.android.PythonActivity')

myBTA = BluetoothAdapter.getDefaultAdapter()


#######################################################################################
# The is the Application class
#######################################################################################
class assassinsApp (App):
    def build (self):
        if(myBTA.isEnabled() == False):
                        intent = Intent()
                        intent.setAction(BluetoothAdapter.ACTION_REQUEST_ENABLE)
                        myActivity = cast('android.app.Activity', PythonActivity.mActivity)
                        myActivity.startActivity(intent)
        return sm

if __name__ == '__main__':
	assassinsApp().run()
		

