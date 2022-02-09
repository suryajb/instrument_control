from libraries import *

class YDFA():
	def __init__(self, port='COM7'):
		self.port = port
		self.timeout = 1
		self.baudrate = 9600
		self.allow_ = 0 # if allow_ is 0, the program will not enable the laser diodes
		
	def read(self):
		with serial.Serial(timeout=1) as ser:
			ser.baudrate = self.baudrate
			ser.port = self.port
			ser.open()
			msg = 0
			self.msg_chain = []
			ser.write(b'READ\r\n')
			while True:
				msg = ser.readline()
				if not(msg):
					break
				self.msg_chain.append(msg.decode())
		return self.msg_chain

	def get_inputpower(self,read=1):
		if read:
			self.read()
		for m in self.msg_chain:
			if 'Input Power' in m:
				msg = m
		if 'LOW' in msg:
			self.allow_ = 0
			self.input_power = 'LOW'
			return 'input power low'
		elif ('Input Power' in msg) and ('LOW' not in msg):
			self.allow_ = 1
			msg = msg.replace(' +',' ')
			for m in msg.split(' '):
				try:
					self.input_power = str(float(m)) # [m for m in msg.split(' ') if m.isdigit()][-1]
				except:
					pass
			return self.input_power
		else:
			self.input_power = 'ERROR'
			return 'incorrect read'

	def get_ld1_current(self,read=1):
		if read:
			self.read()
		for m in self.msg_chain:
			if 'Pump 1 Current' in m:
				msg = m
		self.ld1_current = [m for m in msg.split(' ') if m.isdigit()][-1]
		return self.ld1_current

	def get_ld2_current(self,read=1):
		if read:
			self.read()
		for m in self.msg_chain:
			if 'Pump 2 Current' in m:
				msg = m
		self.ld2_current = [m for m in msg.split(' ') if m.isdigit()][-1]
		return self.ld2_current

	def get_bp(self,read=1): # get booster power
		if read:
			self.read()
		for m in self.msg_chain:
			if 'Power Set' in m:
				msg = m[0:-2]
		self.bp = [m for m in msg.split(' ') if m.isdigit()][-1]
		return self.bp

	def get_enable_status(self,read=1):
		if read:
			self.read()
		for m in self.msg_chain:
			if 'Enable' in m:
				msg = m[0:-2]
		print([m for m in msg.split(' ')])
		self.enable_status = [m for m in msg.split(' ')][-2]
		return self.enable_status

	def set_ld1(self,val=770):
		self.get_inputpower()

		if not(self.allow_):
			return 'input low'

		if val<1 or val>850:
			return 'range err'
		else:
			with serial.Serial(timeout=1) as ser:
				ser.baudrate = self.baudrate
				ser.port = self.port
				ser.open()
				write_msg = f'SETLD1:{val:04}\r\n'.encode()
				ser.write(write_msg)
				sleep(2)
		return self.get_ld1_current()

	def set_ld2(self,val=1050):
		self.read()
		self.get_inputpower(0)

		if not(self.allow_):
			return 'input low'
		if int(self.get_ld1_current(0))<500:
			return 'LD1 low'

		if val<1 or val>1200:
			return 'range err'
		else:
			with serial.Serial(timeout=1) as ser:
				ser.baudrate = self.baudrate
				ser.port = self.port
				ser.open()
				write_msg = f'SETLD2:{val:04}\r\n'.encode()
				ser.write(write_msg)
				sleep(2)
		return self.get_ld2_current()

	def set_bp(self,val=1):
		# self.read()
		# self.get_ld1_current()
		# self.get_ld2_current()

		if int(val)<1 or int(val)>165:
			return 'ERROR'
		else:
			with serial.Serial(timeout=1) as ser:
				ser.baudrate = self.baudrate
				ser.port = self.port
				ser.open()
				write_msg = f'SETBP:{val:03}\r\n'.encode()
				ser.write(write_msg)
				sleep(2)
			ret = self.get_bp()
			return ret

	def get_bp_status(self,read=1):
		if read:
			self.read()
		for m in self.msg_chain:
			if 'Enable' in m:
				msg = m
		if 'ON' in msg:
			self.bp_status = 'ON'
		else:
			self.bp_status = 'OFF'
		return self.bp_status

	def enable_bp(self):
		self.read()
		self.get_ld1_current(0)
		self.get_ld2_current(0)
		self.get_bp_status(0)

		if int(self.ld1_current)<700 or int(self.ld2_current)<1000:
			return 'BP Off'
		else:
			with serial.Serial(timeout=1) as ser:
				ser.baudrate = self.baudrate
				ser.port = self.port
				ser.open()
				if self.bp_status == "OFF":
					write_msg = f'SETBS:1\r\n'.encode()
				elif self.bp_status == "ON":
					write_msg = f'SETBS:0\r\n'.encode()
				else:
					return 'ERROR'
				ser.write(write_msg)
				sleep(4)
		return 'BP '+self.get_bp_status()

	def get_status(self):
		self.read()
		self.get_ld1_current(0)
		self.get_ld2_current(0)
		self.get_bp(0)
		self.get_inputpower(0)
		self.get_bp_status(0)
		return self.ld1_current,self.ld2_current,self.bp,self.input_power,self.bp_status