
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

class LoginScreen(FloatLayout):
        def __init__(self):
                super(LoginScreen, self).__init__()
##                BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
##                myBluetoothAdapter = BluetoothAdapter.startDiscovery()
##                BluetoothName = myBluetoothAdapter.getBondedDevices().toArray()
##                firstDevice = BluetoothName[0].getName()
##                BroadcastReceiver = autoclass('android.content.BroadcastReveiver')
##                Intent = autoclass('android.content.Intent')
##                Activity = autoclass('android.content.Activity')

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

                self.printLabel = self.ids['label1']
                self.printLabel.text = "hello"
                
##                self.action = self.Intent.getAction()
##
##                if (BluetoothDevice.ACTION_FOUND.equals(self.action)
##                    self.device = self.intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
##                    name = self.device.getName();
##                    Toast.makeText(getApplicationContext()," Name:" + name, Toast.LENGTH_SHORT).show()
##
##
##
##                intent = BluetoothAdapter.ACTION_REQUEST_ENABLE
##
##                Activity.startActivityForResult(intent, 0);
##                

##                self.br.start()
##                
##                print BluetoothName
##                self.ids['hello'].text = firstDevice
##
##                self.br = self.BroadcastReceiver(self.onReceive(), self.Intent)
##                self.aDiscoverable = BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE
##                Activity.startActivityForResult(Intent(aDiscoverable), BluetoothAdapter.DISCOVERY_REQUEST)
##                
##                self.Filter = Context.IntentFilter(BluetoothDevice.ACTION_FOUND)
##                Context.RegisterReceiver(self.br, self.Filter)
##
##
##                if (self.BluetoothDevice.ACTION_FOUND == self.action):
##                        self.myBluetoothDevice = intent.getParcelableExtra(self.BluetoothDevice.EXTRA_DEVICE)
##                        name = myBluetoothDevice.getName()
##                        Toast.makeText(getApplicationContext()," Name:" + name, Toast.LENGTH_SHORT).show()

                self.myBTA = self.BluetoothAdapter.getDefaultAdapter()
                
                if self.myBTA is None:
                        popup = Popup(title='Sorry :(', content=Label(text='Didnt connect'), size_hint=(None, None), size=(400, 100))
                        popup.open()

                if(self.myBTA.isEnabled() == False):
                        intent = self.Intent()
                        intent.setAction(self.BluetoothAdapter.ACTION_REQUEST_ENABLE)
                        myActivity = cast('android.app.Activity', self.PythonActivity.mActivity)
                        myActivity.startActivity(intent)
                        
        def turnOnDiscovery (self):
                if(self.myBTA.isEnabled() == True):
                        if(self.myBTA.isDiscovering() == False):
                                intent = self.Intent()
                                intent.setAction(self.BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE)
                                myActivity = cast('android.app.Activity', self.PythonActivity.mActivity)
                                myActivity.startActivity(intent)
                        else:
                                popup = Popup(title='Bluetooth Info', content=Label(text='Bluetooth is Already Enabled'), size_hint=(None, None), size=(400, 100))
                                popup.open()   

        def findDevices (self):
                self.br = BroadcastReceiver(content = self.onReceive, actions=['main'], myFilter = self.BluetoothDevice.ACTION_FOUND)
                self.br.start()

                self.myBTA.startDiscovery()
 
        def onReceive(self, context, intent):
                action = intent.getAction();
                if (self.BluetoothDevice.ACTION_FOUND == action):
                        extras = intent.getParcelableExtra(self.BluetoothDevice.EXTRA_DEVICE)
                        device = cast('android.bluetooth.BluetoothDevice', extras)
                        deviceName = device.getName()
                        print deviceName
                        self.printLabel.text = deviceName
              
class RootWidget(FloatLayout):
        pass

root = RootWidget()
login = LoginScreen()

class assassinsApp (App):
        def build (self):
                root.add_widget(login)
                return root



if __name__ == '__main__':
        assassinsApp().run()
		
