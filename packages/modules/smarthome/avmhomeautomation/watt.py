#!/usr/bin/python3
import avmcommon

interface = avmcommon.AVMHomeAutomation()
interface.connect()
interface.getActualPower()
