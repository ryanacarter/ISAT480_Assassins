
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
                self.BroadcastReceiver = autoclass('android.content.BroadcastReceiver')
                self.UUID = autoclass('java.util.UUID')
                self.Bundle = autoclass('android.os.Bundle')
                self.Intent = autoclass('android.content.Intent')
                self.Activity = autoclass('android.app.Activity')
                self.Context = autoclass('android.content.Context')
                
                
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

                
                self.br = self.BroadcastReceiver(self.onReceive, actions=['Bluetooth_on'])
                self.br.start()
##                
        def onReceive(self, *args, **kwargs):

                self.action = intent.getAction()
                if (self.BluetoothDevice.ACTION_FOUND == self.action):
                        self.myBluetoothDevice = intent.getParcelableExtra(self.BluetoothDevice.EXTRA_DEVICE)
                        name = myBluetoothDevice.getName()
                        Toast.makeText(getApplicationContext()," Name:" + name, Toast.LENGTH_SHORT).show()




   
              
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
		
