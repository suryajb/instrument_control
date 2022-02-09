import sys
sys.path.append('C:\\Users\\Lynn\\Desktop\\instrument_control\\libraries')
from libraries import *
import pyvisa as pv

class yokogawa():
	def __init__(self,gpib=None,model='AQ6376',inst=None):
		assert((gpib is not None) or (inst is not None)), 'gpib must be set or connnection must be inputted'
		self.gpib = gpib
		self.rm = pv.ResourceManager()
		self.connect(inst)
		self.model = self.identity['model']
		assert(self.identity['name'] == 'YOKOGAWA'), f"gpib address not YOKOGAWA, it's {self.identity['name']}"
		assert(self.model == model), 'gpib pointing to different model'
		print(f'{self.model} connected')

		self.yokogawa_sense = {'0':'NHLD', 
							   '1':'NAUT',
							   '2':'MID',
							   '3':'HIGH1',
							   '4':'HIGH2',
							   '5':'HIGH3',
							   '6':'NORMAL'}

		self._trace = 'tra'
		self.models_range = {'AQ6376':[1500,3400],'AQ6374':[350,1750]}

	def connect(self,inst):
		if inst is None:
			try:
				self.inst = self.rm.open_resource(f'GPIB0::{self.gpib}::INSTR')
				output = self.inst.query("*IDN?")[:-1].split(',')
				self.identity = {'name':output[0],'model':output[1],'SN':output[2]}
			except Exception as e:
				print(f'{str(e)}')
		else:
			try:
				self.inst = inst
				output = self.inst.query("*IDN?")[:-1].split(',')
				self.identity = {'name':output[0],'model':output[1],'SN':output[2]}
			except Exception as e:
				print(f'{str(e)}')

	def close(self):
		self.inst.close()

	def query(self,input):
		try: 
			output = self.inst.query(input)
			return output[:-1]
		except Exception as e:
			print(str(e))

	def write(self,input):
		try: 
			output = self.inst.write(input)
			return output
		except Exception as e:
			print(str(e))

	def get_trace_data(self):
		try:
			self.xdata = 1e9*np.array(list(map(float,self.inst.query(f':trace:x? {self._trace}').split(','))))
			self.ydata = np.array(list(map(float,self.inst.query(f':trace:y? {self._trace}').split(','))))
			set_len = self.inst.query(f':trace:snumber? {self._trace}')
			assert(self.xdata.shape[0]==int(set_len)), f'real length ({self.xdata.shape[0]}) not equal to set length ({set_len})'
			self.data = pd.DataFrame({'S':self.ydata,'wavelength':self.xdata})
			return self.data
		except Exception as e:
			print(str(e))

	def define_settings(self,start,stop,points,sensitivity):
		try:
			self.write(f':sense:wavelength:start {start}nm')
			self.write(f':sense:wavelength:stop {stop}nm')
			self.write(f':sense:sweep:points {points}')
			self.write(f':sense:sense {sensitivity}')
			self.settings = {'start':self.query(f':sense:wavelength:start?'),
							'stop':self.query(f':sense:wavelength:stop?'),
							'points':self.query(f':sense:sweep:points?'),
							'sensitivity':self.yokogawa_sense[self.query(f':sense:sense?')]}
			return self.settings
		except Exception as e:
			print(str(e))

	def start_trace(self,scan_type):
		if scan_type == 'repeat':
			self.write(f':initiate:smode 2')
			self.write(':initiate')
			self._free = 0
			return 'repeat'
		elif scan_type == 'single':
			self.write(f':initiate:smode 1')
			self.write(':initiate')
			self._free = 0
			while not(self._free):
				try:
					int(self.query(':trace:data:snumber? tra'))
					self._free = 1
				except:
					sleep(2)
			print('yokogawa is free')
			return 'single'
		elif (scan_type == 'abort') or (scan_type == 'stop'):
			self.write(':abort')
			while not(self._free):
				try:
					int(self.query(':trace:data:snumber? tra'))
					self._free = 1
				except:
					sleep(2)
			print('yokogawa is free')
			return 'aborted'
		else:
			raise ValueError("invalid scan type, choose between: {repeat, single, stop, abort}")

