#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    ????
    Created on ??.??.????
    @author: Tobias Badertscher

"""
import os
import logging
from pyRN2483 import RN2483


class TheThingsNetwork:
    
    def __init__(self, dev):
        self._log = logging.getLogger("RN2483")
        self._dev = dev
    
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


if __name__ == '__main__':
    ter_pat = '/dev/ttyUSB%d'
    cur_ter = 0
    term = ter_pat % cur_ter
    if os.path.exists(term):
        rn2483 = RN2483(term)
        tnn=TheThingsNetwork(rn2483)
        #rn2483.setup()
        print(tnn.showStatus())
