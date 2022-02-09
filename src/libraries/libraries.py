import os
import sys
import pdb
import numpy as np
import glob
import pandas as pd
import clr
from time import sleep
import time
from clr import System
from System.Text import StringBuilder
from System import Int32
from System.Reflection import Assembly
from threading import Thread
sys.path.append('C:\\Program Files (x86)\\Newport\\Newport USB Driver\\Bin')
sys.path.append(os.getcwd()[:os.getcwd().find("instrument_control")+len("instrument_control")]+'\\hardware_classes')
sys.path.append(os.getcwd()[:os.getcwd().find("instrument_control")+len("instrument_control")]+'\\ui_files')
clr.AddReference('UsbDllWrap')
import Newport
import nidaqmx
from nidaqmx.constants import *
from nidaqmx.stream_readers import (AnalogSingleChannelReader, AnalogMultiChannelReader)
import pyqtgraph as pg
import serial

from tlb6700_class import *
from YDFA_class import *
from yokogawa import *
from tsl710 import *