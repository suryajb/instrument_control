import os
import sys
sys.path.append(os.getcwd()[:os.getcwd().find("instrument_control")+len("instrument_control")]+'\\libraries')
from libraries import *

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from tlb6700_gui_1um import Ui_MainWindow

class tlb6700_connection(qtw.QMainWindow,Ui_MainWindow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.setupUi(self)
		self.laser = tlb6700()
		self.configure_daq()
		self.ydfa = YDFA()

		# Connections
		self.connect_to_laser.clicked.connect(self.connect_to_tlb6700)
		self.connect_to_daq.clicked.connect(self.connect_daq)

		# TLB6700 controller parameters
		self.current_wavelength_button.clicked.connect(self.set_wavelength)
		self.laser_power_button.clicked.connect(self.set_power)
		self.set_params_button.clicked.connect(self.set_params)
		self.scan_button.clicked.connect(self.set_and_scan)

		# YDFA parameters
		self.get_status_button.clicked.connect(self.get_ydfa_status)
		self.bp_button.clicked.connect(self.set_bp)
		self.ld1_button.clicked.connect(self.set_ld1_current)
		self.ld2_button.clicked.connect(self.set_ld2_current)
		self.bp_enable_button.clicked.connect(self.enable_ydfa)

	def enable_ydfa(self):
		try:
			self.ydfa_status = self.ydfa.enable_bp()
			self.bp_onoff_label.setText(self.ydfa_status)
		except:
			self.bp_onoff_label.setText('error')

	def set_ld1_current(self):
		try:
			self.ld1_current = self.ydfa.set_ld1(int(self.ld1_edit.text()))
			self.ld1_output.setText(self.ld1_current)
		except:
			self.ld1_output.setText('error')

	def set_ld2_current(self):
		try:
			self.ld2_current = self.ydfa.set_ld2(int(self.ld2_edit.text()))
			self.ld2_output.setText(self.ld2_current)
		except:
			self.ld1_output.setText('error')

	def set_bp(self):
		try:
			self.bp = self.ydfa.set_bp(int(self.bp_edit.text()))
			self.bp_output.setText(f'{self.bp}')
		except Exception as e:
			print(str(e))
			self.bp_output.setText('error')

	def get_ydfa_status(self):
		self.ydfa.port = 'COM'+self.com_edit.text()
		self.ld1_current,self.ld2_current,self.bp,self.ydfa_input_power,self.enable_status = self.ydfa.get_status()
		self.ld1_output.setText(self.ld1_current); self.ld2_output.setText(self.ld2_current)
		self.bp_output.setText(self.bp); self.ydfa_input_label.setText('Input Power: '+self.ydfa_input_power+'dBm')
		self.bp_onoff_label.setText('BP '+self.enable_status)

	def configure_daq(self):
		self.ai_channels = self.aichannel_text.text().split(',')
		self.daq_device = self.daq_device_edit.text()
		self.timing_channel = self.timing_edit.text()
		if type(self.ai_channels) != list:
			# make into iterable if not already, this will help code find all user designed channels (multi or single) 
			self.ai_channels = [self.ai_channels] 
		temp_ai_channels = []
		for ai in self.ai_channels:
			temp_ai_channels.append(self.daq_device+'/'+ai)
		self.ai_channels = temp_ai_channels

	def connect_to_tlb6700(self):
		# attempts connection with DAQ and laser
		self.laser.ProductID = int(self.id_edit.text())
		self.laser.DeviceKey = self.key_edit.text()
		self.laser.tlb_open()
		message = self.laser.query('*IDN?')
		print(message)
		if message != '':
			qtw.QMessageBox.information(self,'Success', f'Successfully connected to laser: {message}')
			self.laser_connection_label.setText('connected')
		else:
			qtw.QMessageBox.critical(self,'Failed', f'Failed to connect to laser: {message}')

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
			self.daq_connection_label.setText(f'{data_point}')
			return f'{data_point}'
		except Exception as e:
			qtw.QMessageBox.critical(self,'Failed', f'Failed to connect to DAQ: {str(e)}')

	def set_wavelength(self):
		try:
			self.laser.set_track()
			out = self.laser.set_lambda(self.current_wavelength_edit.text())
			self.current_wavelength_output.setText(f'{out}')
		except:
			self.current_wavelength_output.setText('error')

	def set_power(self):
		try:
			out = self.laser.set_power(self.laser_power_edit.text())
			self.laser_power_output.setText(f'{out}')
		except:
			self.laser_power_output.setText('error')

	def set_params(self):
		try:
			start_λ = self.start_wavelength_edit.text()
			stop_λ = self.stop_wavelength_edit.text()
			forward_speed = self.forward_speed_edit.text()
			backward_speed = self.backward_speed_edit.text()
			number_of_scans = self.scan_number_edit.text()
			self.start,self.stop = self.laser.set_scan_limits(start_λ,stop_λ)
			self.start,self.stop = float(self.start),float(self.stop)
			forward,backward = self.laser.set_scan_speeds(forward_speed,backward_speed)
			number = self.laser.set_scan_number(number_of_scans)
			self.start_wavelength_output.setText(f'{self.start}')
			self.stop_wavelength_output.setText(f'{self.stop}')
			self.forward_speed_output.setText(f'{forward}')
			self.backward_speed_output.setText(f'{backward}')
			self.scan_number_output.setText(f'{number}')

			# deal with sampling rates and total data points in order to tell DAQ how many data points to collect
			sampling_rate = self.sampling_rate_edit.text()
			total_points = self.total_points_edit.text()
			if self.stop>self.start:
				self.time_taken = (float(self.stop)-float(self.start))/float(forward)
			elif self.start>self.stop:
				self.time_taken = (float(self.start)-float(self.stop))/float(backward)

			if sampling_rate: # if sampling rate and total points are both given, use sampling rate to calculate total points
				self.sampling_rate = float(sampling_rate)*1000
				self.total_points = round(self.sampling_rate*self.time_taken)
			elif total_points: 
				self.total_points = float(total_points)*1000
				self.sampling_rate = round(self.total_points/self.time_taken)
			else: # if nothing is given, use a default of 20k/s sampling rate
				self.sampling_rate = 20000
				self.total_points = round(self.sampling_rate*self.time_taken)
			self.sampling_rate_edit.setText(f'{self.sampling_rate/1000}')
			self.total_points_edit.setText(f'{self.total_points/1000}')

			# if self.stop>self.start:
			self.wavelengths = np.linspace(self.start,self.stop,self.total_points)
			# if self.start>self.stop:
			# 	self.wavelengths = np.linspace(self.stop,self.start,self.total_points)
			self.output = np.zeros((len(self.ai_channels),len(self.wavelengths)))

		except Exception as e:
			qtw.QMessageBox.critical(self,'Failed', f'Failed to set parameters: {str(e)}')

	def read_many_outputs(self,task):
		reader = AnalogMultiChannelReader(task.in_stream)
		reader.read_many_sample(data=self.output,number_of_samples_per_channel=self.total_points,timeout=50)

	def start_scan(self,task):
		# send high then low signal to laser (a pulse), which will trigger laser to start scan at the falling edge
		# use this instead of the built in laser scan function because this can be used to trigger the start of 
		# DAQ multidata acquisition
		task.write(True) 
		sleep(1)
		print('start scan')
		task.write(False)

	def set_and_scan(self):
		self.set_params()
		self.laser.set_track()
		self.laser.set_lambda(self.start)
		while not(self.laser.isFree()):
			sleep(1)

		with nidaqmx.Task() as task1:
			do = task1.do_channels.add_do_chan(f'{self.daq_device}/{self.timing_channel}', # {self.timing_channel}/line0:7
				line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
			# task1.write(True) 
			with nidaqmx.Task() as task2: # needs to start a new task for for the analog input (ai) channel, one task
			# does not accept multiple channel types
				for ai in self.ai_channels:
					task2.ai_channels.add_ai_voltage_chan(f"{ai}")
				task2.timing.cfg_samp_clk_timing(rate=self.sampling_rate,
					sample_mode=AcquisitionType.FINITE,
					samps_per_chan=self.total_points)
				task2.triggers.start_trigger.cfg_dig_edge_start_trig(f"/{self.daq_device}/{self.timing_channel}",
					Edge.FALLING)

				# need to use multi-threading because we want to
				# start the scan during the DAQ function for acquiring data, which will occupy the native thread.  If 
				# multithreads are not used, then the laser will start scan AFTER the DAQ has timed-out.
				threads = []
				t1 = Thread(target=self.read_many_outputs,args=(task2,)) 
				t2 = Thread(target=self.start_scan,args=(task1,))
				t1.start(); t2.start()
				start_time = time.time()
				threads.append(t1); threads.append(t2)
				for t in threads:
					t.join()
				real_time_taken = time.time()-start_time-1
		columns = ['wavelength'] + [f'{i}' for i in self.ai_channels]
		df = pd.DataFrame(np.concatenate((np.array([self.wavelengths]),self.output)).T,columns=columns)
		print(f'scan complete, estimated time = {self.time_taken}s, real time = {real_time_taken}s')
		self.time_taken_label.setText(f'{round(real_time_taken,3)} seconds')

		if self.save_data_checkbox.isChecked():
			filepath = self.filepath_edit.toPlainText().split('\\')
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

			df.to_csv(newfilename,index=False)

		self.output_df = df

		self.plots_view.clear()
		d = {}
		for i in range(len(self.ai_channels)):
			d[i] = self.plots_view.addPlot(title=f'{df.columns[1+i]}')
			d[i].plot(df.wavelength,df[df.columns[1+i]].values,pen=(i,len(self.ai_channels)))
			self.plots_view.nextRow()

	def closeEvent(self,event):
		# this method is used for properly terminating connection with laser
		reply = qtw.QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
				qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.No)
		if reply == qtw.QMessageBox.Yes:
			self.laser.tlb_close()
			event.accept()
			print('Window closed')
		else:
			event.ignore()

if __name__ == '__main__':
	app = qtw.QApplication(sys.argv)
	window = tlb6700_connection()
	window.show()
	app.exec_()
