# File name: main.py

from kivy.lang import Builder 
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivy.clock import Clock
from kivy.utils import platform
from jnius import autoclass

class BoxLayoutWidget(BoxLayout):

	def __init__(self, *args, **kwargs):

		BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
		BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
		BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
		UUID = autoclass('java.util.UUID')

		title = 'BlueTooth'

		super(BoxLayoutWidget, self).__init__(*args, **kwargs)

                text0 = self.ids['b0']

		BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
		

		text0.text=BluetoothAdapter.getName()


root = BoxLayoutWidget()

class BoxLayoutApp(App):
	def build (self):
		root.addWidget(root)

		return root
 
if __name__=="__main__":
   BoxLayoutApp().run()
