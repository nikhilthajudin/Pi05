from pi05_dev import *
import pyvisa
import numpy as np

def read_smu():
    return float(smu.query("READ?")[:-1])

def read_dmm():
    return float(dmm.query("READ?")[:-1])

path=r"C:\Users\Lab_PC\OneDrive\Desktop\pi05_loadreg.txt"

rm = pyvisa.ResourceManager()
dmm = rm.open_resource('USB0::0x1AB1::0x0C94::DM3O234301254::INSTR')
smu = rm.open_resource('USB0::0x05E6::0x2450::04532497::INSTR')
psu = rm.open_resource('USB0::0x1AB1::0x0E11::DP8F234100566::INSTR')
smu.timeout = 100000
dmm.timeout = 100000


softReset(0x41)
unlock(0x41)
dev_write_b_I2C(0x41,0x1,0x17,0x2)

vdac = 0        #VDAC to be trimmed

#Scale Trim
ideal_gain = 2.1875
temp = read_smu()
for scale_trim in range(64):
    obs_gain = 0
    vdacScaleTrim(vdac,scale_trim)
    enableVDAC(0x41, vdac, 0, 1, 0xf00)
    a = abs(read_smu())
    enableVDAC(0x41, vdac, 0, 1, 0x100)
    b = abs(read_smu())
    obs_gain = (b-a)
    if -2e-3<ideal_gain-obs_gain<2e-3:
        print("DAC{} Scale Trim:{}".format(vdac,scale_trim))
        break
    else:
        pass
temp = read_smu()

#Offset Trim
enableVDAC(0x41,vdac,0,1,0x100)
ideal_offset = 2.34375
for i in range(32):
    vdacOffTrim(vdac,i)
    offset = abs(read_smu())
    if -2e-3<ideal_offset-offset<2e-3:
        print("DAC{} Offset Trim:{}".format(vdac,i))
        break







