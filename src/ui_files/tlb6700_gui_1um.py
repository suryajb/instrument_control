# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tlb6700_gui_1um.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(986, 779)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.connect_to_laser = QtWidgets.QPushButton(self.centralwidget)
        self.connect_to_laser.setGeometry(QtCore.QRect(130, 85, 91, 23))
        self.connect_to_laser.setObjectName("connect_to_laser")
        self.laser_connection_label = QtWidgets.QLabel(self.centralwidget)
        self.laser_connection_label.setGeometry(QtCore.QRect(228, 88, 111, 16))
        self.laser_connection_label.setObjectName("laser_connection_label")
        self.aichannel_label = QtWidgets.QLabel(self.centralwidget)
        self.aichannel_label.setGeometry(QtCore.QRect(15, 70, 61, 20))
        self.aichannel_label.setObjectName("aichannel_label")
        self.connect_to_daq = QtWidgets.QPushButton(self.centralwidget)
        self.connect_to_daq.setGeometry(QtCore.QRect(130, 51, 91, 23))
        self.connect_to_daq.setObjectName("connect_to_daq")
        self.aichannel_text = QtWidgets.QLineEdit(self.centralwidget)
        self.aichannel_text.setGeometry(QtCore.QRect(79, 70, 41, 20))
        self.aichannel_text.setObjectName("aichannel_text")
        self.connections_frame = QtWidgets.QFrame(self.centralwidget)
        self.connections_frame.setGeometry(QtCore.QRect(10, 10, 331, 121))
        self.connections_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.connections_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.connections_frame.setObjectName("connections_frame")
        self.connections_title = QtWidgets.QLabel(self.connections_frame)
        self.connections_title.setGeometry(QtCore.QRect(10, 5, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.connections_title.setFont(font)
        self.connections_title.setObjectName("connections_title")
        self.id_edit = QtWidgets.QLineEdit(self.connections_frame)
        self.id_edit.setGeometry(QtCore.QRect(155, 8, 41, 20))
        self.id_edit.setObjectName("id_edit")
        self.id_label = QtWidgets.QLabel(self.connections_frame)
        self.id_label.setGeometry(QtCore.QRect(118, 8, 41, 20))
        self.id_label.setObjectName("id_label")
        self.key_label = QtWidgets.QLabel(self.connections_frame)
        self.key_label.setGeometry(QtCore.QRect(204, 10, 31, 16))
        self.key_label.setObjectName("key_label")
        self.key_edit = QtWidgets.QLineEdit(self.connections_frame)
        self.key_edit.setGeometry(QtCore.QRect(230, 8, 91, 20))
        self.key_edit.setObjectName("key_edit")
        self.daq_device_label = QtWidgets.QLabel(self.connections_frame)
        self.daq_device_label.setGeometry(QtCore.QRect(28, 30, 41, 20))
        self.daq_device_label.setObjectName("daq_device_label")
        self.daq_device_edit = QtWidgets.QLineEdit(self.connections_frame)
        self.daq_device_edit.setGeometry(QtCore.QRect(69, 30, 41, 20))
        self.daq_device_edit.setObjectName("daq_device_edit")
        self.timing_edit = QtWidgets.QLineEdit(self.connections_frame)
        self.timing_edit.setGeometry(QtCore.QRect(69, 90, 41, 20))
        self.timing_edit.setObjectName("timing_edit")
        self.timing_label = QtWidgets.QLabel(self.connections_frame)
        self.timing_label.setGeometry(QtCore.QRect(32, 90, 41, 20))
        self.timing_label.setObjectName("timing_label")
        self.daq_connection_label = QtWidgets.QLineEdit(self.connections_frame)
        self.daq_connection_label.setGeometry(QtCore.QRect(215, 43, 113, 20))
        self.daq_connection_label.setObjectName("daq_connection_label")
        self.laser_params_frame = QtWidgets.QFrame(self.centralwidget)
        self.laser_params_frame.setGeometry(QtCore.QRect(10, 150, 331, 361))
        self.laser_params_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.laser_params_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.laser_params_frame.setObjectName("laser_params_frame")
        self.laser_params_title = QtWidgets.QLabel(self.laser_params_frame)
        self.laser_params_title.setGeometry(QtCore.QRect(13, 6, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.laser_params_title.setFont(font)
        self.laser_params_title.setObjectName("laser_params_title")
        self.current_wavelength_edit = QtWidgets.QLineEdit(self.laser_params_frame)
        self.current_wavelength_edit.setGeometry(QtCore.QRect(125, 32, 101, 20))
        self.current_wavelength_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.current_wavelength_edit.setObjectName("current_wavelength_edit")
        self.current_wavelength_label = QtWidgets.QLabel(self.laser_params_frame)
        self.current_wavelength_label.setGeometry(QtCore.QRect(10, 32, 111, 20))
        self.current_wavelength_label.setObjectName("current_wavelength_label")
        self.current_wavelength_button = QtWidgets.QPushButton(self.laser_params_frame)
        self.current_wavelength_button.setGeometry(QtCore.QRect(284, 30, 41, 23))
        self.current_wavelength_button.setObjectName("current_wavelength_button")
        self.laser_power_label = QtWidgets.QLabel(self.laser_params_frame)
        self.laser_power_label.setGeometry(QtCore.QRect(29, 60, 91, 20))
        self.laser_power_label.setObjectName("laser_power_label")
        self.laser_power_edit = QtWidgets.QLineEdit(self.laser_params_frame)
        self.laser_power_edit.setGeometry(QtCore.QRect(125, 60, 101, 20))
        self.laser_power_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.laser_power_edit.setObjectName("laser_power_edit")
        self.laser_power_button = QtWidgets.QPushButton(self.laser_params_frame)
        self.laser_power_button.setGeometry(QtCore.QRect(284, 58, 41, 23))
        self.laser_power_button.setObjectName("laser_power_button")
        self.scan_params_title = QtWidgets.QLabel(self.laser_params_frame)
        self.scan_params_title.setGeometry(QtCore.QRect(12, 96, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.scan_params_title.setFont(font)
        self.scan_params_title.setObjectName("scan_params_title")
        self.current_wavelength_output = QtWidgets.QLabel(self.laser_params_frame)
        self.current_wavelength_output.setGeometry(QtCore.QRect(230, 34, 47, 13))
        self.current_wavelength_output.setObjectName("current_wavelength_output")
        self.laser_power_output = QtWidgets.QLabel(self.laser_params_frame)
        self.laser_power_output.setGeometry(QtCore.QRect(230, 64, 47, 13))
        self.laser_power_output.setObjectName("laser_power_output")
        self.scan_button = QtWidgets.QPushButton(self.laser_params_frame)
        self.scan_button.setGeometry(QtCore.QRect(230, 311, 91, 41))
        self.scan_button.setObjectName("scan_button")
        self.start_wavelength_edit = QtWidgets.QLineEdit(self.laser_params_frame)
        self.start_wavelength_edit.setGeometry(QtCore.QRect(125, 120, 101, 20))
        self.start_wavelength_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.start_wavelength_edit.setObjectName("start_wavelength_edit")
        self.stop_wavelength_output = QtWidgets.QLabel(self.laser_params_frame)
        self.stop_wavelength_output.setGeometry(QtCore.QRect(230, 152, 47, 13))
        self.stop_wavelength_output.setObjectName("stop_wavelength_output")
        self.stop_wavelength_label = QtWidgets.QLabel(self.laser_params_frame)
        self.stop_wavelength_label.setGeometry(QtCore.QRect(12, 148, 111, 20))
        self.stop_wavelength_label.setObjectName("stop_wavelength_label")
        self.start_wavelength_label = QtWidgets.QLabel(self.laser_params_frame)
        self.start_wavelength_label.setGeometry(QtCore.QRect(10, 120, 111, 20))
        self.start_wavelength_label.setObjectName("start_wavelength_label")
        self.start_wavelength_output = QtWidgets.QLabel(self.laser_params_frame)
        self.start_wavelength_output.setGeometry(QtCore.QRect(230, 122, 47, 13))
        self.start_wavelength_output.setObjectName("start_wavelength_output")
        self.stop_wavelength_edit = QtWidgets.QLineEdit(self.laser_params_frame)
        self.stop_wavelength_edit.setGeometry(QtCore.QRect(125, 148, 101, 20))
        self.stop_wavelength_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.stop_wavelength_edit.setObjectName("stop_wavelength_edit")
        self.forward_speed_edit = QtWidgets.QLineEdit(self.laser_params_frame)
        self.forward_speed_edit.setGeometry(QtCore.QRect(125, 176, 41, 20))
        self.forward_speed_edit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.forward_speed_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.forward_speed_edit.setObjectName("forward_speed_edit")
        self.forward_speed_output = QtWidgets.QLabel(self.laser_params_frame)
        self.forward_speed_output.setGeometry(QtCore.QRect(171, 178, 31, 16))
        self.forward_speed_output.setObjectName("forward_speed_output")
        self.forward_speed_label = QtWidgets.QLabel(self.laser_params_frame)
        self.forward_speed_label.setGeometry(QtCore.QRect(13, 176, 111, 20))
        self.forward_speed_label.setObjectName("forward_speed_label")
        self.set_params_button = QtWidgets.QPushButton(self.laser_params_frame)
        self.set_params_button.setGeometry(QtCore.QRect(130, 266, 71, 31))
        self.set_params_button.setObjectName("set_params_button")
        self.save_data_checkbox = QtWidgets.QCheckBox(self.laser_params_frame)
        self.save_data_checkbox.setGeometry(QtCore.QRect(10, 323, 51, 17))
        self.save_data_checkbox.setChecked(True)
        self.save_data_checkbox.setObjectName("save_data_checkbox")
        self.scan_number_label = QtWidgets.QLabel(self.laser_params_frame)
        self.scan_number_label.setGeometry(QtCore.QRect(68, 206, 51, 20))
        self.scan_number_label.setObjectName("scan_number_label")
        self.scan_number_edit = QtWidgets.QLineEdit(self.laser_params_frame)
        self.scan_number_edit.setGeometry(QtCore.QRect(125, 206, 101, 20))
        self.scan_number_edit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.scan_number_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.scan_number_edit.setObjectName("scan_number_edit")
        self.scan_number_output = QtWidgets.QLabel(self.laser_params_frame)
        self.scan_number_output.setGeometry(QtCore.QRect(230, 208, 31, 16))
        self.scan_number_output.setObjectName("scan_number_output")
        self.backward_speed_label = QtWidgets.QLabel(self.laser_params_frame)
        self.backward_speed_label.setGeometry(QtCore.QRect(205, 176, 51, 20))
        self.backward_speed_label.setObjectName("backward_speed_label")
        self.backward_speed_edit = QtWidgets.QLineEdit(self.laser_params_frame)
        self.backward_speed_edit.setGeometry(QtCore.QRect(255, 176, 41, 20))
        self.backward_speed_edit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.backward_speed_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.backward_speed_edit.setObjectName("backward_speed_edit")
        self.backward_speed_output = QtWidgets.QLabel(self.laser_params_frame)
        self.backward_speed_output.setGeometry(QtCore.QRect(303, 178, 31, 16))
        self.backward_speed_output.setObjectName("backward_speed_output")
        self.filepath_edit = QtWidgets.QTextEdit(self.laser_params_frame)
        self.filepath_edit.setGeometry(QtCore.QRect(59, 304, 161, 51))
        self.filepath_edit.setObjectName("filepath_edit")
        self.sampling_rate_label = QtWidgets.QLabel(self.laser_params_frame)
        self.sampling_rate_label.setGeometry(QtCore.QRect(25, 234, 101, 20))
        self.sampling_rate_label.setObjectName("sampling_rate_label")
        self.total_points_label = QtWidgets.QLabel(self.laser_params_frame)
        self.total_points_label.setGeometry(QtCore.QRect(183, 234, 81, 20))
        self.total_points_label.setObjectName("total_points_label")
        self.sampling_rate_edit = QtWidgets.QLineEdit(self.laser_params_frame)
        self.sampling_rate_edit.setGeometry(QtCore.QRect(125, 235, 51, 20))
        self.sampling_rate_edit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.sampling_rate_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sampling_rate_edit.setObjectName("sampling_rate_edit")
        self.total_points_edit = QtWidgets.QLineEdit(self.laser_params_frame)
        self.total_points_edit.setGeometry(QtCore.QRect(260, 235, 61, 20))
        self.total_points_edit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.total_points_edit.setText("")
        self.total_points_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.total_points_edit.setObjectName("total_points_edit")
        self.time_taken_label = QtWidgets.QLabel(self.laser_params_frame)
        self.time_taken_label.setGeometry(QtCore.QRect(230, 290, 91, 20))
        self.time_taken_label.setText("")
        self.time_taken_label.setAlignment(QtCore.Qt.AlignCenter)
        self.time_taken_label.setObjectName("time_taken_label")
        self.plots_view = GraphicsLayoutWidget(self.centralwidget)
        self.plots_view.setGeometry(QtCore.QRect(360, 10, 611, 721))
        self.plots_view.setObjectName("plots_view")
        self.connections_frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.connections_frame_2.setGeometry(QtCore.QRect(10, 530, 331, 121))
        self.connections_frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.connections_frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.connections_frame_2.setObjectName("connections_frame_2")
        self.ydfa_title = QtWidgets.QLabel(self.connections_frame_2)
        self.ydfa_title.setGeometry(QtCore.QRect(10, 5, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ydfa_title.setFont(font)
        self.ydfa_title.setObjectName("ydfa_title")
        self.ld1_label = QtWidgets.QLabel(self.connections_frame_2)
        self.ld1_label.setGeometry(QtCore.QRect(11, 34, 51, 20))
        self.ld1_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ld1_label.setObjectName("ld1_label")
        self.ld1_edit = QtWidgets.QLineEdit(self.connections_frame_2)
        self.ld1_edit.setGeometry(QtCore.QRect(65, 34, 41, 20))
        self.ld1_edit.setObjectName("ld1_edit")
        self.ld2_edit = QtWidgets.QLineEdit(self.connections_frame_2)
        self.ld2_edit.setGeometry(QtCore.QRect(65, 64, 41, 20))
        self.ld2_edit.setObjectName("ld2_edit")
        self.ld2_label = QtWidgets.QLabel(self.connections_frame_2)
        self.ld2_label.setGeometry(QtCore.QRect(11, 63, 51, 20))
        self.ld2_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ld2_label.setObjectName("ld2_label")
        self.bp_edit = QtWidgets.QLineEdit(self.connections_frame_2)
        self.bp_edit.setGeometry(QtCore.QRect(65, 93, 41, 20))
        self.bp_edit.setObjectName("bp_edit")
        self.bp_label = QtWidgets.QLabel(self.connections_frame_2)
        self.bp_label.setGeometry(QtCore.QRect(21, 92, 41, 20))
        self.bp_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.bp_label.setObjectName("bp_label")
        self.ld1_button = QtWidgets.QPushButton(self.connections_frame_2)
        self.ld1_button.setGeometry(QtCore.QRect(148, 32, 41, 23))
        self.ld1_button.setObjectName("ld1_button")
        self.ld2_button = QtWidgets.QPushButton(self.connections_frame_2)
        self.ld2_button.setGeometry(QtCore.QRect(148, 62, 41, 23))
        self.ld2_button.setObjectName("ld2_button")
        self.bp_button = QtWidgets.QPushButton(self.connections_frame_2)
        self.bp_button.setGeometry(QtCore.QRect(148, 91, 41, 23))
        self.bp_button.setObjectName("bp_button")
        self.bp_enable_button = QtWidgets.QPushButton(self.connections_frame_2)
        self.bp_enable_button.setGeometry(QtCore.QRect(254, 83, 71, 31))
        self.bp_enable_button.setObjectName("bp_enable_button")
        self.get_status_button = QtWidgets.QPushButton(self.connections_frame_2)
        self.get_status_button.setGeometry(QtCore.QRect(254, 7, 71, 31))
        self.get_status_button.setObjectName("get_status_button")
        self.ld1_output = QtWidgets.QLabel(self.connections_frame_2)
        self.ld1_output.setGeometry(QtCore.QRect(108, 37, 41, 16))
        self.ld1_output.setObjectName("ld1_output")
        self.ld2_output = QtWidgets.QLabel(self.connections_frame_2)
        self.ld2_output.setGeometry(QtCore.QRect(108, 67, 41, 16))
        self.ld2_output.setObjectName("ld2_output")
        self.bp_output = QtWidgets.QLabel(self.connections_frame_2)
        self.bp_output.setGeometry(QtCore.QRect(108, 95, 41, 16))
        self.bp_output.setObjectName("bp_output")
        self.ydfa_input_label = QtWidgets.QLabel(self.connections_frame_2)
        self.ydfa_input_label.setGeometry(QtCore.QRect(200, 45, 121, 16))
        self.ydfa_input_label.setObjectName("ydfa_input_label")
        self.bp_onoff_label = QtWidgets.QLabel(self.connections_frame_2)
        self.bp_onoff_label.setGeometry(QtCore.QRect(260, 67, 61, 16))
        self.bp_onoff_label.setAlignment(QtCore.Qt.AlignCenter)
        self.bp_onoff_label.setObjectName("bp_onoff_label")
        self.com_edit = QtWidgets.QLineEdit(self.connections_frame_2)
        self.com_edit.setGeometry(QtCore.QRect(183, 6, 41, 20))
        self.com_edit.setObjectName("com_edit")
        self.com_label = QtWidgets.QLabel(self.connections_frame_2)
        self.com_label.setGeometry(QtCore.QRect(142, 6, 41, 20))
        self.com_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.com_label.setObjectName("com_label")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 660, 331, 71))
        self.textBrowser.setObjectName("textBrowser")
        self.connections_frame.raise_()
        self.connect_to_laser.raise_()
        self.laser_connection_label.raise_()
        self.aichannel_label.raise_()
        self.connect_to_daq.raise_()
        self.aichannel_text.raise_()
        self.laser_params_frame.raise_()
        self.plots_view.raise_()
        self.connections_frame_2.raise_()
        self.textBrowser.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 986, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "New Focus Laser GUI"))
        self.connect_to_laser.setText(_translate("MainWindow", "Connect Laser"))
        self.laser_connection_label.setText(_translate("MainWindow", "Laser not connected "))
        self.aichannel_label.setText(_translate("MainWindow", "Ai channels:"))
        self.connect_to_daq.setText(_translate("MainWindow", "Connect DAQ"))
        self.aichannel_text.setText(_translate("MainWindow", "ai1,ai2"))
        self.connections_title.setText(_translate("MainWindow", "Connections"))
        self.id_edit.setText(_translate("MainWindow", "4106"))
        self.id_label.setText(_translate("MainWindow", "TLB ID:"))
        self.key_label.setText(_translate("MainWindow", "Key:"))
        self.key_edit.setText(_translate("MainWindow", "6700 SN41050"))
        self.daq_device_label.setText(_translate("MainWindow", "Device:"))
        self.daq_device_edit.setText(_translate("MainWindow", "Dev1"))
        self.timing_edit.setText(_translate("MainWindow", "PFI1"))
        self.timing_label.setText(_translate("MainWindow", "Timing:"))
        self.daq_connection_label.setText(_translate("MainWindow", "DAQ not connected"))
        self.laser_params_title.setText(_translate("MainWindow", "Laser Parameters"))
        self.current_wavelength_edit.setText(_translate("MainWindow", "1030"))
        self.current_wavelength_label.setText(_translate("MainWindow", "Curr Wavelength (nm)"))
        self.current_wavelength_button.setText(_translate("MainWindow", "Go"))
        self.laser_power_label.setText(_translate("MainWindow", "Laser Power (mW)"))
        self.laser_power_edit.setText(_translate("MainWindow", "1"))
        self.laser_power_button.setText(_translate("MainWindow", "Go"))
        self.scan_params_title.setText(_translate("MainWindow", "Scan Parameters"))
        self.current_wavelength_output.setText(_translate("MainWindow", ".."))
        self.laser_power_output.setText(_translate("MainWindow", ".."))
        self.scan_button.setText(_translate("MainWindow", "Set and Scan"))
        self.start_wavelength_edit.setText(_translate("MainWindow", "1030"))
        self.stop_wavelength_output.setText(_translate("MainWindow", ".."))
        self.stop_wavelength_label.setText(_translate("MainWindow", "Stop Wavelength (nm)"))
        self.start_wavelength_label.setText(_translate("MainWindow", "Start Wavelength (nm)"))
        self.start_wavelength_output.setText(_translate("MainWindow", ".."))
        self.stop_wavelength_edit.setText(_translate("MainWindow", "1070"))
        self.forward_speed_edit.setText(_translate("MainWindow", "4"))
        self.forward_speed_output.setText(_translate("MainWindow", ".."))
        self.forward_speed_label.setText(_translate("MainWindow", "Forward Speed (nm/s)"))
        self.set_params_button.setText(_translate("MainWindow", "Set Params"))
        self.save_data_checkbox.setText(_translate("MainWindow", "Save"))
        self.scan_number_label.setText(_translate("MainWindow", "# of Scans"))
        self.scan_number_edit.setText(_translate("MainWindow", "1"))
        self.scan_number_output.setText(_translate("MainWindow", ".."))
        self.backward_speed_label.setText(_translate("MainWindow", "Backward"))
        self.backward_speed_edit.setText(_translate("MainWindow", "4"))
        self.backward_speed_output.setText(_translate("MainWindow", ".."))
        self.filepath_edit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">C:\\Users\\Xiang\\Desktop\\Josh\\tlb6700\\test.dat</p></body></html>"))
        self.sampling_rate_label.setText(_translate("MainWindow", "Sampling Rate (K/s)"))
        self.total_points_label.setText(_translate("MainWindow", "Total Points (K)"))
        self.sampling_rate_edit.setText(_translate("MainWindow", "20"))
        self.ydfa_title.setText(_translate("MainWindow", "YDFA Parameters"))
        self.ld1_label.setText(_translate("MainWindow", "LD1 (mA):"))
        self.ld1_edit.setText(_translate("MainWindow", "0"))
        self.ld2_edit.setText(_translate("MainWindow", "0"))
        self.ld2_label.setText(_translate("MainWindow", "LD2 (mA):"))
        self.bp_edit.setText(_translate("MainWindow", "1"))
        self.bp_label.setText(_translate("MainWindow", "BP:"))
        self.ld1_button.setText(_translate("MainWindow", "Go"))
        self.ld2_button.setText(_translate("MainWindow", "Go"))
        self.bp_button.setText(_translate("MainWindow", "Go"))
        self.bp_enable_button.setText(_translate("MainWindow", "BP On/Off"))
        self.get_status_button.setText(_translate("MainWindow", "Get Status"))
        self.ld1_output.setText(_translate("MainWindow", ".."))
        self.ld2_output.setText(_translate("MainWindow", ".."))
        self.bp_output.setText(_translate("MainWindow", ".."))
        self.ydfa_input_label.setText(_translate("MainWindow", "Input Power:"))
        self.bp_onoff_label.setText(_translate("MainWindow", "BP Off"))
        self.com_edit.setText(_translate("MainWindow", "7"))
        self.com_label.setText(_translate("MainWindow", "COM:"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">YDFA Important Notes:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1. Input signal should be enabled before turning on LD1/LD2</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2. Do not lower LD1/LD2 current before booster amplifier</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3. Do not lower LD1 current before turning off LD2</p></body></html>"))
from pyqtgraph import GraphicsLayoutWidget
