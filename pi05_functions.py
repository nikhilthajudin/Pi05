from test_main_board_pi05 import *

#General functions

def softReset(slv_add):     # Causes a soft reset. This bit autoclears and returns 0 on read.
    dev_write_b_I2C(slv_add, 0x1, 0x1, 1)

def unlock(slv_add):
    dev_write_b_I2C (slv_add, 0x40, 0, 0xc0de)
    dev_write_b_I2C (slv_add, 0x40, 1, 0xf00d)

def vrefPwdwn(slv_add):
    dev_write_b_I2C(slv_add, 0x1, 0x17, 2)

def dumpTrims():
    unlock(0x41)
    my_data = ""
    dev_read_b_I2C(0x41,0x20, 0)
    for i in range(6):
        for j in range(4):
            res_list = dev_read_b_I2C(0x41,0x20 + i, j)
            print("{} : {} : {}".format(0x20 + i, j, res_list))
            my_data+="{} : {} : {}\n".format(0x20 + i, j, res_list)
    return my_data


#VDAC
def enableVDAC(slv_add, vdac_no, range, gain, code):        #1: Positive Range, 0: Negative Range
    dev_write_b_I2C(slv_add, 0x1, 0x3, (1<<vdac_no))
    if range == 1:
        if gain == 0:                                       #1: 2.5V full scale, 0: 5V full scale
            dev_write_b_I2C(slv_add, 0x1, 0x8, 0xaa)
        else:
            dev_write_b_I2C(slv_add, 0x1, 0x8, 0xff)

    else:
        if gain == 0:                                       # 1: 2.5V full scale, 0: 5V full scale
            dev_write_b_I2C(slv_add, 0x1, 0x8, 0x0)
        else:
            dev_write_b_I2C(slv_add, 0x1, 0x8, 0x55)
    vdac_code(vdac_no,code)

def vdac_code(vdac_no,code):
    dev_write_b_I2C(0x41, 0x2, vdac_no, code)

def vdacBroadcast(slv_add, vdacs, code):
    a= 0
    for i in range(len(vdacs)):
        a += (1<<vdacs[i])
    dev_write_b_I2C(slv_add, 0x1, 0x5, a)
    dev_write_b_I2C(slv_add, 0x1, 0x3, code)

def vdacSyncLoad(slv_add, vdac_no):
    dev_write_b_I2C(slv_add, 0x1, 0x3, (1 << vdac_no))
    dev_write_b_I2C(slv_add, 0x1, 0x4, (1 << vdac_no))
    dev_write_b_I2C(slv_add, 0x1, 0x13, 0)

def vdacClearExt(slv_add, vdac_no, code):
    dev_write_b_I2C(slv_add, 0x1, 0x3, (1 << vdac_no))
    dev_write_b_I2C(slv_add, 0x1, 0xf, (1<<vdac_no))
    dev_write_b_I2C(slv_add, 0x1, 0x11, code)
    dev_write_b_I2C(slv_add, 0x1, 0x13, 1)

def vdacSoftClear(slv_add, vdac_no, code):
    dev_write_b_I2C(slv_add, 0x1, 0x3, (1 << vdac_no))
    dev_write_b_I2C(slv_add, 0x1, 0xf, (1 << vdac_no))
    dev_write_b_I2C(slv_add, 0x1, 0x10, code)
    dev_write_b_I2C(slv_add, 0x1, 0x12,(1 << vdac_no))

def vdacPdEn(slv_add, vdac_no):
    dev_write_b_I2C(slv_add, 0x1, 0x6, (1<<vdac_no))


#IDAC
def enableIDAC(slv_add, idac_no, range, code):
    dev_write_b_I2C(slv_add, 0x1, 0x3, 1<<(idac_no+4))
    if range == 0:
        dev_write_b_I2C(slv_add, 0x1, 0x18, 0x0)
    elif range == 1:
        dev_write_b_I2C(slv_add, 0x1, 0x18, 0x05)
    idac_code(slv_add,idac_no,code)

def idac_code(slv_add,idac_no,code):
    dev_write_b_I2C(slv_add, 0x2, (idac_no+4), code)

def idacBroadcast(slv_add, idacs, code):
    a=0
    for i in range(len(idacs)):
        a += 0xf + (1<<(idacs[i]+4))
    dev_write_b_I2C(slv_add, 0x1, 0x5, a)
    dev_write_b_I2C(slv_add, 0x1, 0x3, code)

