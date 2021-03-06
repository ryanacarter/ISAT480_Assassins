
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
ip = '192.168.1.6'
#########################################################################
# User Oject to hold all of the Users information
#########################################################################
class user():
    uid = ""
    firstName = ""
    lastName = ""
    username = ""
    game_id = ""
    bt_ID = ""
    status = ""
    target = ""

class GameInfo(FloatLayout):
    def goback(self):
        root.remove_widget(gInfo)
        root.add_widget(sview)

#######################################################################################
# CreateGameScreen Widget
#######################################################################################
class CreateGameScreen(Screen, FloatLayout):
    def goback(self):
        sm.current = "Home"
    
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
            results = create("INSERT INTO Games (name, location) VALUES ('%s','%s')" % (name,location))

            if results == 1:
                popup = Popup(title='Congratulations', content=Label(text='Thank you, game created'), size_hint=(None, None), size=(400, 100))
                self.clear()
                popup.open()
            elif results == 0:
                popup = Popup(title='Sorry :(', content=Label(text='This game already exists.  Also, please do not include apostrophies'), size_hint=(None, None), size=(400, 100))
                self.clear()
                popup.open()
            elif results == 2:
                popup = Popup(title='Sorry :(', content=Label(text='Didnt connect'), size_hint=(None, None), size=(400, 100))
                self.clear()
                popup.open()

#######################################################################################
# EliminatedScreen Widget
#######################################################################################
class EliminatedScreen(Screen, FloatLayout):
    def __init__ (self, *args, **kwargs):
        super(EliminatedScreen, self).__init__(*args, **kwargs)

    def goback(self):
        sm.current = "Home"

    def leaveGame(self):
        update("UPDATE users SET status = '%i', game_id = '%s' WHERE uid = '%s'" % (0, "", user.uid))
        popup = Popup(title='Notification', content=Label(text='Your have left the game'), size_hint=(.9, .3), size=(800, 800))
        popup.open()
        updateUser()
        sm.current = "Home"

#######################################################################################
# CurrentGameScreen Widget
#######################################################################################
class CurrentGameScreen(Screen, FloatLayout):
    def __init__ (self, *args, **kwargs):
        super(CurrentGameScreen, self).__init__(*args, **kwargs)
        self.eliminate = self.ids['eliminate']
        self.status = self.ids['status']
        self.eliminate.disabled = True
        self.BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
        self.BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
        self.BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
        self.UUID = autoclass('java.util.UUID')
        self.Bundle = autoclass('android.os.Bundle')
        self.Intent = autoclass('android.content.Intent')
        self.IntentFilter = autoclass('android.content.IntentFilter')
        self.Context = autoclass('android.content.Context')
        self.Toast = autoclass('android.widget.Toast')
        self.PythonActivity = autoclass('org.renpy.android.PythonActivity')

        self.myBTA = self.BluetoothAdapter.getDefaultAdapter()
        self.popup = Popup(title='Notification', content=Label(text='Searching For Target. . .'), size_hint=(.9, .3), size=(800, 800))
        self.popup1 = Popup(title='Notification', content=Label(text='Target Found!'), size_hint=(.9, .3), size=(800, 800))


    def goback(self):
        sm.current = "Home"

    def findTarget(self):
        self.popup.open()
        self.br = BroadcastReceiver(self.onReceive, actions=['main'], myFilter = self.BluetoothDevice.ACTION_FOUND)
        self.br.start()
        self.myBTA.startDiscovery()

    def onReceive(self, context, intent):
        action = intent.getAction();
        if (self.BluetoothDevice.ACTION_FOUND == action):
            extras = intent.getParcelableExtra(self.BluetoothDevice.EXTRA_DEVICE)
            device = cast('android.bluetooth.BluetoothDevice', extras)
            deviceName = device.getAddress()
            if deviceName == user.target:
                self.eliminate.disabled = False
                self.eliminate.color = (1,0,0,1)
                self.popup.dismiss()
                self.popup1.open()
                self.br.stop()

    def eliminateUser(self):
        query = retrieve("SELECT target FROM users WHERE bt_ID = '%s'" % (user.target))
        update("UPDATE users SET target = '',status = '0' WHERE bt_ID = '%s'" % (user.target))
        user.target = query[0]
        print user.target, '**************************************'
        create("UPDATE users SET target = '%s' WHERE uid = '%s'" % (user.target, user.uid))
        updateUser()
        query1 = retrieve("SELECT firstname,lastname FROM users WHERE bt_ID = '%s'" % (user.target))
        tfirstname, tlastname = query1[0]
        self.status.text = str("Your Current Target is %s %s" % (tfirstname, tlastname))
        

#######################################################################################
# AllGamesScreen Widget
#######################################################################################
class AllGames(Screen, FloatLayout):
        def __init__ (self, *args, **kwargs):
            super(AllGames, self).__init__(*args, **kwargs)
            self.viewGames()

        def viewGames(self):
            sview = ScrollView(size_hint=(.9, .8), pos_hint={'center_x':.5, 'center_y':.5})
            layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
            # Make sure the height is such that there is something to scroll.
            layout.bind(minimum_height=layout.setter('height'))
            # Run sql query to get all available games
            availableGames = retrieve("SELECT * FROM Games")
            
            if availableGames == "":
                popup = Popup(title='No Games', content=Label(text='There are currently no available games'), size_hint=(None, None), size=(400, 100))
                popup.open()
            elif availableGames == 0:
                popup = Popup(title='Connection', content=Label(text='Could not connect to the database'), size_hint=(None, None), size=(400, 100))
                popup.open()
            else:
                for tpl in availableGames:
                    uid, name, location, creator, status = tpl
                    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n\n"
                    print name
                    print "\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n\n"
                    btn = Button(id=name, text=name, size_hint_y=None, height=200)
                    btn.bind(on_press=self.seeInfo)
                    layout.add_widget(btn)

            sview.add_widget(layout)
            self.add_widget(sview)
            
	def goback(self):
            sm.current = "Home"

        def seeInfo(self, args):
            sm.current = "GameInfoScreen"
            
