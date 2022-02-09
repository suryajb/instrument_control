import sys
import os
# sys.path.append('C:\\Users\\Lynn\\Desktop\\instrument_control\\libraries')
sys.path.append(os.getcwd()[:os.getcwd().find("instrument_control")+len("instrument_control")]+'\\libraries')
from libraries import *
import pyvisa as pv

class tsl710():
	def __init__(self,gpib=None,inst=None):
		assert((gpib is not None) or (inst is not None)), 'gpib must be set or connnection must be inputted'
		self.gpib = gpib
		self.rm = pv.ResourceManager()
		self.connect(inst)
		self.wavelength_limits = [1480.0,1640.0]
		self.fine_limits = [-99.0,99.0]

	def connect(self,inst):
		if inst is None:
			self.inst = self.rm.open_resource(f'GPIB0::{self.gpib}::INSTR')
			output = self.inst.query("*IDN?")[:-1].split(',')
			self.identity = {'name':output[0],'model':output[1],'SN':output[2]}
		else:
			self.inst = inst
			output = self.inst.query("*IDN?")[:-1].split(',')
			self.identity = {'name':output[0],'model':output[1],'SN':output[2]}

	def query(self,input):
		output = self.inst.query(input)
		return output

	def write(self,input):
		self.inst.write(input)

	def close(self):
		self.inst.close()

	def set_lambda(self,λ): 
		# set wavelength in units of nm
		self.write(f':wavelength {λ}')
		return self.query(f':wavelength?')

	def get_lambda(self): 
		return self.query(f':wavelength?')

	def set_fine(self,fine):
		self.write(f'wavelength:fine {fine}')
		return self.query(f':wavelength:fine?')

	def get_fine(self):
		return self.query(f':wavelength:fine?')

	def fine_disable(self):
		self.write(f':wavelength:fine:disable')

	def set_scan_mode(self,mode):
		# 0: step operation, one-way
		# 1: continuous operation, one-way
		# 2: step operation, two-way
		# 3: continuous operation, two-way
		self.write(f':wavelength:sweep:mode {mode}')
		return self.query(f':wavelength:sweep:mode?')

	def set_scan_limits(self,λi,λf):
		self.write(f':wavelength:sweep:start {λi}')
		self.write(f':wavelength:sweep:stop {λf}')
		start = self.query(f':wavelength:sweep:start?')
		stop = self.query(f':wavelength:sweep:stop?')
		return start,stop

	def set_scan_speeds(self,speed):
		self.write(f':wavelength:sweep:speed {speed}')
		return self.query(f':wavelength:sweep:speed?')

	def isFree(self):
		isFree = self.query('*OPC?')
		return int(isFree)

	def scan(self,signal=1):
		# signal is true or false
		if signal:
			self.write(f':wavelength:sweep 1')
			# print(self.query(':trig:outp?'))
		else:
			self.write(f':wavelength:sweep: 0')

	def set_power(self,P):
		# P is in units of dbm
		self.write(f':power {P}')
		return self.query(f':power?')