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
                super(BoxLayoutWidget, self).__init__(*args, **kwargs)

                text0 = self.ids['b0']
		text1 = self.ids['b1']
		text2 = self.ids['b2']
		text3 = self.ids['b3']
		text4 = self.ids['b4']
		text5 = self.ids['b5']

		text0.text='0_Hello'
		text1.text='1_World!'
		text2.text='2_Hello'
		text3.text='3_World!'
		text4.text='4_Hello'
                text5.text='5_World!'


class BoxLayoutApp(App):

	BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
	BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
	BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
	UUID = autoclass('java.util.UUID')

	Intent =autoclass('android.content.Intent')
	Short = autoclass('java.lang.Short')

        title = 'BlueTooth'

        def __init__(self, **kwargs):
                super(BoxLayoutApp,self).__init__(**kwargs)

        def build(self):
                self.recv_stream, self.send_stream = self.get_socket_stream('ubuntu-0')
                return BoxLayoutWidget()
 
        def send(self, cmd):
                self.send_stream.write('{}\n'.format(cmd))
                self.send_stream.flush()
 
        def reset(self, btns):
                for btn in btns:
                        btn.state = 'normal'
                self.send("it's me")

	def get_socket_stream(self, name):
#		self.paired_devices = self.BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
#		print name, self.paired_devices
#		self.socket = None
		self.BluetoothAdapter.startDiscovery()
#   		for device in self.discovered_devices:
#        		if device.getName() == name:
                print name
            			#self.socket = device.createRfcommSocketToServiceRecord(self.UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
		self.intent=self.Intent()
		self.intent.getParcelableExtra(self.BluetoothDevice.EXTRA_DEVICE)
		print self.intent.getShortExtra(self.BluetoothDevice.EXTRA_RSSI,self.Short.MIN_VALUE)
            			#recv_stream = self.socket.getInputStream()
            			#send_stream = self.socket.getOutputStream()
#            			break
    		#self.socket.connect()
    		#return recv_stream, send_stream
 
##	def change_button_text(self,*args, **kwargs):
##		text1=self.root.ids['button1']
##		text2=self.root.ids['label1']
##
##		if text1.text=='Hello':
##			text1.text='World!'
##			text2.text='Hello'
##		else:
##			text1.text='Hello'
##			text2.text='World!'

 
if __name__=="__main__":
   BoxLayoutApp().run()