#######################################################################################
# GameInfoScreen Widget
#######################################################################################
class GameInfoScreen(Screen, FloatLayout):
    def __init__ (self, *args, **kwargs):
        super(GameInfoScreen, self).__init__(*args, **kwargs)

    def goback(self):
        sm.current = "AllGames"

#######################################################################################
# UserHomeScreen Widget
#######################################################################################
class UsersHomeScreen(Screen, FloatLayout):
    def __init__ (self, *args, **kwargs):
        super(UsersHomeScreen, self).__init__(*args, **kwargs)
    
    def logout(self):
        logoutUser()

    def currentGameScreen(self):
        updateUser()
        tfirstname = ""
        tlastname = ""
        if (user.game_id == 0):
            popup = Popup(title='Notification', content=Label(text='Please Select a game from \nthe All Games Button'), size_hint=(.9, .3), size=(800, 800))
            popup.open()
        elif (user.status == 0):
            sm.current = "Eliminated"
        else:
            query = retrieve("SELECT firstname, lastname FROM users WHERE bt_ID = \"%s\"" % (user.target))
            tfirstname, tlastname = query[0]
            sm.get_screen("Current").status.text = str("Your Current Target is %s %s" % (tfirstname, tlastname))
            sm.current = "Current"

    def createGameScreen(self):
        sm.current = "Create"

    def viewgames(self):
        sm.get_screen("AllGames").clear_widgets()
        sm.get_screen("AllGames").__init__()
        sm.current = "AllGames"
        
##        root.remove_widget(home)sm.get
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
                    popup = Popup(title='Error', content=Label(text='Please enter values'), size_hint=(.9, .3), size=(800, 800))
                    popup.open()
                else:
                    gameID = 0
                    bt_ID = myBTA.getAddress()
		    results = create("INSERT INTO users (firstname, lastname, username, password, game_id, bt_ID) VALUES ('%s','%s','%s','%s', '%i', '%s')" % (first,last,uname,pword, gameID, bt_ID))
		
                    if results == 1:
                            popup = Popup(title='Congratulations', content=Label(text='Thank you, please sign in'),size_hint=(.9, .3), size=(800, 800))
                            sm.current = "Login"
                            popup.open()
                    elif results == 0:
                            popup = Popup(title='Sorry :(', content=Label(text='Your username is already in use'),size_hint=(.9, .3), size=(800, 800))
                            self.ids['uname_input'].text = ""
                            popup.open()
                    elif results == 2:
                            popup = Popup(title='Sorry :(', content=Label(text='Didnt connect'), size_hint=(.9, .3), size=(800, 800))
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
                                popup = Popup(title='', content=Label(text='Loading . . .'), size_hint=(.9, .3), size=(800, 800))
                                popup.open()
                                query = retrieve("SELECT * FROM users WHERE username = \"%s\" AND password = \"%s\"" % (uname.text, pword.text))
                                popup.dismiss()
                                if query == 0:
                                        popup = Popup(title='Connection', content=Label(text='Could not connect to the database'), size_hint=(.9, .3), size=(800, 800))
                                        popup.open()
                                elif len(query) < 1:
                                        popup = Popup(title='Invalid Credentials', content=Label(text='Username or Password is Incorrect'), size_hint=(.9, .3), size=(800, 800))
                                        popup.open()
                                else:
                                        user.uid, user.firstname, user.lastname, user.username, user.password, user.game_id, user.bt_ID, user.status, user.target = query[0]
                                        bt_ID = myBTA.getAddress()
                                        results = create("UPDATE users SET bt_ID = '%s' WHERE uid = '%s'" % (bt_ID, user.uid))
                                        uname.text = ""
                                        pword.text = ""
                                        sm.current = "Home"
                        else:
                                popup = Popup(title='Invalid Credentials', content=Label(text='Please Enter a Password'), size_hint=(.9, .3), size=(800, 800))
                                popup.open()
                else:
                        popup = Popup(title='Invalid Credentials', content=Label(text='Please Enter a Username'), size_hint=(.9, .3), size=(800, 800))
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
    user.uid = ""
    user.firstName = ""
    user.lastName = ""
    user.username = ""
    user.game_id = ""
    user.bt_ID = ""
    user.status = 1
    user.target = ""
    sm.current = "Login"

def updateUser():
    print "**********", user.game_id
    query = retrieve("SELECT * FROM users WHERE uid = \"%s\"" % (user.uid))
    user.uid, user.firstname, user.lastname, user.username, user.password, user.game_id, user.bt_ID, user.status, user.target = query[0]
    print "**********", user.game_id

#########################################################################
# Screen Manager
#########################################################################              
sm = ScreenManager()
sm.add_widget(LoginScreen(name='Login'))
sm.add_widget(NewUserScreen(name='NewUser'))
sm.add_widget(UsersHomeScreen(name='Home'))
sm.add_widget(CurrentGameScreen(name='Current'))
sm.add_widget(EliminatedScreen(name='Eliminated'))
sm.add_widget(CreateGameScreen(name='Create'))
sm.add_widget(AllGames(name='AllGames'))
sm.add_widget(GameInfoScreen(name='GameInfoScreen'))


#########################################################################
# Variables
######################################################################### 
sview = ScrollView(size_hint=(None, None), size=(400, 400))
layout = GridLayout(cols=1, spacing=10, size_hint_y=None)

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
		

