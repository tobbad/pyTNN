#!/bin/env python3
'''
Python module to controll a RN2483 over tty interface.
'''

from serial import Serial, serialutil
import time
import logging
import os
import sys


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def prop(func):
    nitem = func.__name__.split('_')
    #logging.info("%s %s" % (func.__name__,  str(nitem)))
    def new_func(self,  value = None):
        if value == None:
            data = "%s get %s" %  tuple(nitem)
        else:
            data ="%s set %s %s" % (nitem[0],  nitem[1],  value)
        self._write(data)
        return self._read()
    return new_func

def get_func(comp_name, para_name, min_para_cnt, is_command, is_setable, is_getable, convert):
        def new_func(self, value = ()):
            if isinstance(value, (int, float, bool, str)):
                value = (value,)
            logging.info("Func %s_%s %s called" % (comp_name, para_name,  value ))
            data = b""
            pcnt = len(value)
            conv = None
            data = " " + " ".join([str(i) for i in value]) if value else ""
            if (is_setable is True and pcnt >  min_para_cnt) or is_command is True:
                data = "%s %s%s%s" % ( comp_name, "" if is_command else "set ", para_name, data)
            if (is_getable is True and pcnt ==  min_para_cnt):
                data = "%s get %s%s" % ( comp_name, para_name, data)
                conv = convert
            self._write(data)
            res = self._read()
            if conv:
                if isinstance(conv[0], int):
                    res = conv[0](res, conv[1])
                elif isinstance(conv[0], float):
                    if res == "none":
                        res = None
                    else:
                        res = float(res)
            logging.debug(">> Result: %s" % (res))
            return res
        return new_func



def CLASS_PROP(cls):
    for item in cls.ADD_METHOD:
        fun = get_func(*item)
        fun.__name__ = "%s_%s"% (item[0],item[1].replace(" ",'_'))
        setattr(cls, fun.__name__, fun)
        #logging.debug("Created %s" % (fun.__name__))
    return cls

