import os
import sys
sys.path.append(os.getcwd()[:os.getcwd().find("instrument_control")+len("instrument_control")]+'\\libraries')
from libraries import *
import pyvisa as pv
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from laser_control_gui import Ui_MainWindow
from time import perf_counter
from collections import deque
from pyqtgraph import GraphicsLayoutWidget
from PyQt5 import QtCore, QtGui, QtWidgets
import gc

class lasers_control(qtw.QMainWindow,Ui_MainWindow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.setupUi(self)
		self.connect_button.clicked.connect(self.make_connections)
		self.current_gpib_button.clicked.connect(self.current_connected_devices)
		self.configure_joysticks()

		self.update_wavelength_a_on = 0
		self.update_signals = {'monitor': 0,
							   'wavelength': {'a':0,'b':0},
							   'fine': {'a':0,'b':0}}
		
		self.monitor_data = np.empty
		self.d = {}
		self.plot_curves = {}
		self.wavelength = {}; self.output = {}
		self.last_df = pd.Series([])

		self.monitor_button.clicked.connect(self.update_monitor)
		self.curr_wavelength_a_button.clicked.connect(lambda: self.set_laser_wavelength(self.lasers['a'],'a',self.laser_a_type))
		self.curr_wavelength_b_button.clicked.connect(lambda: self.set_laser_wavelength(self.lasers['b'],'b',self.laser_b_type))
		self.curr_power_a_button.clicked.connect(lambda: self.set_laser_power(self.lasers['a'],'a',self.laser_a_type))
		self.curr_power_b_button.clicked.connect(lambda: self.set_laser_power(self.lasers['b'],'b',self.laser_b_type))
		self.append_n = 0
		self.scan_laser_a_button.clicked.connect(lambda: self.configure_and_scan('a'))
		self.scan_laser_b_button.clicked.connect(lambda: self.configure_and_scan('b'))
		
		self.wavelength_timers = {}
		self.fine_timers = {}
		self._queue = []
		self.curr_wavelength_label = {'a':self.curr_wavelength_a_label,'b':self.curr_wavelength_b_label}
		self.curr_fine_label = {'a':self.curr_fine_a_label,'b':self.curr_fine_b_label}
		self.wavelength_update_a_button.clicked.connect(lambda: self.update_santec_wavelength('a'))
		self.wavelength_update_b_button.clicked.connect(lambda: self.update_santec_wavelength('b'))
		self.fine_update_a_button.clicked.connect(lambda: self.update_santec_fine('a'))
		self.fine_update_b_button.clicked.connect(lambda: self.update_santec_fine('b'))

	def setup_scan_vars(self,a_or_b):
		self.start = {}; self.stop = {}; self.speed = {}; 
		self.sampling_rate = {}; self.total_points = {}
		self.return_to_set = {};
		if a_or_b == 'a':
			try:
				self.start['a'] = self.start_a_edit.text()
				self.stop['a'] = self.stop_a_edit.text()
				self.speed['a'] = self.speed_a_edit.text()
				self.sampling_rate['a'] = self.sampling_rate_a_edit.text()
				self.total_points['a'] = float(self.sampling_rate['a'])*(abs(float(self.start['a'])-float(self.stop['a'])) \
					/float(self.speed['a']))*1000
				self.return_to_set['a'] = self.return_a_checkbox.isChecked()
			except Exception as e:
				print(f"{e} at setup_scan_vars first try-except block")
		else:
			try:
				self.start['b'] = self.start_b_edit.text()
				self.stop['b'] = self.stop_b_edit.text()
				self.speed['b'] = self.speed_b_edit.text()
				self.sampling_rate['b'] = self.sampling_rate_b_edit.text()
				self.total_points['b'] = float(self.sampling_rate['b'])*(abs(float(self.start['b'])-float(self.stop['b'])) \
					/float(self.speed['b']))*1000
				self.return_to_set['b'] = self.return_b_checkbox.isChecked()
			except Exception as e:
				print(f"{e} at setup_scan_vars second try-except block")
		if a_or_b == 'a':
			try:
				self.total_points_a_edit.setText(f"{round(self.total_points['a']/1000)}")
				self.wavelength['a'] = np.linspace(float(self.start['a']),
												   float(self.stop['a']),
												   int(self.total_points['a']))
				self.output['a'] = np.zeros((len(self.ai_channels),len(self.wavelength['a'])))
			except Exception as e:
				print(f"{e} at setup_scan_vars third try-except block")
		else:
			try:
				self.total_points_b_edit.setText(f"{round(self.total_points['b']/1000)}")
				self.wavelength['b'] = np.linspace(float(self.start['b']),
												   float(self.stop['b']),
												   int(self.total_points['b']))
				self.output['b'] = np.zeros((len(self.ai_channels),len(self.wavelength['b'])))
			except Exception as e:
				print(f"{e} at setup_scan_vars fourth try-except block")
		
	def set_signals_zero(self):
		self.update_signals['monitor'] = 0
		self.update_signals['wavelength']['a'] = 0; self.update_signals['wavelength']['b'] = 0
		self.update_signals['fine']['a'] = 0; self.update_signals['fine']['b'] = 0

	def configure_and_scan(self,a_or_b):
		# self.update_signals['monitor'] = 0
		self.set_signals_zero()
		self.setup_scan_vars(a_or_b) # ends with setting wavelength and output initializations

		if self.laser_types[a_or_b] == 'Santec':
			speed = self.lasers[a_or_b].set_scan_speeds(self.speed[a_or_b])
			start,stop = self.lasers[a_or_b].set_scan_limits(self.start[a_or_b],self.stop[a_or_b])
			print(f'speed={speed},start={start},stop={stop}')
		else:
			forward,backward = self.lasers[a_or_b].set_scan_speeds(self.speed[a_or_b],self.speed[a_or_b])
			start,stop = self.lasers[a_or_b].set_scan_limits(self.start[a_or_b],self.stop[a_or_b])
			print(f'speed={forward},{backward},start={start},stop={stop}')

		self.scan_laser(a_or_b)

	def read_many_outputs(self,task,a_or_b):
		reader = AnalogMultiChannelReader(task.in_stream)
		reader.read_many_sample(data=self.output[a_or_b],
			number_of_samples_per_channel=int(self.total_points[a_or_b]),timeout=50)

	def scan_laser(self,a_or_b):
		if self.laser_types[a_or_b] == 'Santec':
			self.scan_santec(a_or_b)
		else:
			self.scan_newfocus(a_or_b)

	def start_scan_santec(self,laser):
		laser.scan()
		return

	def scan_santec(self,a_or_b):
		with nidaqmx.Task() as task: # needs to start a new task for for the analog input (ai) channel, one task
			# does not accept multiple channel types
			for ai in self.ai_channels:
				task.ai_channels.add_ai_voltage_chan(f"{ai}")
			task.timing.cfg_samp_clk_timing(rate=int(self.sampling_rate[a_or_b])*1000,
				sample_mode=AcquisitionType.FINITE,
				samps_per_chan=int(self.total_points[a_or_b]))
			task.triggers.start_trigger.cfg_dig_edge_start_trig(\
				f"{self.timing_channels[a_or_b]}", # /{self.daq_device}/{self.timing_channel}
 				Edge.RISING)
			threads = []
			t1 = Thread(target=self.read_many_outputs,args=(task,a_or_b,))
			t2 = Thread(target=self.start_scan_santec,args=(self.lasers[a_or_b],))
			t1.start()
			t2.start()
			start_time = time.time()
			threads.append(t1); threads.append(t2)
			for t in threads:
				t.join()
			real_time_taken = time.time()-start_time-1

		print(f'Santec real scan time = {real_time_taken}')
		while not(self.lasers[a_or_b].isFree()):
			sleep(1)

		if self.return_to_set[a_or_b]:
			print(f'set return wavelength {self.return_to_set[a_or_b]}')
			sleep(1)
			self.lasers[a_or_b].set_lambda(self.start[a_or_b])

		print('Santec is free')
		print(self.output[a_or_b])

		columns = ['wavelength'] + [f'{i}' for i in self.ai_channels]
		df = pd.DataFrame(np.concatenate((np.array([self.wavelength[a_or_b]]),self.output[a_or_b])).T,columns=columns)
		print(f'scan complete, real time = {real_time_taken}s')

		# if self.save_data_checkbox.isChecked():
		# 	filepath = self.filelocation_edit.toPlainText().split('\\')
		# 	filename = ('\\').join(filepath)
		# 	filepath = filepath[:-1]

		# 	append = f'_{self.append_n:02}'
		# 	if filename in glob.glob(("\\").join(filepath)+"\\*"):
		# 		newfilename = ('.').join(filename.split('.')[:-1]) + append + '.' + filename.split('.')[-1]
		# 		while newfilename in glob.glob(("\\").join(filepath)+"\\*"):
		# 			self.append_n += 1
		# 			append = f'_{self.append_n:02}'
		# 			newfilename = ('.').join(filename.split('.')[:-1]) + append + '.' + filename.split('.')[-1]
		# 	else:
		# 		newfilename = filename
		# 	self.append_n = 0

		# 	df.to_csv(newfilename,index=False)

		# self.last_df = df
		
		# _logplot = self.get_logplot_check(a_or_b)
		# self.plot_last(_logplot)
		if self.save_data_checkbox.isChecked():
			filepath = self.filelocation_edit.toPlainText().split('\\')
			filename = ('\\').join(filepath)
			filepath = filepath[:-1]

			append = f'_{self.append_n:02}'
			if filename in glob.glob(("\\").join(filepath)+"\\*"):
				newfilename = ('.').join(filename.split('.')[:-1]) + append + '.' + filename.split('.')[-1]
				while newfilename in glob.glob(("\\").join(filepath)+"\\*"):
					self.append_n += 1
					append = f'_{self.append_n:02}'
					newfilename = ('.').join(filename.split('.')[:-1]) + append + '.' + filename.split('.')[-1]
			else:
				newfilename = filename
			self.append_n = 0

			IR_newfilename = newfilename[0:-4] + '_IR' + newfilename[-4:]
			others_newfilename = newfilename[0:-4] + '_others' + newfilename[-4:]
			df[['wavelength',self.ai_channels[0]]].to_csv(IR_newfilename,header=False,
														  sep='\t',index=False)
			df[['wavelength']+self.ai_channels[1:]].to_csv(others_newfilename,header=False,
														  sep='\t',index=False)

		self.last_df = df

		_logplot = self.get_logplot_check(a_or_b)
		self.plot_last(_logplot)

		return

	def plot_last(self,logPlot=None):
		if logPlot is None: # need this because when turn off monitor, qt needs to know what the last setting was
			logPlot = self._logplot_last
		self._logplot_last = logPlot
		self.plots_view.clear()
		p = {}
		for i in range(len(self.ai_channels)):
			p[i] = self.plots_view.addPlot(title=f'{self.last_df.columns[1+i]}')
			if logPlot:
				p[i].setLogMode(False, True)
			p[i].plot(self.last_df.wavelength,
					  self.last_df[self.last_df.columns[1+i]].values,
					  pen=(i,len(self.ai_channels)))
			self.plots_view.nextRow()

	def start_scan_newfocus(self,task):
		# send high then low signal to laser (a pulse), which will trigger laser to start scan at the falling edge
		# use this instead of the built in laser scan function because this can be used to trigger the start of 
		# DAQ multidata acquisition
		task.write(True) 
		sleep(1)
		print('start scan')
		task.write(False)

	def get_logplot_check(self,a_or_b):
		if a_or_b == 'a':
			return self.plot_log_a_checkbox.isChecked()
		else:
			return self.plot_log_b_checkbox.isChecked()

	def scan_newfocus(self,a_or_b):
		self.lasers[a_or_b].set_track()
		self.lasers[a_or_b].set_lambda(self.start[a_or_b])
		while not(self.lasers[a_or_b].isFree()):
			sleep(1)

		with nidaqmx.Task() as task1:
			do = task1.do_channels.add_do_chan(f'{self.timing_channels[a_or_b]}', # {self.timing_channel}/line0:7
				line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
			# task1.write(True) 
			with nidaqmx.Task() as task2: # needs to start a new task for for the analog input (ai) channel, one task
			# does not accept multiple channel types
				for ai in self.ai_channels:
					task2.ai_channels.add_ai_voltage_chan(f"{ai}")
				task2.timing.cfg_samp_clk_timing(rate=int(self.sampling_rate[a_or_b])*1000,
					sample_mode=AcquisitionType.FINITE,
					samps_per_chan=int(self.total_points[a_or_b]))
				task2.triggers.start_trigger.cfg_dig_edge_start_trig(f"{self.timing_channels[a_or_b]}",
					Edge.FALLING)

				# need to use multi-threading because we want to
				# start the scan during the DAQ function for acquiring data, which will occupy the native thread.  If 
				# multithreads are not used, then the laser will start scan AFTER the DAQ has timed-out.
				threads = []
				t1 = Thread(target=self.read_many_outputs,args=(task2,a_or_b,)) 
				t2 = Thread(target=self.start_scan_newfocus,args=(task1,))
				t1.start(); t2.start()
				start_time = time.time()
				threads.append(t1); threads.append(t2)
				for t in threads:
					t.join()
				real_time_taken = time.time()-start_time-1

		if not(self.return_to_set[a_or_b]):
			print('returning to stop wavelength')
			sleep(real_time_taken+1)
			self.lasers[a_or_b].set_lambda(self.stop[a_or_b])

		while not(self.lasers[a_or_b].isFree()):
			sleep(1)

		columns = ['wavelength'] + [f'{i}' for i in self.ai_channels]
		df = pd.DataFrame(np.concatenate((np.array([self.wavelength[a_or_b]]),self.output[a_or_b])).T,columns=columns)
		print(f'scan complete, real time = {real_time_taken}s')

		if self.save_data_checkbox.isChecked():
			filepath = self.filelocation_edit.toPlainText().split('\\')
			filename = ('\\').join(filepath)
			filepath = filepath[:-1]

			append = f'_{self.append_n:02}'
			if filename in glob.glob(("\\").join(filepath)+"\\*"):
				newfilename = ('.').join(filename.split('.')[:-1]) + append + '.' + filename.split('.')[-1]
				while newfilename in glob.glob(("\\").join(filepath)+"\\*"):
					self.append_n += 1
					append = f'_{self.append_n:02}'
					newfilename = ('.').join(filename.split('.')[:-1]) + append + '.' + filename.split('.')[-1]
			else:
				newfilename = filename
			self.append_n = 0

			IR_newfilename = newfilename[0:-4] + '_IR' + newfilename[-4:]
			others_newfilename = newfilename[0:-4] + '_others' + newfilename[-4:]
			df[['wavelength',self.ai_channels[0]]].to_csv(IR_newfilename,header=False,
														  sep='\t',index=False)
			df[['wavelength']+self.ai_channels[1:]].to_csv(others_newfilename,header=False,
														  sep='\t',index=False)

		self.last_df = df

		_logplot = self.get_logplot_check(a_or_b)
		self.plot_last(_logplot)

		return

	def set_laser_power(self,laser,a_or_b,laserType):
		if laserType == 'Santec':
			if a_or_b == 'a':
				power = self.curr_power_a_edit.text()
				curr_power = laser.set_power(power)
				self.curr_power_a_label.setText(f'{curr_power}')
			else:
				power = self.curr_power_b_edit.text()
				curr_power = laser.set_power(power)
				self.curr_power_b_label.setText(f'{curr_power}')
		else:
			if a_or_b == 'a':
				power = self.curr_wavelength_a_edit.text()
				curr_power = laser.set_power(power)
				self.curr_power_a_label.setText(f'{curr_power}')
			else:
				power = self.curr_wavelength_b_edit.text()
				curr_power = laser.set_power(power)
				self.curr_power_b_label.setText(f'{curr_power}')

	def set_laser_wavelength(self,laser,a_or_b,laserType):
		if laserType == 'Santec':
			if a_or_b == 'a':
				λ = self.curr_wavelength_a_edit.text()
				curr = laser.set_lambda(λ)
				self.curr_wavelength_a_label.setText(f'{curr}')
			else:
				λ = self.curr_wavelength_b_edit.text()
				curr = laser.set_lambda(λ)
				self.curr_wavelength_b_label.setText(f'{curr}')
		else:
			if a_or_b == 'a':
				λ = self.curr_wavelength_a_edit.text()
				laser.set_track()
				curr = laser.set_lambda(λ)
				self.curr_wavelength_a_label.setText(f'{curr}')
			else:
				λ = self.curr_wavelength_b_edit.text()
				laser.set_track()
				curr = laser.set_lambda(λ)
				self.curr_wavelength_b_label.setText(f'{curr}')
			
	def configure_joysticks(self):
		self.joystick_1.setFixedWidth(30)
		self.joystick_1.setFixedHeight(30)
		self.joystick_2.setFixedWidth(30)
		self.joystick_2.setFixedHeight(30)
		self.joystick_3.setFixedWidth(30)
		self.joystick_3.setFixedHeight(30)
		self.joystick_4.setFixedWidth(30)
		self.joystick_4.setFixedHeight(30)
		self.joysticks_wavelength = {'a':self.joystick_1,'b':self.joystick_3}
		self.joysticks_fine = {'a':self.joystick_2,'b':self.joystick_4}

	def configure_daq(self):
		try:
			self.ai_channels = self.aichannel_text.text().split(',')
			self.daq_device = self.daq_device_edit.text()
			self.timing_channel = self.timing_edit.text().split(',')
			self.timing_channels = {}
			if len(self.timing_channel) == 1:
				# make into iterable if not already, this will help code find all user designed channels (multi or single) 
				self.timing_channels['a'] = f'/{self.daq_device}/{self.timing_channel}'
				self.timing_channels['b'] = f'/{self.daq_device}/{self.timing_channel}'
			else:
				self.timing_channels['a'] = f'/{self.daq_device}/{self.timing_channel[0]}'
				self.timing_channels['b'] = f'/{self.daq_device}/{self.timing_channel[1]}'
			if type(self.ai_channels) != list:
				# make into iterable if not already, this will help code find all user designed channels (multi or single) 
				self.ai_channels = [self.ai_channels] 
			temp_ai_channels = []
			for ai in self.ai_channels:
				temp_ai_channels.append(self.daq_device+'/'+ai)
			self.ai_channels = temp_ai_channels
		except Exception as e:
			print(str(e))

	def connect_daq(self):
		# initiate connection with daq and output a test data point
		self.configure_daq()
		try:
			with nidaqmx.Task() as task:
				for ai in self.ai_channels:
					task.ai_channels.add_ai_voltage_chan(f"{ai}")
				data_point = task.read()
				if type(data_point) == list:
					data_point = [round(d,5) for d in data_point]
				else:
					data_point = round(data_point,5)
			return f'{data_point}'
		except Exception as e:
			qtw.QMessageBox.critical(self,'Failed', f'Failed to connect to DAQ: {str(e)}')

	def connect_laser(self,a_or_b,laser_type,code):
		# Connect to one laser
		try:
			if  laser_type == 'Santec':
				self.lasers[a_or_b] = tsl710(gpib=code)
				if a_or_b == 'a':
					self.power_a_label.setText('dBm')
				else:
					self.power_b_label.setText('dBm')
				return self.lasers[a_or_b].identity['model'] + ' ' + self.lasers[a_or_b].identity['SN']
			else:
				self.lasers[a_or_b] = tlb6700()
				self.lasers[a_or_b].DeviceKey = code
				self.lasers[a_or_b].tlb_open()
				out = self.lasers[a_or_b].query('*IDN?')
				if a_or_b == 'a':
					self.power_b_label.setText('mW')
				else:
					self.power_b_label.setText('mW')
				return out.split(' ')[1]+' '+out.split(' ')[-1]
				
		except Exception as e:
			return f'Laser {a_or_b.upper()} not connected: {str(e)}'

	def make_connections(self):
		# Connect DAQ
		try:
			daq_msg = 'DAQ output: '+self.connect_daq()
		except Exception as e:
			daq_msg = 'DAQ not connected'

		self.lasers = {}
		self.a_gpib_serial = self.laser_a_gpib_edit.text()
		self.b_gpib_serial = self.laser_b_gpib_edit.text()
		self.laser_a_type = self.laser_a_connections_combobox.currentText()
		self.laser_b_type = self.laser_b_connections_combobox.currentText()
		self.laser_types = {'a':self.laser_a_type,'b':self.laser_b_type}

		# Connect Lasers
		a_msg = self.connect_laser('a',laser_type=self.laser_a_type,
								   code=self.a_gpib_serial)
		b_msg = self.connect_laser('b',laser_type=self.laser_b_type,
								   code=self.b_gpib_serial)

		self.connections_edit.setText(daq_msg+'\n'+a_msg+'\n'+b_msg)

	def current_connected_devices(self):
		rm = pv.ResourceManager()
		resources = rm.list_resources()
		qtw.QMessageBox.information(self,'Connected Resources:', f"{resources} \n If New Focus Controller, syntax is similar to:\n'6700 SN10064'")

	def plot_daq_signals(self,monitor_len=400):
		# we want a moving array of data points plotted to get a scrolling effect in normal transmission monitors
		# the best way to do this is to implement a queue using collections deque, since the popping and inserting 
		# operations are optimized if we use deque
		if not(self.update_signals['monitor']):
			self.timer.stop()
			self.timer.deleteLater()

		with nidaqmx.Task() as task:
			for ai in self.ai_channels:
				task.ai_channels.add_ai_voltage_chan(f"{ai}")
			data_point = task.read()

		if type(data_point) == list:
			data_point = [round(d,7) for d in data_point]
		else:
			data_point = [round(data_point,7)]

		if len(self.q[0]) < monitor_len:
			for i in range(len(self.ai_channels)):
				self.q[i].append(data_point[i])
				self.plot_curves[i].setData(np.array(list(self.q[i])))
		else:
			for i in range(len(self.ai_channels)):
				self.q[i].append(data_point[i])
				self.q[i].popleft()
				self.plot_curves[i].setData(np.array(list(self.q[i])))
		return

	def update_monitor(self):

		self.update_signals['monitor'] = not(self.update_signals['monitor'])
		self.timer = qtc.QTimer()
		if self.update_signals['monitor']:
			self.q = {} # deque([])
			for i in range(len(self.ai_channels)):
				self.q[i] = deque([])

			if not(self.last_df.empty) or not(self.d) or (len(self.d)!=len(self.ai_channels)): # if more ai_channels were set
			# or if d doesn't exist, 
				self.plots_view.clear()
				for i in range(len(self.ai_channels)):
					self.d[i] = self.plots_view.addPlot()
					self.plot_curves[i] = self.d[i].plot(pen=(i,len(self.ai_channels)))
					self.plots_view.nextRow()
			# if empty, then can comfortably plot, but if not must clear first
			self.timer.timeout.connect(lambda: self.plot_daq_signals())
			self.timer.start(50)
		else:
			self.timer.stop()
			if not(self.last_df.empty):
				self.plot_last()
			self.timer.deleteLater() # must delete timer otherwise memory leakage will cause
			# huge slowdown of the code after Mon on/off button has been pressed multiple times.
		return

	def set_santec_wavelength(self,a_or_b):
		if not(self.update_signals['wavelength'][a_or_b]):
			self.wavelength_timers[a_or_b].stop()
			self.wavelength_timers[a_or_b].deleteLater()
		dx,dy = self.joysticks_wavelength[a_or_b].getState()
		self.currWavelength += dx*self.wavelength_stepsize[a_or_b]
		if self.currWavelength>self.lasers[a_or_b].wavelength_limits[1]:
			self.currWavelength = self.lasers[a_or_b].wavelength_limits[1]
		if self.currWavelength<self.lasers[a_or_b].wavelength_limits[0]:
			self.currWavelength = self.lasers[a_or_b].wavelength_limits[0]
		set_wavelength = self.lasers[a_or_b].set_lambda(self.currWavelength)
		self.curr_wavelength_label[a_or_b].setText(f'{set_wavelength}')


	def update_santec_wavelength(self,a_or_b):
		self.update_signals['wavelength'][a_or_b] = not(self.update_signals['wavelength'][a_or_b])
		self.wavelength_timers[a_or_b] = qtc.QTimer()
		self.wavelength_stepsize = {} 
		if self.update_signals['wavelength'][a_or_b]:
			if self._queue:
				which_laser = self._queue.pop()
				if which_laser == a_or_b:
					self.update_signals['fine'][which_laser] = 0
				else:
					self.update_signals['wavelength'][which_laser] = 0
					self.update_signals['fine'][which_laser] = 0

			self.wavelength_stepsize[a_or_b] = float(self.wavelength_stepsize_a_edit.text())
			self.currWavelength = float(self.lasers[a_or_b].get_lambda())
			self.wavelength_timers[a_or_b].timeout.connect(lambda: self.set_santec_wavelength(a_or_b))
			self.wavelength_timers[a_or_b].start(100)
			self._queue.append(a_or_b)
		else:
			self._queue.pop()
			self.wavelength_timers[a_or_b].stop()
			self.wavelength_timers[a_or_b].deleteLater()
		return

	def set_santec_fine(self,a_or_b):
		if not(self.update_signals['fine'][a_or_b]):
			self.fine_timers[a_or_b].stop()
			self.fine_timers[a_or_b].deleteLater()
		dx,dy = self.joysticks_fine[a_or_b].getState()
		self.currFine += dx*self.fine_stepsize[a_or_b]
		if self.currFine>self.lasers[a_or_b].fine_limits[1]:
			self.currFine = self.lasers[a_or_b].fine_limits[1]
		if self.currFine<self.lasers[a_or_b].fine_limits[0]:
			self.currFine = self.lasers[a_or_b].fine_limits[0]
		set_fine = self.lasers[a_or_b].set_fine(self.currFine)
		self.curr_fine_label[a_or_b].setText(f'{set_fine}')

	def update_santec_fine(self,a_or_b):
		self.update_signals['fine'][a_or_b] = not(self.update_signals['fine'][a_or_b])
		self.fine_timers[a_or_b] = qtc.QTimer()
		self.fine_stepsize = {} 
		if self.update_signals['fine'][a_or_b]:
			if self._queue:
				which_laser = self._queue.pop()
				if which_laser == a_or_b: # this means the same laser has wavelength on, so need
				# to turn it off before enabling fine tuning
					self.update_signals['wavelength'][which_laser] = 0
				else:
					self.update_signals['wavelength'][which_laser] = 0
					self.update_signals['fine'][which_laser] = 0

			self.fine_stepsize[a_or_b] = float(self.fine_stepsize_a_edit.text())
			self.currFine = float(self.lasers[a_or_b].get_fine())
			self.fine_timers[a_or_b].timeout.connect(lambda: self.set_santec_fine(a_or_b))
			self.fine_timers[a_or_b].start(100)
			self._queue.append(a_or_b)
		else:
			self._queue.pop()
			self.fine_timers[a_or_b].stop()
			self.fine_timers[a_or_b].deleteLater()
		return

	def closeEvent(self,event):
		# this method is used for properly terminating connection with laser
		reply = qtw.QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
				qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.No)
		if reply == qtw.QMessageBox.Yes:
			for k,v in self.lasers.items():
				v.close()
			event.accept()
			print('Window closed')
		else:
			event.ignore()

if __name__ == '__main__':
	app = qtw.QApplication(sys.argv)
	window = lasers_control()
	window.show()
	app.exec_()
