#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Implementation of TheThingsNetwork API
    Created on 9.3.2018
    @author: Tobias Badertscher

"""
import os
import inspect # TODO Remove when all fuinctions are implemented
import logging
from enum import Enum
from pyRN2483 import RN2483

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
log=logging.getLogger('__main__')

class TTN:
    
    RETX = 7
    
    class RESP(Enum):   
        TTN_ERROR_SEND_COMMAND_FAILED = -1
        TTN_ERROR_UNEXPECTED_RESPONSE = -10
        TTN_SUCCESSFUL_TRANSMISSION = 1
        TTN_SUCCESSFUL_RECEIVE = 2
    
    class FP(Enum):
        EU868 = 0
        US915 = 1
        AS920_923 = 2
        AS923_925 = 3
        KR920_923 = 4
    
    class PWRIDX(Enum):
        EU868 = 1
        US915 = 5
        AS920_923 = 1 # TODO: should be 0, but the current RN2903AS firmware doesn't accept that value (probably still using EU868: 1=14dBm)
        AS923_925 = 1 # TODO: should be 0
        KR920_923 = 1 # TODO: should be 0
        
    
    
    def __init__(self, dev):
        self._log = logging.getLogger("TTN")
        self._dev = dev
        self._cb = None
    
    def _configureEU868(self):
        self._dev.mac_rx2(3, 869525000)
        self._dev.mac_ch_drrange(1, 0, 6)
        freq = 867100000
        for ch in range(8):
            self._dev.mac_ch_dcycle(ch, 799)
            if ch > 2:
                self._dev.mac_ch_freq(ch, freq)
                self._dev.mac_ch_drrange(ch, 0, 5)
                self._dev.mac_ch_status(ch, "on")
                freq += 200000
        self._dev.mac_pwridx(TTN.PWRIDX.EU868)
    
    def _configureUS915(self, fsb):
        self._log.error("%s not implemented" % (inspect.stack()[0][3]))
    
    def _configureAS920_923(self):
        self._log.error("%s not implemented" % (inspect.stack()[0][3]))
    
    def _configureAS923_925(self):
        self._log.error("%s not implemented" % (inspect.stack()[0][3]))
    
    def _configureKR920_923(self):
        self._log.error("%s not implemented" % (inspect.stack()[0][3]))
        
    def configureChannels(self, fsb):
        if fsb == TTN.FP.EU868:
            self._configureEU868()
        elif fsb == TTN.FP.US915:
            self._configureUS915(fsb)
        elif fsb == TTN.FP.AS920_923:
            self._configureAS920_923()
        elif fsb == TTN.FP.AS923_925:
            self._configureAS923_925()
        elif fsb == TTN.FP.KR920_923:
            self._configureKR920_923();
        else:
            self._log.error("Invalid FP");
        self._com.mac_retx(TTN.RETX)
    
    def reset(self):
        return self._dev.reset()

    def getHardwareEui(self):
        return self._dev.sys_hweui()

    def getAppEui(self):
        return self._dev.mac_appeui()
    
    def showStatus(self):
        res = ()
        res += ("EUI: %08X" % self.getHardwareEui(),)
        res += ("Battery: %d mV" % self._dev.sys_vdd(),)
        res += ("DevEUI: %08X" % self.getAppEui(),)
        res += ("AppEUI: %08X" % self._dev.mac_appeui(),)
        res += ("Data Rate: %d" % self._dev.radio_bitrate(),)
        res += ("RX Delay 1: %d" % self._dev.mac_rxdelay1(),)
        res += ("RX Delay 2: %d" % self._dev.mac_rxdelay2(),)
        return "\n".join(res)

    def onMessage(self, callback):
        self._cb = callback
        
    def _join(self, retries, retryDelay):
        self._log.error("%s not implemented" % (inspect.stack()[0][3]))
        return False
                
    def join(self, appEui, appKey, retries=-1, retryDelay=10000):
        prov_res = self.provision(appEui, appKey)
        _join_res = self._join(retries, retryDelay)
        return prov_res and _join_res
    
    def personalize(self, devAddr, nwkSKey, appSKey):
        self._log.error("%s not implemented" % (inspect.stack()[0][3]))
    
    def sendBytes(self, payload, port=1, confirme=False, sf=0):
        return self.TTN_ERROR_SEND_COMMAND_FAILED

    def poll(self, port=1, confirm=False):
        return self.sendBytes(b'\x00', confirm)

    def provision(self, appEui, appKey):
        self._log.error("%s not implemented" % (inspect.stack()[0][3]))
    
    def sleep(self, seconds):
        self._dev.sys_sleep(seconds*1000)
    
    def wake(self):
        self._dev.wake()

    def saveState(self):
        self._dev.mac_save()

    def linkCheck(self, seconds):
        self._log.error("%s not implemented" % (inspect.stack()[0][3]))
        
    def getLinkCheckGateways(self):
        self._log.error("%s not implemented" % (inspect.stack()[0][3]))
        
    def getLinkCheckMargin(self):
        self._log.error("%s not implemented" % (inspect.stack()[0][3]))
        
    def getVDD(self):
        return self._dev.sys_vdd()

if __name__ == '__main__':
    ter_pat = '/dev/ttyUSB%d'
    cur_ter = 0
    term = ter_pat % cur_ter
    if os.path.exists(term):
        rn2483 = RN2483(term)
        tnn=TTN(rn2483)
        #rn2483.setup()
        print(tnn.showStatus())
    else:
        log.error("%s does not exist" % (term))