import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import sys
import datetime
import nidaqmx
from nidaqmx.constants import AcquisitionType, Edge, TerminalConfiguration

# usage: python ADmoniNI.py <Nchan> <Fs> <Tdur>
# e.g. : python ADmoniNI.py 4 1000 5.0

DevID='Dev1'
AImode=TerminalConfiguration.DIFFERENTIAL
#AImode=TerminalConfiguration.RSE
args=sys.argv
Nchan=int(args[1])
Fs=int(args[2])
nd=int(Fs*float(args[3]))

device = nidaqmx.system.device.Device(DevID)
if Nchan>1:
 chan='ai0:'+str(Nchan-1)
else:
 chan='ai0'

# Detect key event
def onKey(event):
 if event.key=='r':
  print('Recording...')
  t,y=funcDAQ(Nchan, nd, Fs)
  df = pd.DataFrame(np.concatenate([t, y], 1))
  now=datetime.datetime.now()
  fname='AD'+now.strftime('%Y%m%d%H%M%S')+'.xlsx'
  df.to_excel(fname, sheet_name='raw', index=False, header=False)
  funcDrawdat(t, y, Nchan, lc='r')
  plt.pause(5)
  print('...Exported to '+fname)
  sys.exit()
 elif event.key=='q':
  print('Stopped.')
  sys.exit()

# Plot
def funcDrawdat(t, x, Nchan, lc='b'):
 if Nchan>1:
  for i in range(Nchan):	
   plt.subplot(Nchan,1,i+1)
   plt.cla()
   plt.plot(t,x[:,i],lc)
 else:
  plt.cla()
  plt.plot(t,x,lc)

# Data Acquisition & Plot
def funcDAQ(Nchan, nd, Fs):
 dat=task.read(number_of_samples_per_channel=nd)
 dat=np.array(dat)
 dat=np.reshape(dat.T, (nd,Nchan))
 dt=1/Fs
 t=np.linspace(1/Fs,1/Fs*nd,nd)
 t=np.reshape(t, (nd,1))
 funcDrawdat(t, dat, Nchan)
 plt.pause(1e-9)
 return t, dat

with nidaqmx.Task() as task:
 ai_channel = task.ai_channels.add_ai_voltage_chan(DevID+'/'+chan, terminal_config = AImode)
 task.timing.cfg_samp_clk_timing(Fs,active_edge=Edge.RISING, sample_mode=AcquisitionType.CONTINUOUS, samps_per_chan=nd)
 while True:
  try:
   plt.connect('key_press_event',onKey)
   t,y=funcDAQ(Nchan, int(Fs/2), Fs)
  except KeyboardInterrupt:
   break
# end of file