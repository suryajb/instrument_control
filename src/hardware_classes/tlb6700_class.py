import sys
import os
# sys.path.append('C:\\Users\\Lynn\\Desktop\\instrument_control\\libraries')
sys.path.append(os.getcwd()[:os.getcwd().find("instrument_control")+len("instrument_control")]+'\\libraries')
from libraries import *

class tlb6700(object):
	def __init__(self, **kwargs):
		super(tlb6700,self).__init__()
		self.tlb = Newport.USBComm.USB()
		self.answer = StringBuilder(64)
		self.ProductID = 4106
		self.DeviceKey = '6700 SN10064'

	def tlb_open(self):
		self.tlb.CloseDevices()
		self.tlb.OpenDevices(self.ProductID,True)

	def close(self):
		self.tlb.CloseDevices()

	def query(self,msg):
		self.answer.Clear()
		self.tlb.Query(self.DeviceKey,msg,self.answer)
		return self.answer.ToString()

	def set_power(self,P):
		# P is in units of mW
		self.query(f'SOURCE:POWER:DIODE {P}')
		power = self.query(f'SOURCE:POWER:DIODE?')
		return power

	def set_track(self,track=1):
		self.query(f'OUTPUT:TRACK {track}')
		t = self.query(f'OUTPUT:TRACK?')
		return t

	def set_lambda(self,λ):
		# units of nm
		self.query(f'SOURCE:WAVE {λ}')
		wavelength = self.query(f'SOURCE:WAVE?')
		return wavelength

	def set_scan_limits(self,λi,λf):
		# units of nm
		self.query(f'SOURCE:WAVE:START {λi}')
		self.query(f'SOURCE:WAVE:STOP {λf}')
		start = self.query(f'SOURCE:WAVE:START?'); stop = self.query(f'SOURCE:WAVE:STOP?')
		return start,stop

	def set_scan_speeds(self,forward,backward=0.1):
		self.query(f'SOURCE:WAVE:SLEW:FORWARD {forward}')
		self.query(f'SOURCE:WAVE:SLEW:RETURN {backward}')
		f = self.query(f'SOURCE:WAVE:SLEW:FORWARD?')
		b = self.query(f'SOURCE:WAVE:SLEW:RETURN?')
		return f,b

	def set_scan_number(self,scan_number):
		self.query(f'SOURCE:WAVE:DESSCANS {scan_number}')
		number = self.query(f'SOURCE:WAVE:DESSCANS?')
		return number

	def isFree(self):
		isFree = self.query('*OPC?')
		return int(isFree)

	def get_wavelength(self):
		return float(self.query('SENSE:WAVELENGTH'))

	def scan(self,signal):
		# signal is true or false
		if signal:
			self.query(f'OUTPUT:SCAN:START')
		else:
			self.query(f'OUTPUT:SCAN:STOP')