def idacSyncLoad(slv_add, idac_no):
    dev_write_b_I2C(slv_add, 0x1, 0x3, (idac_no + 4))
    dev_write_b_I2C(slv_add, 0x1, 0x4, (idac_no+4))
    dev_write_b_I2C(slv_add, 0x1, 0x14, 1)

def idacClearExt(slv_add, idac_no, code):
    dev_write_b_I2C(slv_add, 0x1, 0x3, (1<<(idac_no+4)))
    dev_write_b_I2C(slv_add, 0x1, 0xf, (1<<(idac_no+4)))
    dev_write_b_I2C(slv_add, 0x1, 0x10, code)
    dev_write_b_I2C(slv_add, 0x1, 0x13, 1)

def idacSoftClear(slv_add, idac_no, code):
    dev_write_b_I2C(slv_add, 0x1, 0x3, (1 << (idac_no + 4)))
    dev_write_b_I2C(slv_add, 0x1, 0xf, (1 << (idac_no + 4)))
    dev_write_b_I2C(slv_add, 0x1, 0x10, code)
    dev_write_b_I2C(slv_add, 0x1, 0x12,(1 << (idac_no + 4)))

def idacPdEn(slv_add, idac_no):
    dev_write_b_I2C(slv_add, 0x1, 0x6, (1<<(idac_no+4)))


#ADC
def configADC(slv_add, adc_cfg_reg, adc_channel, averaging, acq_time):
    if averaging == 0:
        dev_write_b_I2C(slv_add, 0x7, adc_cfg_reg, (acq_time*0x100)+adc_channel)
    elif averaging == 1:
        dev_write_b_I2C(slv_add, 0x7, adc_cfg_reg, (acq_time*0x100)+0x40+adc_channel)
    elif averaging == 2:
        dev_write_b_I2C(slv_add, 0x7, adc_cfg_reg, (acq_time*0x100)+0x80+adc_channel)
    else:
        dev_write_b_I2C(slv_add, 0x7, adc_cfg_reg, (acq_time*0x100)+0xc0+adc_channel)

def adcRead(slv_add, adc_cfg_reg):
    return dev_read_b_I2C(slv_add,0x9,adc_cfg_reg)

def enADC(slv_add):
    dev_write_b_I2C(slv_add, 0x7, 0x62, 1)
    dev_write_b_I2C(slv_add, 0x7, 0x63, 1)

def adcPwdwn(slv_add):
    dev_write_b_I2C(slv_add, 0x1, 0x17, 0)



#TIAN
def tianVbiasSet(slv_add, tia_no, code):
    dev_write_b_I2C(slv_add, 0x11, tia_no, code)

def tianGainSet(slv_add, tia_no, gain_set):
    dev_write_b_I2C(slv_add, 0x11, tia_no + 4, gain_set)

def tianPwrDwn(slv_add, tia_no):
    dev_write_b_I2C(slv_add, 0x11, 0x8, 1 << tia_no)


#TIAP
def tiapVbiasSet(slv_add, tia_no, code):
    dev_write_b_I2C(slv_add, 0x12, tia_no, code)

def tiapGainSet(slv_add, tia_no, gain_set):
    dev_write_b_I2C(slv_add, 0x12, tia_no + 4, gain_set)

def tiapPwrDwn(slv_add, tia_no):
    dev_write_b_I2C(slv_add, 0x12, 0x8, 1 << tia_no)


#BOOST
def enBoost(slv_add, clk_sel):
    dev_write_b_I2C(slv_add, 0xb, 0x2, (clk_sel << 1)+1)

def boostOutSet(slv_add, code):
    dev_write_b_I2C(slv_add, 0xb, 0x3, code)

def boostCurrLmt(slv_add, curr_sel):
    dev_write_b_I2C(slv_add, 0xb, 0x4, curr_sel)


#BUCK
def enBuck(slv_add, code):
    dev_write_b_I2C(slv_add, 0xb, 0, 1)
    dev_write_b_I2C(slv_add, 0xb, 1, code)


#NRAIL
def nrailEn(slv_add, pwm_duty_sel, code):
    dev_write_b_I2C(slv_add, 0xb, 0x5, (pwm_duty_sel << 4)+1)
    nrailVset(slv_add, code)

