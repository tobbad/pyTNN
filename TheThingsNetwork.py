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
from pyRN2483 import RN2483


class TheThingsNetwork:
    
    
    TTN_ERROR_SEND_COMMAND_FAILED = -1
    TTN_ERROR_UNEXPECTED_RESPONSE = -10
    TTN_SUCCESSFUL_TRANSMISSION = 1
    TTN_SUCCESSFUL_RECEIVE = 2

    
    
    def __init__(self, dev):
        self._log = logging.getLogger("RN2483")
        self._dev = dev
        self._cb = None
    
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
        
    def join(self, appEui, appKey, retries=-1, retryDelay=10000):
        self._log.error("%s not implemented" % (inspect.stack()[0][3]))
    
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
        tnn=TheThingsNetwork(rn2483)
        #rn2483.setup()
        print(tnn.showStatus())