@CLASS_PROP
class RN2483:

    CRLF=b"\r\n"

    DEBUG = False

    BAUDRATE = 57600

    ADD_METHOD = [
    # Layer  Item   min_para_cnt, is_command, is_Set_able,  is_Get_able, Returned datatype (str )
     ('sys', 'ver', 0,            False,           False,          True,    (int, 10)),
     ('sys', 'nvm', 2,            False,           True,           True,    (int, 10)),
     ('sys', 'vdd', 0,            False,           False,          True,    (int, 10)),
     ('sys', 'hweui', 0,          False,           False,          True,    (int, 16)),
     ('sys', 'pindig', 1,         False,           True,           True,    (int, 10)),
     ('sys', 'sleep', 0,          True,            False,          False,   None),
     ('sys', 'factoryRESET', 0,   True,            False,          False,   None),
     ('mac', 'reset', 1,          True,            False,          False,   None),
     ('mac', 'tx', 3,             True,            False,          False,   None),
     ('mac', 'join', 1,           True,            False,          False,   None),
     ('mac', 'save', 0,           True,            False,          False,   None),
     ('mac', 'forceENABLE', 0,    True,            False,          False,   None),
     ('mac', 'pause', 0,          True,            False,          False,   None),
     ('mac', 'resume', 0,         True,            False,          False,   None),
     ('mac', 'devaddr', 0,        False,            True,          True,    (int, 16)),
     ('mac', 'deveui', 0,         False,            True,          True,    (int, 16)),
     ('mac', 'appeui', 0,         False,            True,          True,    (int, 16)),
     ('mac', 'nwkskey', 0,        False,            True,          False,   None),
     ('mac', 'appskey', 0,        False,            True,          False,   None),
     ('mac', 'appkey', 0,         False,            True,          False,   None),
     ('mac', 'dr', 0,             False,            True,          True,    (int, 10)),
     ('mac', 'band', 0,           False,            True,          True,    (int, 10)),
     ('mac', 'pwridx', 0,         False,            True,          True,    (int, 10)),
     ('mac', 'adr', 0,            False,            True,          True,    None),
     ('mac', 'bat', 0,            False,            True,          False,   None),
     ('mac', 'retx', 0,           False,            True,          True,    (int, 10)),
     ('mac', 'linkchk', 0,        False,            True,          False,   None),
     ('mac', 'rxdelay1', 0,       False,            True,          True,    (int, 10)),
     ('mac', 'rxdelay2', 0,       False,            False,         True,    (int, 10)),
     ('mac', 'ar', 0,             False,            True,          True,    None),
     ('mac', 'rx2', 1,            False,            True,          True,    (int, 10)),
     ('mac', 'dcyleps', 0,        False,            False,         True,    (int, 10)),
     ('mac', 'mrgn', 0,           False,            False,         True,    (int, 10)),
     ('mac', 'gwbn', 0,           False,            False,         True,    (int, 10)),
     ('mac', 'status', 0,         False,            False,         True,    (int, 10)),
     ('mac', 'sync', 1,           False,            True,          True,    (int, 10)),
     ('mac', 'upctr', 0,          False,            True,          True,    (int, 10)),
     ('mac', 'dnctr', 0,          False,            True,          True,    (int, 10)),
     ('mac', 'ch freq', 1,        False,            True,          True,    (int, 10)),
     ('mac', 'ch dcycle', 1,      False,            True,          True,    (int, 10)),
     ('mac', 'ch drrange', 1,     False,            True,          True,    (int, 10)),
     ('mac', 'ch status', 1,      False,            True,          True,    None),
     ('radio', 'bt', 0,           False,            True,          True,    float),
     ('radio', 'mod', 0,          False,            True,          True,    None),
     ('radio', 'freq', 0,         False,            True,          True,    (int, 10)),
     ('radio', 'pwr', 0,          False,            True,          True,    (int, 10)),
     ('radio', 'sf', 0,           False,            True,          True,    None),
     ('radio', 'afcwb', 0,        False,            True,          True,    float),
     ('radio', 'rxbw', 0,         False,            True,          True,    float),
     ('radio', 'bitrate', 0,      False,            True,          True,    (int, 10)),
     ('radio', 'fdev', 0,         False,            True,          True,    (int, 10)),
     ('radio', 'prlen', 0,        False,            True,          True,    (int, 10)),
     ('radio', 'crc', 0,          False,            True,          True,    None),
     ('radio', 'iqi', 0,          False,            True,          True,    None),
     ('radio', 'cr', 0,           False,            True,          True,    None),
     ('radio', 'wdt', 0,          False,            True,          True,    (int, 10)),
     ('radio', 'bw', 0,           False,            True,          True,    (int, 10)),
     ('radio', 'snr', 0,          False,            False,         True,    (int, 10)),
     ('radio', 'sync', 0,         False,            True,          True,    (int, 10)),
     ]


    def __init__(self,  dev_name,  debug = False):
        self._log = logging.getLogger("RN2483")
        self.DEBUG = debug
        self._byte_wait_s =  15.0/self.BAUDRATE
        self._read_delay_s = 0.9
        self.com = Serial(dev_name,  self.BAUDRATE,  timeout=2*self._byte_wait_s)
        res = self.sys_reset()
        self._log.debug("sys reset result \"%s\"" % (res))

    def _write(self,  data,  last = True):
        data=bytes(data,  'utf-8') + (self.CRLF if last else b"")
        self._log.debug("Send data \"%s\"" % data)
        start = time.time()
        self.com.write(data)
        stop = time.time()
        sleep_time=float(15*len(data))/self.BAUDRATE
        time.sleep(sleep_time)
        self._log.debug("Sent %d bits in %f s (sleep %f ms)" % (len(data)*8, stop-start, sleep_time))
        return

    def _read(self):
        do_read = True
        data = b''
        while do_read:
            data += self.com.read(1)
            time.sleep(self._byte_wait_s)
            if len(data)>2 and data[-2:]==self.CRLF:
                do_read = False
        self._log.info("Received data \"%s\"" % data)
        data = data.replace(self.CRLF, b'').decode('utf-8')
        return data

    def reset(self):
        self.sys.reset()
        time.sleep(0.5)
        return self._read()

    def setup(self):
        self.mac_devaddr("02011E16")
        self.mac_appskey("2B7E151628AED2A6ABF7158809CF4F3C")
        self.mac_nwkskey("2B7E151628AED2A6ABF7158809CF4F3C")
        self.mac_adr("off")
        self.mac_rx2((3,"869525000"))
        self.mac_join("abp")

    def send(self,  data):
        port = 1
        self._log.info("Send \"%s\" to port %d" % (data, port))
        tx_data = ("uncnf", port)
        var = ""
        for ch in data:
            var += ("%02X" % ord(ch))
        tx_data += (var,)
        res = self.mac_tx(tx_data)
        return res

    def run(self):
        while True:
            self.send("Hello LoRa World %s" % (time.strftime("%d.%m.%Y %H:%M:%S")))
            time.sleep(5)



class TheThingsNetwork:
    
    def __init__(self, dev):
        self._dev = dev
    
    def reset(self):
        return self._dev.reset()

    def getHardwareEui(self):
        return self.sys_hweui()

    def getAppEui(self):
        return self.mac_appeui()
    
    def showStatus(self):
        res = ()
        res += ("EUI: %08X" % self.getHardwareEui(),)
        res += ("Battery: %d mV" % self.sys_vdd(),)
        res += ("DevEUI: %08X" % self.mac_deveui(),)
        res += ("AppEUI: %08X" % self.mac_appeui(),)
        res += ("Data Rate: %d" % self.radio_bitrate(),)
        res += ("RX Delay 1: %d" % self.mac_rxdelay1(),)
        res += ("RX Delay 2: %d" % self.mac_rxdelay2(),)
        return "\n".join(res)


if __name__ == '__main__':
    ter_pat = '/dev/ttyUSB%d'
    cur_ter = 0
    while True:
        rn2483 = None
        term = ter_pat % cur_ter
        if os.path.exists(term):
            rn2483 = RN2483(term)
            #rn2483.setup()
            print(rn2483.showStatus())
            sys.exit()
        else:
            cur_ter = (cur_ter +1)%2
        if rn2483 is not None:
            while os.path.exists(term):
                rn2483.send("Hello LoRa World %s" % (time.strftime("%d.%m.%Y %H:%M:%S")))
                time.sleep(5)

