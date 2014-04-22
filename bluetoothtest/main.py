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
	BroadcastReceiver = autoclass('android.content.BroadcastReceiver')
	UUID = autoclass('java.util.UUID')
	Bundle = autoclass('android.os.Bundle')
	Intent = autoclass('android.content.Intent')
	Activity = autoclass('android.app.Activity')
	Context = autoclass('android.content.Context')

        title = 'BlueTooth'

        def __init__(self, **kwargs):
                super(BoxLayoutApp,self).__init__(**kwargs)

        def build(self):
		self.myBluetoothAdapter = self.BluetoothAdapter.getDefaultAdapter()
		print self.myBluetoothAdapter.getName()
		if self.myBluetoothAdapter.getName != None:
			print "device is BT Capable"
		else:
			print "device is not BT Capable"
		if self.myBluetoothAdapter.isEnabled() is False:
#			self.intent = self.Intent()
			print self.myBluetoothAdapter.isEnabled()
#			self.myBluetoothAdapter.startDiscovery()
#			self.enableBtIntent = self.Intent(self.BluetoothAdapter.ACTION_REQUEST_ENABLE)
#			self.getActivity().startActivityForResult(self.enableBtIntent, 1)
#		self.myBluetoothAdapter.disable() 
#		self.myBluetoothAdapter.startDiscovery()
		self.br =self.BroadcastReceiver(self.onReceive, actions=['Bluetooth_on'])
		self.br.start()

		print "I am here."
	        return BoxLayoutWidget()

	def onReceive(self,*args,**kwargs):
            	self.intent= self.Intent()
		self.action = self.intent.getAction()
            	#When discovery finds a device
            	if (BluetoothDevice.ACTION_FOUND.equals(action)):
                #Get the BluetoothDevice object from the Intent
                	self.myBluetoothDevice = self.BluetoothDevice
			self.myBluetoothDevice = self.intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE)
  			rssi = int(intent.getShortExtra(BluetoothDevice.EXTRA_RSSI,Short.MIN_VALUE))
	             	Toast.makeText(getApplicationContext(),"  RSSI: " + rssi + "dBm", Toast.LENGTH_SHORT).show()
 
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
