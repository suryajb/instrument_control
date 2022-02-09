import sys
# sys.path.append('C:\\Users\\Lynn\\Desktop\\instrument_control\\libraries')
sys.path.append(os.getcwd()[:os.getcwd().find("instrument_control")+len("instrument_control")]+'\\libraries')
from libraries import *
import pyvisa as pv
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from yokogawa_gui import Ui_MainWindow

class yokogawa_gui(qtw.QMainWindow,Ui_MainWindow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.setupUi(self)
		self.append_n = 0
		self.connect_button.clicked.connect(self.connect_to_yokogawas)
		self.scan_short_button.clicked.connect(lambda: self.scan(['AQ6374']))
		self.scan_long_button.clicked.connect(lambda: self.scan(['AQ6376']))
		self.scan_both_button.clicked.connect(lambda: self.scan(['AQ6374','AQ6376']))
		# self.laser = tlb6700()
		# self.configure_daq()
		# self.ydfa = YDFA()

		# # Connections
		# self.connect_to_laser.clicked.connect(self.connect_to_tlb6700)
		# self.connect_to_daq.clicked.connect(self.connect_daq)

		# # TLB6700 controller parameters
		# self.current_wavelength_button.clicked.connect(self.set_wavelength)
		# self.laser_power_button.clicked.connect(self.set_power)
		# self.set_params_button.clicked.connect(self.set_params)
		# self.scan_button.clicked.connect(self.set_and_scan)

		# # YDFA parameters
		# self.get_status_button.clicked.connect(self.get_ydfa_status)
		# self.bp_button.clicked.connect(self.set_bp)
		# self.ld1_button.clicked.connect(self.set_ld1_current)
		# self.ld2_button.clicked.connect(self.set_ld2_current)
		# self.bp_enable_button.clicked.connect(self.enable_ydfa)

	def connect_to_yokogawas(self):
		# automatically detects connected yokogawas and initiates connections through gpib
		rm = pv.ResourceManager()
		resources = rm.list_resources()
		self.connections = {}
		for r in resources:
			try: # doing everything in exception handling because don't want program to crash
			# also for ease of user debugging
				inst = rm.open_resource(r)
				name = inst.query("*IDN?")[:-1].split(',')
				if name[0] == 'YOKOGAWA':
					try:
						self.connections[name[1]] = yokogawa(model=name[1],inst=inst)
					except Exception as e:
						print(str(e))
						self.connections_edit.setText(str(e))
						return -1
			except:
				pass
		if not(self.connections):
			output_str = 'no connections made, check GPIB'
		else:
			output_str = 'connected to:\n'
			for key,val in self.connections.items():
				output_str += val.identity['model']+' '
		self.connections_edit.setText(output_str)

	# def scan_short(self):
	# def scan_single(self,)

	def scan(self,models):
		# user parameters in a dictionary so it can be iterated through
		start = {}; stop = {}; points = {}; sensitivity = {}; scan_type = {}
		self.data = {}
		sensitivity = {'Normal Hold':'NHLD', 
					   'Normal Auto':'NAUT',
					   'Mid':'MID',
					   'High1':'HIGH1',
					   'High2':'HIGH2',
					   'High3':'HIGH3',
					   'Normal':'NORMAL'}
		start['AQ6374'] = self.short_start_edit.text()
		start['AQ6376'] = self.long_start_edit.text()
		stop['AQ6374'] = self.short_stop_edit.text()
		stop['AQ6376'] = self.long_stop_edit.text()
		points['AQ6374'] = self.short_points_edit.text()
		points['AQ6376'] = self.long_points_edit.text()
		sensitivity['AQ6374'] = sensitivity[self.short_sensitivity_combobox.currentText()]
		sensitivity['AQ6376'] = sensitivity[self.long_sensitivity_combobox.currentText()]
		scan_type['AQ6374'] = self.short_scantype_combobox.currentText()
		scan_type['AQ6376'] = self.long_scantype_combobox.currentText()

		# scan one yokagawa
		if len(models) == 1:
			m = models[0]
			if m in self.connections:
				 # define settings for trace
				self.connections[m].define_settings(start=start[m],
													stop=stop[m],
													points=points[m],
													sensitivity=sensitivity[m])
				if scan_type[m] == 'Single':
					self.connections[m].start_trace(scan_type[m].lower())
					self.data[m] = self.connections[m].get_trace_data()
				elif scan_type[m] == 'Stop':
					self.connections[m].start_trace(scan_type[m].lower())
					return
				elif scan_type[m] == 'Repeat':
					self.connections[m].start_trace('single')
					self.data[m] = self.connections[m].get_trace_data()
					self.connections[m].start_trace('repeat')
			else:
				qtw.QMessageBox.critical(self,'Failed', f'{m} not in connections')

		if len(models) == 2: # scan both button is pressed
			for m in models:
				if m in self.connections:
					 # define settings for trace
					self.connections[m].define_settings(start=start[m],
														stop=stop[m],
														points=points[m],
														sensitivity=sensitivity[m])
					if scan_type[m] == 'Stop':
						self.connections[m].start_trace(scan_type[m].lower())
				else:
					qtw.QMessageBox.critical(self,'Failed', f'{m} not in connections')
			
			# need to start multithreads because otherwise yokogawas will not start at the same time
			# there are three conditions, both are set to stop, (stop and return nothing)
			# both are not set to stop, (record both, set the correct one to repeat)
			# one of the two is set to stop (one needs to stop)
			if (scan_type[models[0]] == 'Stop') and (scan_type[models[1]] == 'Stop'):
				return
			elif not(scan_type[models[0]] == 'Stop') and not(scan_type[models[1]] == 'Stop'):
				threads = []
				t1 = Thread(target=self.connections[models[0]].start_trace,args=('single',))
				t2 = Thread(target=self.connections[models[1]].start_trace,args=('single',))
				t1.start(); t2.start()
				threads.append(t1); threads.append(t2)
				for t in threads:
					t.join()
				for m in models:
					self.data[m] = self.connections[m].get_trace_data()
					if scan_type[m] == 'Repeat':
						self.connections[m].start_trace('repeat')
			else: # one of the models is set to stop
				for m in models:
					if scan_type[m] != 'Stop':
						self.connections[m].start_trace('single')
						self.data[m] = self.connections[m].get_trace_data()
					if scan_type[m] == 'Repeat':
						self.connections[m].start_trace('repeat')

		data_list = self.data.values()
		data_agg = pd.concat(data_list,ignore_index=True,sort=True)
		data_agg = data_agg[['wavelength','S']]
		# # save data
		# if self.save_checkbox.isChecked():
		# 	filepath = self.filelocation_edit.toPlainText().split('\\')
		# 	filename = ('\\').join(filepath)
		# 	filepath = filepath[:-1]

		# 	append = f'_{self.append_n:02}'
		# 	while filename in glob.glob(("\\").join(filepath)+"\\*"):
		# 		filename = ('.').join(filename.split('.')[:-1]) + append + '.' + filename.split('.')[-1]
		# 		self.append_n += 1
		# 		append = f'_{self.append_n:02}'

		# 	data_agg.to_csv(filename,index=False)
		# save data
		if self.save_checkbox.isChecked():
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
			data_agg.to_csv(newfilename,index=False)
		# plot data
		self.plot_glw.clear()
		plot = self.plot_glw.addPlot(title='OSA Trace')
		plot.plot(data_agg.wavelength,data_agg.S)

	def closeEvent(self,event):
		# this method is used for properly terminating connection with laser
		reply = qtw.QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
				qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.No)
		if reply == qtw.QMessageBox.Yes:
			for k,v in self.connections.items():
				v.close()
			event.accept()
			print('Window closed')
		else:
			event.ignore()

if __name__ == '__main__':
	app = qtw.QApplication(sys.argv)
	window = yokogawa_gui()
	window.show()
	app.exec_()
