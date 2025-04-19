#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

controller_spec = ["implementation_id", "Controller", 
                   "type_name",         "Controller", 
                   "description",       "Controller component", 
                   "version",           "1.0", 
                   "vendor",            "Shinji Kurihara, AIST", 
                   "category",          "example", 
                   "activity_type",     "DataFlowComponent", 
                   "max_instance",      "10", 
                   "language",          "Python", 
                   "lang_type",         "SCRIPT",
                   ""]

class Controller(OpenRTM_aist.DataFlowComponentBase):
  def __init__(self, manager):
    OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
    return
    
  def onInitialize(self):
    self._d_in = RTC.TimedFloat(RTC.Time(0,0),0)
    self._inIn = OpenRTM_aist.InPort("in", self._d_in)
    self._d_out = RTC.TimedFloat(RTC.Time(0,0),0)
    self._outOut = OpenRTM_aist.OutPort("out", self._d_out)

    # Set InPort buffers
    self.addInPort("in",self._inIn)
    
    # Set OutPort buffers
    self.addOutPort("out",self._outOut)
    
    return RTC.RTC_OK


  def onExecute(self, ec_id):
    if self._inIn.isNew():
      data = self._inIn.read()
      print "Controller Received data: ", data.data
      self._d_out.data = data.data *2
      self._outOut.write()
    return RTC.RTC_OK
  



def ControllerInit(manager):
  profile = OpenRTM_aist.Properties(defaults_str=controller_spec)
  manager.registerFactory(profile,
                          Controller,
                          OpenRTM_aist.Delete)

def MyModuleInit(manager):
  ControllerInit(manager)

  # Create a component
  comp = manager.createComponent("Controller")



def main():
  mgr = OpenRTM_aist.Manager.init(sys.argv)
  mgr.setModuleInitProc(MyModuleInit)
  mgr.activateManager()
  mgr.runManager()

if __name__ == "__main__":
  main()