def nrailVset(slv_add, code):
    dev_write_b_I2C(slv_add, 0xb, 0x6, code)


#TRIMS
def vrefTempcoTrim(slv_add, value):
    dev_write_b_I2C(slv_add, 0x20, 0, value << 8)

def refClockTrim(slv_add, code):
    dev_write_b_I2C(slv_add, 0x41, 1, 2)
    dev_write_b_I2C(slv_add, 0x25, 2, code)

def fastClockTrim(slv_add, code):
    dev_write_b_I2C(slv_add, 0x41, 1, 1)
    dev_write_b_I2C(slv_add, 0x25, 3, code)

def ibiasTrim(slv_add, code):
    dev_write_b_I2C(slv_add, 0x20, 0, code)

def vdacOffTrim(vdac_no,trim_val):
    if(vdac_no==0):
        dev_write_b_I2C(0x41,0x22,0,trim_val)
    elif(vdac_no==1):
        dev_write_b_I2C(0x41,0x22,0,trim_val<<8)
    elif(vdac_no==2):
        dev_write_b_I2C(0x41,0x22,1,trim_val)
    else:
        dev_write_b_I2C(0x41,0x22,1,trim_val<<8)

def vdacScaleTrim(vdac_no,trim_val):
    if(vdac_no==0):
        dev_write_b_I2C(0x41,0x22,2,trim_val)
    elif(vdac_no==1):
        dev_write_b_I2C(0x41,0x22,2,trim_val<<8)
    elif(vdac_no==2):
        dev_write_b_I2C(0x41,0x22,3,trim_val)
    else:
        dev_write_b_I2C(0x41,0x22,3,trim_val<<8)

def idacOffTrim(vdac_no,trim_val):
    if(vdac_no==0):
        dev_write_b_I2C(0x41,0x20,2,trim_val<<8)
    elif(vdac_no==1):
        dev_write_b_I2C(0x41,0x20,3,trim_val<<8)
    elif(vdac_no==2):
        dev_write_b_I2C(0x41,0x21,0,trim_val<<8)
    else:
        dev_write_b_I2C(0x41,0x21,1,trim_val<<8)

def idacScaleTrim(vdac_no,trim_val):
    if(vdac_no==0):
        dev_write_b_I2C(0x41,0x21,2,trim_val)
    elif(vdac_no==1):
        dev_write_b_I2C(0x41,0x21,2,trim_val<<8)
    elif(vdac_no==2):
        dev_write_b_I2C(0x41,0x21,3,trim_val)
    else:
        dev_write_b_I2C(0x41,0x21,3,trim_val<<8)

#TEC
def tecEn(slv_add, mode, oc_en):
    if mode==0:      #Mode 0: PID mode, 1: Manual mode
        if oc_en == 1:      #oc_en 1: Over current protection enabled, 0: Over current protection disabled
            dev_write_b_I2C(slv_add, 0xc, 0x7, 0x5)
        if oc_en == 0:
            dev_write_b_I2C(slv_add, 0xc, 0x7, 0x1)
        dev_write_b_I2C(slv_add, 0xc, 0xa, 1)

    if mode == 1:
        if oc_en == 1:
            dev_write_b_I2C(slv_add, 0xc, 0x7, 0x7)
        if oc_en == 0:
            dev_write_b_I2C(slv_add, 0xc, 0x7, 0x3)

def pidSetpoint(slv_add, code):
    dev_write_b_I2C(slv_add, 0xc, 0, code)

def manPwm(slv_add, code):
    dev_write_b_I2C(slv_add, 0xc, 0x8, code)

def pidCoef(slv_add, prop, int, diff):
    dev_write_b_I2C(slv_add, 0xc, 0x1, prop)
    dev_write_b_I2C(slv_add, 0xc, 0x2, int)
    dev_write_b_I2C(slv_add, 0xc, 0x3, diff)

def pidShift(slv_add, pshift, ishift, dshift):
    dev_write_b_I2C(slv_add, 0xc, 0x4, (dshift << 8)+(ishift << 4)+pshift)

def pidMaxClamp(slv_add, code):
    dev_write_b_I2C(slv_add, 0xc, 0x5, code)

def pidMinClamp(slv_add, code):
    dev_write_b_I2C(slv_add, 0xc, 0x6, code)









