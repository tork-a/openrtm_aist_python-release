#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file Manager.py
# @brief RTComponent manager class
# @date $Date: $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import threading
import string
import signal, os
import traceback
import sys
import time
from omniORB import CORBA, PortableServer
from types import IntType, ListType

import OpenRTM_aist
import RTC
import SDOPackage


#------------------------------------------------------------
# static var
#------------------------------------------------------------

##
# @if jp
# @brief ͣ��� Manager �ؤΥݥ���
# @else
# @brief The pointer to the Manager
# @endif
manager = None

##
# @if jp
# @brief ͣ��� Manager �ؤΥݥ��󥿤��Ф��� mutex
# @else
# @brief The mutex of the pointer to the Manager 
# @endif
mutex = threading.RLock()


##
# @if jp
# @brief ��λ����
#
# �ޥ͡������λ������
#
# @param signum �����ʥ��ֹ�
# @param frame ���ߤΥ����å��ե졼��
#
# @else
#
# @endif
def handler(signum, frame):
  mgr = OpenRTM_aist.Manager.instance()
  mgr.terminate()



##
# @if jp
# @class Manager
# @brief Manager ���饹
#
# ����ݡ��ͥ�ȤʤɳƼ�ξ��������Ԥ��ޥ͡����㥯�饹��
#
# @since 0.2.0
#
# @else
# @class Manager
# @brief Manager class
# @endif
class Manager:
  """
  """



  ##
  # @if jp
  # @brief ���ԡ����󥹥ȥ饯��
  #
  # ���ԡ����󥹥ȥ饯��
  #
  # @param self
  # @param _manager ���ԡ����ޥ͡����㥪�֥�������(�ǥե������:None)
  #
  # @else
  # @brief Protected Copy Constructor
  #
  # @endif
  def __init__(self, _manager=None):
    self._initProc   = None
    self._runner     = None
    self._terminator = None
    self._compManager = OpenRTM_aist.ObjectManager(self.InstanceName)
    self._factory = OpenRTM_aist.ObjectManager(self.FactoryPredicate)
    self._ecfactory = OpenRTM_aist.ObjectManager(self.ECFactoryPredicate)
    self._terminate = self.Term()
    self._ecs = []
    self._timer = None
    self._orb = None
    self._poa = None
    self._poaManager = None 
    self._finalized = self.Finalized()
    signal.signal(signal.SIGINT, handler)
    
    return


  ##
  # @if jp
  # @brief �ޥ͡�����ν����
  #
  # �ޥ͡�������������� static �ؿ���
  # �ޥ͡�����򥳥ޥ�ɥ饤�������Ϳ���ƽ�������롣
  # �ޥ͡��������Ѥ�����ϡ�ɬ�����ν�������дؿ� init() ��
  # �ƤФʤ���Фʤ�ʤ���
  # �ޥ͡�����Υ��󥹥��󥹤����������ˡ�Ȥ��ơ�init(), instance() ��
  # 2�Ĥ� static �ؿ����Ѱդ���Ƥ��뤬���������init()�Ǥ����Ԥ��ʤ����ᡢ
  # Manager ����¸���֤ΰ��ֺǽ�ˤ�init()��Ƥ�ɬ�פ����롣
  #
  # ���ޥ͡�����ν��������
  # - initManager: ����������config�ե�������ɤ߹��ߡ����֥����ƥ�����
  # - initLogger: Logger�����
  # - initORB: ORB �����
  # - initNaming: NamingService �����
  # - initExecutionContext: ExecutionContext factory �����
  # - initTimer: Timer �����
  #
  # @param argv ���ޥ�ɥ饤�����
  # 
  # @return Manager ��ͣ��Υ��󥹥��󥹤λ���
  #
  # @else
  # @brief Initializa manager
  #
  # This is the static function to tintialize the Manager.
  # The Manager is initialized by given arguments.
  # At the starting the manager, this static function "must" be called from
  # application program. The manager has two static functions to get 
  # the instance, "init()" and "instance()". Since initializing
  # process is only performed by the "init()" function, the "init()" has
  # to be called at the beginning of the lifecycle of the Manager.
  # function.
  #
  # @param argv The array of the command line arguments.
  #
  # @endif
  def init(*arg):
    global manager
    global mutex
    
    if len(arg) == 1:
      argv = arg[0]
    elif len(arg) == 2 and \
             isinstance(arg[0], IntType) and \
             isinstance(arg[1], ListType):
      # for 0.4.x
      argv = arg[1]
    else:
      print "Invalid arguments for init()"
      print "init(argc,argv) or init(argv)"
        
    if manager is None:
      guard = OpenRTM_aist.ScopedLock(mutex)
      if manager is None:
        manager = Manager()
        manager.initManager(argv)
        manager.initLogger()
        manager.initORB()
        manager.initNaming()
        manager.initFactories()
        manager.initExecContext()
        manager.initComposite()
        manager.initTimer()
        manager.initManagerServant()

    return manager
  
  init = staticmethod(init)


  ##
  # @if jp
  # @brief �ޥ͡�����Υ��󥹥��󥹤μ���
  #
  # �ޥ͡�����Υ��󥹥��󥹤�������� static �ؿ���
  # ���δؿ���Ƥ����ˡ�ɬ�����ν�����ؿ� init() ���ƤФ�Ƥ���ɬ�פ����롣
  #
  # @return Manager ��ͣ��Υ��󥹥��󥹤λ���
  # 
  # @else
  #
  # @brief Get instance of the manager
  #
  # This is the static function to get the instance of the Manager.
  # Before calling this function, ensure that the initialization function
  # "init()" is called.
  #
  # @return The only instance reference of the manager
  #
  # @endif
  def instance():
    global manager
    global mutex
    
    if manager is None:
      guard = OpenRTM_aist.ScopedLock(mutex)
      if manager is None:
        manager = Manager()
        manager.initManager(None)
        manager.initLogger()
        manager.initORB()
        manager.initNaming()
        manager.initFactories()
        manager.initExecContext()
        manager.initComposite()
        manager.initTimer()
        #manager.initManagerServant()

    return manager

  instance = staticmethod(instance)


  ##
  # @if jp
  # @brief �ޥ͡����㽪λ����
  #
  # �ޥ͡�����ν�λ������¹Ԥ��롣
  #
  # @param self
  #
  # @else
  #
  # @endif
  def terminate(self):
    if self._terminator:
      self._terminator.terminate()


  ##
  # @if jp
  # @brief �ޥ͡����㡦����åȥ�����
  #
  # �ޥ͡�����ν�λ������¹Ԥ��롣
  # ORB��λ�塢Ʊ�����äƽ�λ���롣
  #
  # @param self
  #
  # @else
  #
  # @endif
  def shutdown(self):
    self._rtcout.RTC_TRACE("Manager.shutdown()")
    self.shutdownComponents()
    self.shutdownNaming()
    self.shutdownORB()
    self.shutdownManager()

    if self._runner:
      self._runner.wait()
    else:
      self.join()

    self.shutdownLogger()
    global manager
    if manager:
      manager = None


  ##
  # @if jp
  # @brief �ޥ͡����㽪λ�������Ԥ���碌
  #
  # Ʊ�����뤿�ᡢ�ޥ͡����㽪λ�������Ԥ���碌��Ԥ���
  #
  # @param self
  #
  # @else
  #
  # @endif
  def join(self):
    self._rtcout.RTC_TRACE("Manager.wait()")
    guard = OpenRTM_aist.ScopedLock(self._terminate.mutex)
    self._terminate.waiting += 1
    del guard
    while 1:
      guard = OpenRTM_aist.ScopedLock(self._terminate.mutex)
      #if self._terminate.waiting > 1:
      if self._terminate.waiting > 0:
        break
      del guard
      time.sleep(0.001)


  ##
  # @if jp
  #
  # @brief ������ץ�������Υ��å�
  #
  # ���Υ��ڥ졼�����ϥ桼�����Ԥ��⥸�塼�����ν�����ץ�������
  # �����ꤹ�롣���������ꤵ�줿�ץ�������ϡ��ޥ͡����㤬��������졢
  # �����ƥ��ֲ����줿�塢Ŭ�ڤʥ����ߥ󥰤Ǽ¹Ԥ���롣
  #
  # @param self
  # @param proc ������ץ�������δؿ��ݥ���
  #
  # @else
  #
  # @brief Run the Manager
  #
  # This operation sets the initial procedure call to process module
  # initialization, other user defined initialization and so on.
  # The given procedure will be called at the proper timing after the 
  # manager initialization, activation and run.
  #
  # @param proc A function pointer to the initial procedure call
  #
  # @endif
  def setModuleInitProc(self, proc):
    self._initProc = proc
    return


  ##
  # @if jp
  #
  # @brief Manager�Υ����ƥ��ֲ�
  #
  # ���Υ��ڥ졼�����ϰʲ��ν�����Ԥ�
  # - CORBA POAManager �Υ����ƥ��ֲ�
  # - �ޥ͡�����CORBA���֥������ȤΥ����ƥ��ֲ�
  # - Manager ���֥������Ȥؤν�����ץ�������μ¹�
  #
  # ���Υ��ڥ졼�����ϡ��ޥ͡�����ν�����塢runManager()
  # �����˸Ƥ�ɬ�פ����롣
  #
  # @param self
  #
  # @return �������(�����ƥ��ֲ�����:true������:false)
  #
  # @else
  #
  # @brief Activate Manager
  #
  # This operation do the following,
  # - Activate CORBA POAManager
  # - Activate Manager CORBA object
  # - Execute the initial procedure call of the Manager
  #
  # This operationo should be invoked after Manager:init(),
  # and before tunManager().
  #
  # @endif
  def activateManager(self):
    self._rtcout.RTC_TRACE("Manager.activateManager()")

    try:
      self.getPOAManager().activate()
      self._rtcout.RTC_TRACE("POA Manager activated.")
    except:
      self._rtcout.RTC_ERROR("Exception: POA Manager activation failed.")
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      return False

    mods = [s.strip() for s in self._config.getProperty("manager.modules.preload").split(",")]

    for i in range(len(mods)):
      if mods[i] is None or mods[i] == "":
        continue
      tmp = [mods[i]]
      OpenRTM_aist.eraseHeadBlank(tmp)
      OpenRTM_aist.eraseTailBlank(tmp)
      mods[i] = tmp[0]

      basename = os.path.basename(mods[i]).split(".")[0]
      basename += "Init"

      try:
        self._module.load(mods[i], basename)
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
        self.__try_direct_load(basename)

    if self._initProc:
      self._initProc(self)

    comps = [s.strip() for s in self._config.getProperty("manager.components.precreate").split(",")]
    for i in range(len(comps)):
      if comps[i] is None or comps[i] == "":
        continue
      tmp = [comps[i]]
      OpenRTM_aist.eraseHeadBlank(tmp)
      OpenRTM_aist.eraseTailBlank(tmp)
      comps[i] = tmp[0]

      self.createComponent(comps[i])

    return True


  ##
  # @if jp
  #
  # @brief Manager�μ¹�
  #
  # ���Υ��ڥ졼�����ϥޥ͡�����Υᥤ��롼�פ�¹Ԥ��롣
  # ���Υᥤ��롼����Ǥϡ�CORBA ORB�Υ��٥�ȥ롼������
  # ��������롣�ǥե���ȤǤϡ����Υ��ڥ졼�����ϥ֥�å�����
  # Manager::destroy() ���ƤФ��ޤǽ������ᤵ�ʤ���
  # ���� no_block �� true �����ꤵ��Ƥ�����ϡ������ǥ��٥�ȥ롼��
  # ��������륹��åɤ�ư�����֥�å������˽������᤹��
  #
  # @param self
  # @param no_block false: �֥�å��󥰥⡼��, true: �Υ�֥�å��󥰥⡼��
  #
  # @else
  #
  # @brief Run the Manager
  #
  # This operation processes the main event loop of the Manager.
  # In this main loop, CORBA's ORB event loop or other processes
  # are performed. As the default behavior, this operation is going to
  # blocking mode and never returns until manager::destroy() is called.
  # When the given argument "no_block" is set to "true", this operation
  # creates a thread to process the event loop internally, and it doesn't
  # block and returns.
  #
  # @param no_block false: Blocking mode, true: non-blocking mode.
  #
  # @endif
  def runManager(self, no_block=None):
    if no_block is None:
      no_block = False
      
    if no_block:
      self._rtcout.RTC_TRACE("Manager.runManager(): non-blocking mode")
      self._runner = self.OrbRunner(self._orb)
    else:
      self._rtcout.RTC_TRACE("Manager.runManager(): blocking mode")
      try:
        self._orb.run()
        self._rtcout.RTC_TRACE("Manager.runManager(): ORB was terminated")
        self.join()
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    return


  ##
  # @if jp
  # @brief [CORBA interface] �⥸�塼��Υ���
  #
  # ���ꤷ������ݡ��ͥ�ȤΥ⥸�塼�����ɤ���ȤȤ�ˡ�
  # ���ꤷ��������ؿ���¹Ԥ��롣
  #
  # @param self
  # @param fname   �⥸�塼��ե�����̾
  # @param initfunc ������ؿ�̾
  # 
  # @else
  #
  # @brief [CORBA interface] Load module
  #
  # Load module (shared library, DLL etc..) by file name,
  # and invoke initialize function.
  #
  # @param fname    The module file name
  # @param initfunc The initialize function name
  #
  # @endif
  def load(self, fname, initfunc):
    self._rtcout.RTC_TRACE("Manager.load(fname = %s, initfunc = %s)",
                           (fname, initfunc))
    try:
      fname_ = fname.split(os.sep)
      if len(fname_) > 1:
        fname_ = fname_[-1]
      else:
        fname_ = fname_[0]

      if not initfunc:
        mod = [s.strip() for s in fname_.split(".")]
        initfunc = mod[0]+"Init"
      path = self._module.load(fname, initfunc)
      self._rtcout.RTC_DEBUG("module path: %s", path)
    except:
      self.__try_direct_load(fname)

    return


  ##
  # @if jp
  #
  # @brief �⥸�塼��Υ������
  #
  # �⥸�塼��򥢥���ɤ���
  #
  # @param self
  # @param fname �⥸�塼��Υե�����̾
  # 
  # @else
  #
  # @brief Unload module
  #
  # Unload shared library.
  #
  # @param pathname Module file name
  #
  # @endif
  def unload(self, fname):
    self._rtcout.RTC_TRACE("Manager.unload()")
    self._module.unload(fname)
    return


  ##
  # @if jp
  #
  # @brief ���⥸�塼��Υ������
  #
  # �⥸�塼��򤹤٤ƥ�����ɤ���
  #
  # @param self
  #
  # @else
  #
  # @brief Unload module
  #
  # Unload all loaded shared library.
  #
  # @endif
  def unloadAll(self):
    self._rtcout.RTC_TRACE("Manager.unloadAll()")
    self._module.unloadAll()
    return


  ##
  # @if jp
  # @brief ���ɺѤߤΥ⥸�塼��ꥹ�Ȥ��������
  #
  # ���ߥޥ͡�����˥��ɤ���Ƥ���⥸�塼��Υꥹ�Ȥ�������롣
  #
  # @param self
  #
  # @return ���ɺѤߥ⥸�塼��ꥹ��
  #
  # @else
  # @brief Get loaded module names
  # @endif
  #  std::vector<coil::Properties> getLoadedModules();
  def getLoadedModules(self):
    self._rtcout.RTC_TRACE("Manager.getLoadedModules()")
    return self._module.getLoadedModules()


  ##
  # @if jp
  # @brief ���ɲ�ǽ�ʥ⥸�塼��ꥹ�Ȥ��������
  #
  # ���ɲ�ǽ�⥸�塼��Υꥹ�Ȥ�������롣
  # (���ߤ�ModuleManager¦��̤����)
  #
  # @param self
  #
  # @return ���ɲ�ǽ�⥸�塼�롡�ꥹ��
  #
  # @else
  # @brief Get loadable module names
  # @endif
  def getLoadableModules(self):
    self._rtcout.RTC_TRACE("Manager.getLoadableModules()")
    return self._module.getLoadableModules()


  #============================================================
  # Component Factory Management
  #============================================================

  ##
  # @if jp
  # @brief RT����ݡ��ͥ���ѥե����ȥ����Ͽ����
  #
  # RT����ݡ��ͥ�ȤΥ��󥹥��󥹤��������뤿���
  # Factory����Ͽ���롣
  #
  # @param self
  # @param profile RT����ݡ��ͥ�� �ץ�ե�����
  # @param new_func RT����ݡ��ͥ�������Ѵؿ�
  # @param delete_func RT����ݡ��ͥ���˴��Ѵؿ�
  #
  # @return ��Ͽ�������(��Ͽ����:true������:false)
  #
  # @else
  # @brief Register RT-Component Factory
  # @endif
  def registerFactory(self, profile, new_func, delete_func):
    self._rtcout.RTC_TRACE("Manager.registerFactory(%s)", profile.getProperty("type_name"))
    try:
      factory = OpenRTM_aist.FactoryPython(profile, new_func, delete_func)
      self._factory.registerObject(factory)
      return True
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      return False

    return


  ##
  # @if jp
  # @brief �ե����ȥ�Υץ�ե���������
  #
  # �ե����ȥ�Υץ�ե������������롣
  #
  # @return �ե����ȥ�Υץ�ե�����
  #
  # @else
  # @brief Get profiles of factories. 
  #
  # Get profiles of factories. 
  #
  # @return profiles of factories
  #
  # @endif
  #
  def getFactoryProfiles(self):
    factories = self._factory.getObjects()

    if not factories:
      return []
      
    props = []
    for factory in factories:
      props.append(factory.profile())

    return props


  ##
  # @if jp
  # @brief ExecutionContext�ѥե����ȥ����Ͽ����
  #
  # ExecutionContext�Υ��󥹥��󥹤��������뤿���Factory����Ͽ���롣
  #
  # @param self
  # @param name �����о�ExecutionContext̾��
  # @param new_func ExecutionContext�����Ѵؿ�
  # @param delete_func ExecutionContext�˴��Ѵؿ�
  #
  # @return ��Ͽ�������(��Ͽ����:true������:false)
  #
  # @else
  # @brief Register ExecutionContext Factory
  # @endif
  def registerECFactory(self, name, new_func, delete_func):
    self._rtcout.RTC_TRACE("Manager.registerECFactory(%s)", name)
    try:
      self._ecfactory.registerObject(OpenRTM_aist.ECFactoryPython(name, new_func, delete_func))
      return True
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      return False

    return False


  ##
  # @if jp
  # @brief �ե����ȥ����ꥹ�Ȥ��������
  #
  # ��Ͽ����Ƥ���ե����ȥ�����ꥹ�Ȥ�������롣
  #
  # @param self
  #
  # @return ��Ͽ�ե����ȥ� �ꥹ��
  #
  # @else
  # @brief Get the list of all RT-Component Factory
  # @endif
  def getModulesFactories(self):
    self._rtcout.RTC_TRACE("Manager.getModulesFactories()")

    self._modlist = []
    for _obj in self._factory._objects._obj:
      self._modlist.append(_obj.profile().getProperty("implementation_id"))
    return self._modlist


  #============================================================
  # Component management
  #============================================================

  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ���������
  #
  # ���ꤷ��RT����ݡ��ͥ�ȤΥ��󥹥��󥹤���Ͽ���줿Factory��ͳ
  # ���������롣
  #
  # ��������륳��ݡ��ͥ�ȤγƼ�ץ�ե�����ϰʲ���ͥ���̤�
  # ���ꤵ��롣
  #
  # -# createComponent() �ΰ�����Ϳ����줿�ץ�ե�����
  # -# rtc.conf�ǻ��ꤵ�줿�����ե������Ϳ����줿�ץ�ե�����
  # --# category.instance_name.config_file
  # --# category.component_type.config_file
  # -# �����ɤ������ޤ줿�ץ�ե����� 
  #
  # ���󥹥�������������������硢ʻ���ưʲ��ν�����¹Ԥ��롣
  #  - �����ե���������ꤷ������ե�����졼����������ɤ߹��ߡ�����
  #  - ExecutionContext�ΥХ���ɡ�ư���
  #  - �͡��ߥ󥰥����ӥ��ؤ���Ͽ
  #
  # @param comp_args �����о�RT����ݡ��ͥ��ID����ӥ���ե�����졼
  # �����������ե����ޥåȤ��礭��ʬ���� "id" �� "configuration" 
  # ��ʬ��¸�ߤ��롣
  #
  # comp_args:     [id]?[configuration]
  #                id ��ɬ�ܡ�configuration�ϥ��ץ����
  # id:            RTC:[vendor]:[category]:[implementation_id]:[version]
  #                RTC �ϸ��꤫��ɬ��
  #                vendor, category, version �ϥ��ץ����
  #                implementation_id ��ɬ��
  #                ���ץ������ά������Ǥ� ":" �Ͼ�ά�Բ�
  # configuration: [key0]=[value0]&[key1]=[value1]&[key2]=[value2].....
  #                RTC������Properties���ͤ򤹤٤ƾ�񤭤��뤳�Ȥ��Ǥ��롣
  #                key=value �η����ǵ��Ҥ���"&" �Ƕ��ڤ�
  #
  # �㤨�С�
  # RTC:jp.go.aist:example:ConfigSample:1.0?conf.default.str_param0=munya
  # RTC::example:ConfigSample:?conf.default.int_param0=100
  #
  # @return ��������RT����ݡ��ͥ�ȤΥ��󥹥���
  #
  # @else
  # @brief Create RT-Components
  #
  # Create specified RT-Component's instances via registered Factory.
  # When its instances have been created successfully, the following
  # processings are also executed.
  #  - Read and set configuration information that was set by external file.
  #  - Bind ExecutionContext and start operation.
  #  - Register to naming service.
  #
  # @param module_name Target RT-Component names for the creation
  #
  # @return Created RT-Component's instances
  #
  # @endif
  #
  def createComponent(self, comp_args):
    self._rtcout.RTC_TRACE("Manager.createComponent(%s)", comp_args)
    comp_prop = OpenRTM_aist.Properties()
    comp_id   = OpenRTM_aist.Properties()

    print "comp_args:", comp_args
    if not self.procComponentArgs(comp_args, comp_id, comp_prop):
      return None

    if comp_prop.findNode("exported_ports"):
      exported_ports = OpenRTM_aist.split(comp_prop.getProperty("exported_ports"),
                                          ",")
      exported_ports_str = ""
      for i in range(len(exported_ports)):
        keyval = OpenRTM_aist.split(exported_ports[i], ".")
        if len(keyval) > 2:
          exported_ports_str += (keyval[0] + "." + keyval[-1])
        else:
          exported_ports_str += exported_ports[i]

        if i != (len(exported_ports) - 1) :
          exported_ports_str += ","

      comp_prop.setProperty("exported_ports", exported_ports_str)
      comp_prop.setProperty("conf.default.exported_ports", exported_ports_str)

    factory = self._factory.find(comp_id)
    if factory is None:
      self._rtcout.RTC_ERROR("createComponent: Factory not found: %s",
                             comp_id.getProperty("implementation_id"))

      # automatic module loading
      mp = self._module.getLoadableModules()
      self._rtcout.RTC_INFO("%d loadable modules found", len(mp))

      found_obj = None
      predicate = self.ModulePredicate(comp_id)
      for _obj in mp:
        if predicate(_obj):
          found_obj = _obj
          break

      if not found_obj:
        self._rtcout.RTC_ERROR("No module for %s in loadable modules list",
                               comp_id.getProperty("implementation_id"))
        return None

      if not found_obj.findNode("module_file_name"):
        self._rtcout.RTC_ERROR("Hmm...module_file_name key not found.")
        return 0

      # module loading
      self._rtcout.RTC_INFO("Loading module: %s", found_obj.getProperty("module_file_name"))
      self.load(found_obj.getProperty("module_file_name"), "")
      factory = self._factory.find(comp_id)
      if not factory:
        self._rtcout.RTC_ERROR("Factory not found for loaded module: %s",
                               comp_id.getProperty("implementation_id"))
        return 0


    # get default configuration of component.
    prop = factory.profile()

    inherit_prop = ["config.version",
                    "openrtm.name",
                    "openrtm.version",
                    "os.name",
                    "os.release",
                    "os.version",
                    "os.arch",
                    "os.hostname",
                    "corba.endpoint",
                    "corba.id",
                    "exec_cxt.periodic.type",
                    "exec_cxt.periodic.rate",
                    "exec_cxt.evdriven.type",
                    "logger.enable",
                    "logger.log_level",
                    "naming.enable",
                    "naming.type",
                    "naming.formats"]

    for i in range(len(inherit_prop)):
      prop.setProperty(inherit_prop[i],self._config.getProperty(inherit_prop[i]))

    comp = factory.create(self)

    if comp is None:
      self._rtcout.RTC_ERROR("createComponent: RTC creation failed: %s",
                             comp_id.getProperty("implementation_id"))
      return None
    self._rtcout.RTC_TRACE("RTC Created: %s", comp_id.getProperty("implementation_id"))

    # The property specified by the parameter of createComponent() is merged.
    # The property("instance_name") specified by the parameter of createComponent()
    # must be merged here.
    prop.mergeProperties(comp_prop)

    #------------------------------------------------------------
    # Load configuration file specified in "rtc.conf"
    #
    # rtc.conf:
    #   [category].[type_name].config_file = file_name
    #   [category].[instance_name].config_file = file_name
    self.configureComponent(comp,prop)

    # The property specified by the parameter of createComponent() is set.
    # The property("exported_ports") specified by the parameter of createComponent()
    # must be set here.
    #comp.setProperties(comp_prop)

    # Component initialization
    if comp.initialize() != RTC.RTC_OK:
      self._rtcout.RTC_TRACE("RTC initialization failed: %s",
                             comp_id.getProperty("implementation_id"))
      comp.exit()
      self._rtcout.RTC_TRACE("%s was finalized", comp_id.getProperty("implementation_id"))
      return None
      
    self._rtcout.RTC_TRACE("RTC initialization succeeded: %s",
                           comp_id.getProperty("implementation_id"))
    self.registerComponent(comp)
    return comp



  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ�ľ�� Manager ����Ͽ����
  #
  # ���ꤷ��RT����ݡ��ͥ�ȤΥ��󥹥��󥹤�ե����ȥ��ͳ�ǤϤʤ�
  # ľ�ܥޥ͡��������Ͽ���롣
  #
  # @param self
  # @param comp ��Ͽ�о�RT����ݡ��ͥ�ȤΥ��󥹥���
  #
  # @return ��Ͽ�������(��Ͽ����:true������:false)
  #
  # @else
  # @brief Register RT-Component directly without Factory
  # @endif
  def registerComponent(self, comp):
    self._rtcout.RTC_TRACE("Manager.registerComponent(%s)", comp.getInstanceName())

    self._compManager.registerObject(comp)
    names = comp.getNamingNames()

    for name in names:
      self._rtcout.RTC_TRACE("Bind name: %s", name)
      self._namingManager.bindObject(name, comp)

    return True

  
  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ���Ͽ��������
  #
  # ���ꤷ��RT����ݡ��ͥ�Ȥ���Ͽ�������롣
  #
  # @param self
  # @param comp ��Ͽ����о�RT����ݡ��ͥ�ȤΥ��󥹥���
  #
  # @return ��Ͽ����������(�������:true���������:false)
  #
  # @else
  # @brief Register RT-Component directly without Factory
  # @endif
  def unregisterComponent(self, comp):
    self._rtcout.RTC_TRACE("Manager.unregisterComponent(%s)", comp.getInstanceName())
    self._compManager.unregisterObject(comp.getInstanceName())
    names = comp.getNamingNames()
    
    for name in names:
      self._rtcout.RTC_TRACE("Unbind name: %s", name)
      self._namingManager.unbindObject(name)

    return True


  ##
  # @if jp
  # @brief Context����������
  #
  # @return ��������Conetext�Υ��󥹥���
  #
  # @else
  # @brief Create Context
  #
  # @return Created Context's instances
  #
  # @endif
  #
  # ExecutionContextBase* createContext(const char* ec_args);
  def createContext(self, ec_args):
    self._rtcout.RTC_TRACE("Manager.createContext()")
    self._rtcout.RTC_TRACE("ExecutionContext type: %s",
                           self._config.getProperty("exec_cxt.periodic.type"))
    ec_id = [""]
    ec_prop = OpenRTM_aist.Properties()

    if not self.procContextArgs(ec_args, ec_id, ec_prop):
      return None

    factory = self._ecfactory.find(ec_id[0])

    if factory == None:
      self._rtcout.RTC_ERROR("Factory not found: %s", ec_id[0])
      return None

    ec = factory.create()
    return ec
    

  ##
  # @if jp
  # @brief Manager ����Ͽ����Ƥ���RT����ݡ��ͥ�Ȥ�������(̤����)
  #
  # �ޥ͡��������Ͽ����Ƥ���RT����ݡ��ͥ�Ȥ������롣
  #
  # @param self
  # @param instance_name ����о�RT����ݡ��ͥ�ȤΥ��󥹥���̾
  #
  # @else
  # @brief Unregister RT-Component that is registered in the Manager
  # @endif
  def deleteComponent(self, instance_name=None, comp=None):
    if instance_name:
      self._rtcout.RTC_TRACE("Manager.deleteComponent(%s)", instance_name)
      _comp = self._compManager.find(instance_name)
      if _comp is None:
        self._rtcout.RTC_WARN("RTC %s was not found in manager.", instance_name)
        return
      self.deleteComponent(comp=_comp)

    elif comp:
      self._rtcout.RTC_TRACE("Manager.deleteComponent(RTObject_impl)")
      # cleanup from manager's table, and naming serivce
      self.unregisterComponent(comp)
      
      comp_id = comp.getProperties()
      factory = self._factory.find(comp_id)

      if not factory:
        self._rtcout.RTC_DEBUG("Factory not found: %s",
                               comp_id.getProperty("implementation_id"))
        return
      else:
        self._rtcout.RTC_DEBUG("Factory found: %s",
                               comp_id.getProperty("implementation_id"))
        factory.destroy(comp)
        

      if OpenRTM_aist.toBool(self._config.getProperty("manager.shutdown_on_nortcs"),
                             "YES","NO",True) and \
                             not OpenRTM_aist.toBool(self._config.getProperty("manager.is_master"),
                                                     "YES","NO",False):
        comps = self.getComponents()
        if len(comps) == 0:
          self.shutdown()

    return


  ##
  # @if jp
  # @brief Manager ����Ͽ����Ƥ���RT����ݡ��ͥ�Ȥ򸡺�����
  #
  # Manager ����Ͽ����Ƥ���RT����ݡ��ͥ�Ȥ���ꤷ��̾�ΤǸ�������
  # ���פ��륳��ݡ��ͥ�Ȥ�������롣
  #
  # @param self
  # @param instance_name �����о�RT����ݡ��ͥ�Ȥ�̾��
  #
  # @return ̾�Τ����פ���RT����ݡ��ͥ�ȤΥ��󥹥���
  #
  # @else
  # @brief Get RT-Component's pointer
  # @endif
  def getComponent(self, instance_name):
    self._rtcout.RTC_TRACE("Manager.getComponent(%s)", instance_name)
    return self._compManager.find(instance_name)


  ##
  # @if jp
  # @brief Manager ����Ͽ����Ƥ�����RT����ݡ��ͥ�Ȥ��������
  #
  # Manager ����Ͽ����Ƥ���RT����ݡ��ͥ�Ȥ������󥹥��󥹤�������롣
  #
  # @param self
  #
  # @return ��RT����ݡ��ͥ�ȤΥ��󥹥��󥹥ꥹ��
  #
  # @else
  # @brief Get all RT-Component's pointer
  # @endif
  def getComponents(self):
    self._rtcout.RTC_TRACE("Manager.getComponents()")
    return self._compManager.getObjects()


  #============================================================
  # CORBA ��Ϣ
  #============================================================

  ##
  # @if jp
  # @brief ORB �Υݥ��󥿤��������
  #
  # Manager �����ꤵ�줿 ORB �Υݥ��󥿤�������롣
  #
  # @param self
  #
  # @return ORB ���֥�������
  #
  # @else
  # @brief Get the pointer to the ORB
  # @endif
  def getORB(self):
    self._rtcout.RTC_TRACE("Manager.getORB()")
    return self._orb


  ##
  # @if jp
  # @brief Manager ������ RootPOA �Υݥ��󥿤��������
  #
  # Manager �����ꤵ�줿 RootPOA �ؤΥݥ��󥿤�������롣
  #
  # @param self
  #
  # @return RootPOA���֥�������
  #
  # @else
  # @brief Get the pointer to the RootPOA 
  # @endif
  def getPOA(self):
    self._rtcout.RTC_TRACE("Manager.getPOA()")
    return self._poa


  ##
  # @if jp
  # @brief Manager ������ POAManager ���������
  #
  # Manager �����ꤵ�줿 POAMAnager ��������롣
  #
  # @param self
  #
  # @return POA�ޥ͡�����
  #
  # @else
  #
  # @endif
  def getPOAManager(self):
    self._rtcout.RTC_TRACE("Manager.getPOAManager()")
    return self._poaManager



  #============================================================
  # Manager initialize and finalization
  #============================================================

  ##
  # @if jp
  # @brief Manager ���������������
  # 
  # Manager �����������������¹Ԥ��롣
  #  - Manager ����ե�����졼����������
  #  - �����ϥե����������
  #  - ��λ�����ѥ���åɤ�����
  #  - �������ѥ���åɤ�����(�����޻��ѻ�)
  #
  # @param self
  # @param argv ���ޥ�ɥ饤�����
  # 
  # @else
  # @brief Manager internal initialization
  # @endif
  def initManager(self, argv):
    config = OpenRTM_aist.ManagerConfig(argv)
    self._config = OpenRTM_aist.Properties()
    config.configure(self._config)
    self._config.setProperty("logger.file_name",self.formatString(self._config.getProperty("logger.file_name"), 
                                                                  self._config))
    self._module = OpenRTM_aist.ModuleManager(self._config)
    self._terminator = self.Terminator(self)
    guard = OpenRTM_aist.ScopedLock(self._terminate.mutex)
    self._terminate.waiting = 0
    del guard

    if OpenRTM_aist.toBool(self._config.getProperty("timer.enable"), "YES", "NO", True):
      tm = OpenRTM_aist.TimeValue(0, 100000)
      tick = self._config.getProperty("timer.tick")
      if tick != "":
        tm = tm.set_time(float(tick))
        if self._timer:
          self._timer.stop()
          self._timer.join()
        self._timer = OpenRTM_aist.Timer(tm)
        self._timer.start()

    if OpenRTM_aist.toBool(self._config.getProperty("manager.shutdown_auto"),
                           "YES", "NO", True) and \
                           not OpenRTM_aist.toBool(self._config.getProperty("manager.is_master"),
                                                   "YES", "NO", False):
      tm = OpenRTM_aist.TimeValue(10, 0)
      if self._config.findNode("manager.auto_shutdown_duration"):
        duration = float(self._config.getProperty("manager.auto_shutdown_duration"))
        if duration:
          tm.set_time(duration)

      if self._timer:
        self._timer.registerListenerObj(self,
                                        OpenRTM_aist.Manager.shutdownOnNoRtcs,
                                        tm)
    
    if self._timer:
      tm = OpenRTM_aist.TimeValue(1, 0)
      self._timer.registerListenerObj(self,
                                      OpenRTM_aist.Manager.cleanupComponents,
                                      tm)

    return


  ##
  # @if jp
  # @brief Manager �ν�λ����(̤����)
  #
  # Manager ��λ����
  # (�����������ߤ�̤����)
  #
  # @param self
  #
  # @else
  #
  # @endif
  def shutdownManager(self):
    self._rtcout.RTC_TRACE("Manager.shutdownManager()")
    if self._timer:
      self._timer.stop()
      self._timer.join()
      self._timer = None

    return


  ##
  # @if jp
  # @brief Manager �ν�λ����
  #
  # configuration �� "manager.shutdown_on_nortcs" YES �ǡ�
  # ����ݡ��ͥ�Ȥ���Ͽ����Ƥ��ʤ���� Manager ��λ���롣
  #
  # @else
  # @brief Shutdown Manager
  #
  # This method shutdowns Manager as follows.
  # - "Manager.shutdown_on_nortcs" of configuration is YES. 
  # - The component is not registered. 
  #
  # @endif
  #
  # void shutdownOnNoRtcs();
  def shutdownOnNoRtcs(self):
    self._rtcout.RTC_TRACE("Manager::shutdownOnNoRtcs()")
    if OpenRTM_aist.toBool(self._config.getProperty("manager.shutdown_on_nortcs"),
                           "YES", "NO", True):

      comps = self.getComponents()
      
      if len(comps) == 0:
        self.shutdown()

    return


  #============================================================
  # Logger initialize and terminator
  #============================================================

  ##
  # @if jp
  # @brief System logger �ν����
  #
  # System logger �ν������¹Ԥ��롣
  # ����ե�����졼�����ե���������ꤵ�줿����˴�Ť���
  # �����ν�����������¹Ԥ��롣
  #
  # @param self
  #
  # @return ������¹Է��(���������:true�����������:false)
  #
  # @else
  # @brief System logger initialization
  # @endif
  def initLogger(self):

    if not OpenRTM_aist.toBool(self._config.getProperty("logger.enable"), "YES", "NO", True):
      self._rtcout = OpenRTM_aist.LogStream()
      return True

    logfile = "./rtc.log"

    logouts = self._config.getProperty("logger.file_name")
    logouts = [s.strip() for s in logouts.split(",")]
    
    self._rtcout = None

    for i in range(len(logouts)):
      tmp = [logouts[i]]
      OpenRTM_aist.eraseHeadBlank(tmp)
      OpenRTM_aist.eraseTailBlank(tmp)
      logouts[i] = tmp[0]
      if logouts[i].lower() == "stdout":
        if self._rtcout is None:
          self._rtcout = OpenRTM_aist.LogStream("manager","STDOUT")
        else:
          self._rtcout.addHandler(logouts[i])
      else:
        if logouts[i] == "":
          logfile = "./rtc.log"
        else:
          logfile = logouts[i]
          
        if self._rtcout is None:
          self._rtcout = OpenRTM_aist.LogStream("manager","FILE", logfile)
        else:
          self._rtcout.addHandler("FILE",logfile)

    self._rtcout.setLogLevel(self._config.getProperty("logger.log_level"))
    self._rtcout.setLogLock(OpenRTM_aist.toBool(self._config.getProperty("logger.stream_lock"),
                                                "enable", "disable", False))

    self._rtcout.RTC_INFO("%s", self._config.getProperty("openrtm.version"))
    self._rtcout.RTC_INFO("Copyright (C) 2003-2010")
    self._rtcout.RTC_INFO("  Noriaki Ando")
    self._rtcout.RTC_INFO("  Intelligent Systems Research Institute, AIST")
    self._rtcout.RTC_INFO("Manager starting.")
    self._rtcout.RTC_INFO("Starting local logging.")

    return True


  ##
  # @if jp
  # @brief System Logger �ν�λ����(̤����)
  #
  # System Logger�ν�λ������¹Ԥ��롣
  # (���ߤ�̤����)
  #
  # @param self
  #
  # @else
  # @brief System Logger finalization
  # @endif
  def shutdownLogger(self):
    self._rtcout.RTC_TRACE("Manager.shutdownLogger()")
    self._rtcout.shutdown()
    return


  #============================================================
  # ORB initialization and finalization
  #============================================================

  ##
  # @if jp
  # @brief CORBA ORB �ν��������
  #
  # �������򸵤�ORB���������롣
  #
  # @param self
  #
  # @return ORB ������������(���������:true�����������:false)
  #
  # @else
  # @brief CORBA ORB initialization
  # @endif
  def initORB(self):
    self._rtcout.RTC_TRACE("Manager.initORB()")
    try:
      args = OpenRTM_aist.split(self.createORBOptions(), " ")
      args.insert(0,"manager")
      argv = OpenRTM_aist.toArgv(args)
      self._orb = CORBA.ORB_init(argv)

      self._poa = self._orb.resolve_initial_references("RootPOA")
      if CORBA.is_nil(self._poa):
        self._rtcout.RTC_ERROR("Could not resolve RootPOA")
        return False

      self._poaManager = self._poa._get_the_POAManager()

    except:
      self._rtcout.RTC_ERROR("Exception: Caught unknown exception in initORB().")
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      return False

    return True


  ##
  # @if jp
  # @brief ORB �Υ��ޥ�ɥ饤�󥪥ץ�������
  #
  # ����ե�����졼������������ꤵ�줿���Ƥ���
  # ORB �ε�ư�����ץ�����������롣
  #
  # @param self
  #
  # @return ORB ��ư�����ץ����
  #
  # @else
  # @brief ORB command option creation
  # @endif
  def createORBOptions(self):
    opt      = self._config.getProperty("corba.args")
    self._rtcout.RTC_DEBUG("corba.args: %s",opt)

    endpoints = []
    self.createORBEndpoints(endpoints)
    opt = [opt]
    self.createORBEndpointOption(opt,endpoints)

    self._rtcout.RTC_PARANOID("ORB options: %s", opt[0])

    return opt[0]


  ##
  # @if jp
  # @brief ����ɥݥ���Ȥ�����
  #
  # ����ե����졼����󤫤饨��ɥݥ���Ȥ��������롣
  #
  # @param endpoints ����ɥݥ���ȥꥹ��
  #
  # @else
  # @brief Create Endpoints
  #
  # Create Endpoints from the configuration.
  # 
  # @param endpoints Endpoints list
  #
  # @endif
  #
  # void createORBEndpoints(coil::vstring& endpoints);
  def createORBEndpoints(self, endpoints):

    # corba.endpoint is obsolete
    # corba.endpoints with comma separated values are acceptable
    if self._config.findNode("corba.endpoints"):
      endpoints_ = [s.strip() for s in self._config.getProperty("corba.endpoints").split(",")]
      for ep in endpoints_:
        endpoints.append(ep)

      self._rtcout.RTC_DEBUG("corba.endpoints: %s", self._config.getProperty("corba.endpoints"))

    if self._config.findNode("corba.endpoint"):
      endpoints_ = [s.strip() for s in self._config.getProperty("corba.endpoint").split(",")]
      for ep in endpoints_:
        endpoints.append(ep)
      self._rtcout.RTC_DEBUG("corba.endpoint: %s", self._config.getProperty("corba.endpoint"))

    # If this process has master manager,
    # master manager's endpoint inserted at the top of endpoints
    self._rtcout.RTC_DEBUG("manager.is_master: %s",
                           self._config.getProperty("manager.is_master"))

    if OpenRTM_aist.toBool(self._config.getProperty("manager.is_master"), "YES", "NO", False):
      mm = self._config.getProperty("corba.master_manager", ":2810")
      mmm = [s.strip() for s in mm.split(":")]
      if len(mmm) == 2:
        endpoints.insert(0, ":" + mmm[1])
      else:
        endpoints.insert(0, ":2810")

    endpoints = OpenRTM_aist.unique_sv(endpoints)
    
    return

    
  ##
  # @if jp
  # @brief ORB �� Endpoint �Υ��ޥ�ɥ饤�󥪥ץ�������
  # @param opt ���ޥ�ɥ饤�󥪥ץ����
  # @param endpoints ����ɥݥ���ȥꥹ��
  #
  # @else
  # @brief Create a command optional line of Endpoint of ORB.
  # @param opt ORB options
  # @param endpoints Endpoints list
  #
  # @endif
  # void createORBEndpointOption(std::string& opt, coil::vstring& endpoints);
  def createORBEndpointOption(self, opt, endpoints):
    corba = self._config.getProperty("corba.id")
    self._rtcout.RTC_DEBUG("corba.id: %s", corba)

    for i in range(len(endpoints)):
      if endpoints[i]:
        endpoint = endpoints[i]
      else:
        continue

      self._rtcout.RTC_DEBUG("Endpoint is : %s", endpoint)
      if endpoint.find(":") == -1:
        endpoint += ":"

      if corba == "omniORB":
        endpoint = OpenRTM_aist.normalize([endpoint])
        if OpenRTM_aist.normalize([endpoint]) == "all:":
          opt[0] += " -ORBendPointPublishAllIFs 1"
        else:
          opt[0] += " -ORBendPoint giop:tcp:" + endpoint

      elif corba == "TAO":
        opt[0] += "-ORBEndPoint iiop://" + endpoint
      elif corba == "MICO":
        opt[0] += "-ORBIIOPAddr inet:" + endpoint

      endpoints[i] = endpoint

    return


  ##
  # @if jp
  # @brief ORB �ν�λ����
  #
  # ORB �ν�λ������¹Ԥ��롣
  # �¹��Ԥ��ν�����¸�ߤ�����ˤϡ����ν�������λ����ޤ��Ԥġ�
  # �ºݤν�λ�����Ǥϡ�POA Manager������������� ORB �Υ���åȥ������¹�
  # ���롣
  #
  # @param self
  #
  # @else
  # @brief ORB finalization
  # @endif
  def shutdownORB(self):
    self._rtcout.RTC_TRACE("Manager.shutdownORB()")
    if not self._orb:
      return

    try:
      while self._orb.work_pending():
        self._rtcout.RTC_PARANOID("Pending work still exists.")
        if self._orb.work_pending():
            self._orb.perform_work()
            pass

      self._rtcout.RTC_DEBUG("No pending works of ORB. Shutting down POA and ORB.")
    except:
      self._rtcout.RTC_TRACE(OpenRTM_aist.Logger.print_exception())
      pass

    if not CORBA.is_nil(self._poa):
      try:
        if not CORBA.is_nil(self._poaManager):
          self._poaManager.deactivate(False, True)
        self._rtcout.RTC_DEBUG("POA Manager was deactivated.")
        self._poa.destroy(False, True)
        self._poa = PortableServer.POA._nil
        self._rtcout.RTC_DEBUG("POA was destroyed.")
      except CORBA.SystemException, ex:
        self._rtcout.RTC_ERROR("Caught SystemException during root POA destruction")
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      except:
        self._rtcout.RTC_ERROR("Caught unknown exception during destruction")
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if self._orb:
      try:
        self._orb.shutdown(True)
        self._rtcout.RTC_DEBUG("ORB was shutdown.")
        self._orb = CORBA.Object._nil
      except CORBA.SystemException, ex:
        self._rtcout.RTC_ERROR("Caught CORBA::SystemException during ORB shutdown.")
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      except:
        self._rtcout.RTC_ERROR("Caught unknown exception during ORB shutdown.")
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())


  #============================================================
  # NamingService initialization and finalization
  #============================================================

  ##
  # @if jp
  # @brief NamingManager �ν����
  #
  # NamingManager �ν����������¹Ԥ��롣
  # �������� NamingManager ����Ѥ��ʤ��褦�˥ץ�ѥƥ���������ꤵ��Ƥ���
  # ���ˤϲ��⤷�ʤ���
  # NamingManager ����Ѥ����硢�ץ�ѥƥ���������ꤵ��Ƥ���
  # �ǥե���� NamingServer ����Ͽ���롣
  # �ޤ������Ū�˾���򹹿�����褦�����ꤵ��Ƥ�����ˤϡ����ꤵ�줿����
  # �Ǽ�ư������Ԥ�����Υ����ޤ�ư����ȤȤ�ˡ������ѥ᥽�åɤ򥿥��ޤ�
  # ��Ͽ���롣
  #
  # @param self
  #
  # @return ������������(���������:true�����������:false)
  #
  # @else
  #
  # @endif
  def initNaming(self):
    self._rtcout.RTC_TRACE("Manager.initNaming()")
    self._namingManager = OpenRTM_aist.NamingManager(self)

    if not OpenRTM_aist.toBool(self._config.getProperty("naming.enable"), "YES", "NO", True):
      return True

    meths = OpenRTM_aist.split(self._config.getProperty("naming.type"),",")
    
    for meth in meths:
      names = OpenRTM_aist.split(self._config.getProperty(meth+".nameservers"), ",")
      for name in names:
        self._rtcout.RTC_TRACE("Register Naming Server: %s/%s", (meth, name))
        self._namingManager.registerNameServer(meth,name)

    if OpenRTM_aist.toBool(self._config.getProperty("naming.update.enable"), "YES", "NO", True):
      tm = OpenRTM_aist.TimeValue(10,0)
      intr = self._config.getProperty("naming.update.interval")
      if intr != "":
        tm = OpenRTM_aist.TimeValue(intr)

      if self._timer:
        self._timer.registerListenerObj(self._namingManager,OpenRTM_aist.NamingManager.update,tm)
  
    return True


  ##
  # @if jp
  # @brief NamingManager �ν�λ����
  #
  # NamingManager ��λ���롣
  # ��Ͽ����Ƥ��������Ǥ򥢥�Х���ɤ�����λ���롣
  #
  # @param self
  #
  # @else
  #
  # @endif
  def shutdownNaming(self):
    self._rtcout.RTC_TRACE("Manager.shutdownNaming()")
    self._namingManager.unbindAll()


  ##
  # @if jp
  # @brief ExecutionContextManager �ν����
  #
  # ���Ѥ���� ExecutionContext �ν����������¹Ԥ����� ExecutionContext 
  # ������ Factory �� ExecutionContextManager ����Ͽ���롣
  #
  # @param self
  #
  # @return ExecutionContextManager ����������¹Է��
  #         (���������:true�����������:false)
  #
  # @else
  #
  # @endif
  def initExecContext(self):
    self._rtcout.RTC_TRACE("Manager.initExecContext()")
    OpenRTM_aist.PeriodicExecutionContextInit(self)
    OpenRTM_aist.ExtTrigExecutionContextInit(self)
    OpenRTM_aist.OpenHRPExecutionContextInit(self)
    return True


  ##
  # @if jp
  # @brief PeriodicECSharedComposite �ν����
  #
  # @return PeriodicECSharedComposite ����������¹Է��
  #         (���������:true�����������:false)
  #
  # @else
  # @brief PeriodicECSharedComposite initialization
  #
  # @return PeriodicECSharedComposite initialization result
  #          (Successful:true, Failed:false)
  #
  # @endif
  #
  def initComposite(self):
    self._rtcout.RTC_TRACE("Manager.initComposite()")
    OpenRTM_aist.PeriodicECSharedCompositeInit(self)
    return True

  
  ##
  # @if jp
  # @brief �ե����ȥ�ν����
  #
  # �Хåե�������åɡ��ѥ֥�å��㡢�ץ�Х��������󥷥塼�ޤ�
  # �ե����ȥ���������롣
  #
  # @return �ե����ȥ����������¹Է��
  #         (���������:true�����������:false)
  #
  # @else
  # @brief Factories initialization
  #
  # Initialize buffer factories, thread factories, publisher factories, 
  # provider factories, and consumer factories. 
  #
  # @return PeriodicECSharedComposite initialization result
  #          (Successful:true, Failed:false)
  #
  # @endif
  #
  def initFactories(self):
    self._rtcout.RTC_TRACE("Manager.initFactories()")
    OpenRTM_aist.FactoryInit()
    return True

  
  ##
  # @if jp
  # @brief Timer �ν����
  #
  # ���Ѥ���� Timer �ν����������¹Ԥ��롣
  # (�����μ����Ǥϲ��⤷�ʤ�)
  #
  # @param self
  #
  # @return Timer ����������¹Է��(���������:true�����������:false)
  #
  # @else
  #
  # @endif
  def initTimer(self):
    return True


  ##
  # @if jp
  # @brief ManagerServant �ν����
  #
  # @return Timer ����������¹Է��(���������:true�����������:false)
  #
  # @else
  # @brief ManagerServant initialization
  #
  # @return Timer Initialization result (Successful:true, Failed:false)
  #
  # @endif
  #
  def initManagerServant(self):
    self._rtcout.RTC_TRACE("Manager.initManagerServant()")
    if not OpenRTM_aist.toBool(self._config.getProperty("manager.corba_servant"),
                               "YES","NO",True):
      return True

    self._mgrservant = OpenRTM_aist.ManagerServant()
    prop = self._config.getNode("manager")
    names = OpenRTM_aist.split(prop.getProperty("naming_formats"),",")

    if OpenRTM_aist.toBool(prop.getProperty("is_master"),
                           "YES","NO",True):
      for name in names:
        mgr_name = self.formatString(name, prop)
        self._namingManager.bindManagerObject(mgr_name, self._mgrservant)

    otherref = None

    try:
      otherref = file(self._config.getProperty("manager.refstring_path"),'r')
      refstring = otherref.readline()
      otherref.close()
    except:
      try:
        reffile = file(self._config.getProperty("manager.refstring_path"),'w')
      except:
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
        return False
      else:
        reffile.write(self._orb.object_to_string(self._mgrservant.getObjRef()))
        reffile.close()
    return True

  
  ##
  # @if jp
  # @brief NamingManager ����Ͽ����Ƥ���������ݡ��ͥ�Ȥν�λ����
  #
  # NamingManager ����Ͽ����Ƥ���RT����ݡ��ͥ�Ȥ���� ExecutionContext ��
  # �ꥹ�Ȥ��������������ݡ��ͥ�Ȥ�λ���롣
  #
  # @param self
  #
  # @else
  #
  # @endif
  def shutdownComponents(self):
    self._rtcout.RTC_TRACE("Manager.shutdownComponents()")
    comps = self._namingManager.getObjects()
    for comp in comps:
      try:
        comp.exit()
        p = OpenRTM_aist.Properties(key=comp.getInstanceName())
        p.mergeProperties(comp.getProperties())
      except:
        self._rtcout.RTC_TRACE(OpenRTM_aist.Logger.print_exception())
        pass

    for ec in self._ecs:
      try:
        self._poa.deactivate_object(self._poa.servant_to_id(ec))
      except:
        self._rtcout.RTC_TRACE(OpenRTM_aist.Logger.print_exception())
        pass


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ���Ͽ���
  #
  # ���ꤷ��RT����ݡ��ͥ�ȤΥ��󥹥��󥹤�͡��ߥ󥰥����ӥ�����
  # ��Ͽ������롣
  #
  # @param self
  # @param comp ��Ͽ����о�RT����ݡ��ͥ��
  #
  # @else
  #
  # @endif
  def cleanupComponent(self, comp):
    self._rtcout.RTC_TRACE("Manager.cleanupComponent()")
    self.unregisterComponent(comp)

    return


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥκ������
  #
  # notifyFinalized()�ˤ�ä���Ͽ���줿RT����ݡ��ͥ�Ȥ������롣
  #
  # @else
  # @brief This method deletes RT-Components. 
  #
  # This method deletes RT-Components registered by notifyFinalized(). 
  #
  # @endif
  #
  # void cleanupComponents();
  def cleanupComponents(self):
    self._rtcout.RTC_VERBOSE("Manager.cleanupComponents()")
    guard = OpenRTM_aist.ScopedLock(self._finalized.mutex)
    self._rtcout.RTC_VERBOSE("%d components are marked as finalized.",
                             len(self._finalized.comps))
    for _comp in self._finalized.comps:
      self.deleteComponent(comp=_comp)

    self._finalized.comps = []
    del guard
    return


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥκ������
  #
  # �������RT����ݡ��ͥ�Ȥ���Ͽ���롣
  # ��Ͽ���줿RT����ݡ��ͥ�Ȥ� cleanupComponents() �Ǻ������롣
  #
  # @param �������RT����ݡ��ͥ��
  #
  # @else
  # @brief This method deletes RT-Components. 
  #
  # The deleted RT-Component is registered. The registered RT-Components 
  # are deleted by cleanupComponents(). 
  #
  # @param Deleted RT component
  # @endif
  #
  # void notifyFinalized(RTObject_impl* comp);
  def notifyFinalized(self, comp):
    self._rtcout.RTC_TRACE("Manager.notifyFinalized()")
    guard = OpenRTM_aist.ScopedLock(self._finalized.mutex)
    self._finalized.comps.append(comp)
    del guard
    return


  ##
  # @if jp
  # @brief createComponent�ΰ������������
  # @ param self
  # @ param comp_arg(str)
  # @ param comp_id(Properties object)
  # @ param comp_conf(Properties object)
  # @ return True or False
  # @else
  #
  # @endif
  #
  # bool procComponentArgs(const char* comp_arg,
  #                        coil::Properties& comp_id,
  #                        coil::Properties& comp_conf)
  def procComponentArgs(self, comp_arg, comp_id, comp_conf):
    id_and_conf = [s.strip() for s in comp_arg.split("?")]
    if len(id_and_conf) != 1 and len(id_and_conf) != 2:
      self._rtcout.RTC_ERROR("Invalid arguments. Two or more '?'")
      return False

    if id_and_conf[0].find(":") == -1:
      id_and_conf[0] = "RTC:::" + id_and_conf[0] + ":"

    id = [s.strip() for s in id_and_conf[0].split(":")]

    if len(id) != 5:
      self._rtcout.RTC_ERROR("Invalid RTC id format.")
      return False

    prof = ["RTC", "vendor", "category", "implementation_id", "version"]

    if id[0] != prof[0]:
      self._rtcout.RTC_ERROR("Invalid id type.")
      return False

    for i in [1,2,3,4]:
      comp_id.setProperty(prof[i], id[i])
      self._rtcout.RTC_TRACE("RTC basic profile %s: %s", (prof[i], id[i]))

    if len(id_and_conf) == 2:
      conf = [s.strip() for s in id_and_conf[1].split("&")]
      for i in range(len(conf)):
        keyval = [s.strip() for s in conf[i].split("=")]
        if len(keyval) > 1:
          comp_conf.setProperty(keyval[0],keyval[1])
          self._rtcout.RTC_TRACE("RTC property %s: %s", (keyval[0], keyval[1]))

    return True


  # bool procContextArgs(const char* ec_args,
  #                      std::string& ec_id,
  #                      coil::Properties& ec_conf);
  def procContextArgs(self, ec_args, ec_id, ec_conf):
    id_and_conf = [s.strip() for s in ec_args.split("?")]

    if len(id_and_conf) != 1 and len(id_and_conf) != 2:
      self._rtcout.RTC_ERROR("Invalid arguments. Two or more '?'")
      return False

    if (id_and_conf[0] == "") or id_and_conf[0] is None:
      self._rtcout.RTC_ERROR("Empty ExecutionContext's name")
      return False

    ec_id[0] = id_and_conf[0]

    if len(id_and_conf) == 2:
      conf = [s.strip() for s in id_and_conf[1].split("&")]
      for i in range(len(conf)):
        k = [s.strip() for s in conf[i].split("=")]
        ec_conf.setProperty(k[0],k[1])
        self._rtcout.RTC_TRACE("EC property %s: %s",(k[0],k[1]))
        
    return True


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�ȤΥ���ե�����졼��������
  #
  # RT����ݡ��ͥ�Ȥη�����ӥ��󥹥�����˵��ܤ��줿�ץ�ѥƥ��ե������
  # ������ɤ߹��ߡ�����ݡ��ͥ�Ȥ����ꤹ�롣
  # �ޤ����ƥ���ݡ��ͥ�Ȥ� NamingService ��Ͽ����̾�Τ�����������ꤹ�롣
  #
  # @param self
  # @param comp ����ե�����졼������о�RT����ݡ��ͥ��
  #
  # @else
  #
  # @endif
  # void configureComponent(RTObject_impl* comp, const coil::Properties& prop);
  def configureComponent(self, comp, prop):
    category  = comp.getCategory()
    type_name = comp.getTypeName()
    inst_name = comp.getInstanceName()

    type_conf = category + "." + type_name + ".config_file"
    name_conf = category + "." + inst_name + ".config_file"

    type_prop = OpenRTM_aist.Properties()

    name_prop = OpenRTM_aist.Properties()

    if self._config.getProperty(name_conf) != "":
      try:
        conff = open(self._config.getProperty(name_conf))
      except:
        print "Not found. : %s" % self._config.getProperty(name_conf)
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      else:
        name_prop.load(conff)

    if self._config.findNode(category + "." + inst_name):
      name_prop.mergeProperties(self._config.getNode(category + "." + inst_name))

    if self._config.getProperty(type_conf) != "":
      try:
        conff = open(self._config.getProperty(type_conf))
      except:
        print "Not found. : %s" % self._config.getProperty(type_conf)
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      else:
        type_prop.load(conff)

    if self._config.findNode(category + "." + type_name):
      type_prop.mergeProperties(self._config.getNode(category + "." + type_name))

    comp.setProperties(prop)
    type_prop.mergeProperties(name_prop)
    comp.setProperties(type_prop)

    comp_prop = OpenRTM_aist.Properties(prop=comp.getProperties())

    naming_formats = self._config.getProperty("naming.formats")
    if comp_prop.findNode("naming.formats"):
      naming_formats = comp_prop.getProperty("naming.formats")
    naming_formats = OpenRTM_aist.flatten(OpenRTM_aist.unique_sv(OpenRTM_aist.split(naming_formats, ",")))

    naming_names = self.formatString(naming_formats, comp.getProperties())
    comp.getProperties().setProperty("naming.formats",naming_formats)
    comp.getProperties().setProperty("naming.names",naming_names)
    return


  ##
  # @if jp
  # @brief �ץ�ѥƥ�����Υޡ���
  #
  # ���ꤵ�줿�ե�����������ꤵ��Ƥ���ץ�ѥƥ��������ɤ���
  # ��¸������Ѥߥץ�ѥƥ��ȥޡ������롣
  #
  # @param self
  # @param prop �ޡ����оݥץ�ѥƥ�
  # @param file_name �ץ�ѥƥ����󤬵��Ҥ���Ƥ���ե�����̾
  #
  # @return �ޡ��������¹Է��(�ޡ�������:true���ޡ�������:false)
  #
  # @else
  #
  # @endif
  def mergeProperty(self, prop, file_name):
    if file_name == "":
      self._rtcout.RTC_ERROR("Invalid configuration file name.")
      return False
  
    if file_name[0] != '\0':
      
      try:
        conff = open(file_name)
      except:
        print "Not found. : %s" % file_name
        self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      else:
        prop.load(conff)
        conff.close()
        return True
  
    return False


  ##
  # @if jp
  # @brief NamingServer ����Ͽ����ݤ���Ͽ������Ȥ�Ω�Ƥ�
  #
  # ���ꤵ�줿�񼰤ȥץ�ѥƥ�������� NameServer ����Ͽ����ݤξ����
  # �Ȥ�Ω�Ƥ롣
  # �ƽ񼰻�����ʸ���ΰ�̣�ϰʲ��ΤȤ���
  # - % : ����ƥ����Ȥζ��ڤ�
  # - n : ���󥹥���̾��
  # - t : ��̾
  # - m : ��̾
  # - v : �С������
  # - V : �٥����
  # - c : ���ƥ���
  # - h : �ۥ���̾
  # - M : �ޥ͡�����̾
  # - p : �ץ���ID
  #
  # @param self
  # @param naming_format NamingService ��Ͽ����񼰻���
  # @param prop ���Ѥ���ץ�ѥƥ�����
  #
  # @return ������Ѵ����
  #
  # @else
  #
  # @endif
  def formatString(self, naming_format, prop):
    name_ = naming_format
    str_  = ""
    count = 0
    len_  = len(name_)
    it = iter(name_)

    try:
      while 1:
        n = it.next()
        if n == '%':
          count+=1
          if not (count % 2):
            str_ += n
        elif n == '$':
          count = 0
          n = it.next()
          if n == '{' or n == '(':
            n = it.next()
            env = ""
            for i in xrange(len_):
              if n == '}' or n == ')':
                break
              env += n
              n = it.next()
            envval = os.getenv(env)
            if envval:
              str_ += envval
          else:
            str_ += n
        else:
          if  count > 0 and (count % 2):
            count = 0
            if   n == "n": str_ += prop.getProperty("instance_name")
            elif n == "t": str_ += prop.getProperty("type_name")
            elif n == "m": str_ += prop.getProperty("type_name")
            elif n == "v": str_ += prop.getProperty("version")
            elif n == "V": str_ += prop.getProperty("vendor")
            elif n == "c": str_ += prop.getProperty("category")
            elif n == "h": str_ += self._config.getProperty("manager.os.hostname")
            elif n == "M": str_ += self._config.getProperty("manager.name")
            elif n == "p": str_ += str(self._config.getProperty("manager.pid"))
            else: str_ += n
          else:
            count = 0
            str_ += n
    except:
      # Caught StopIteration exception.
      return str_

    return str_


  ##
  # @if jp
  # @brief ���Хåե��μ���
  #
  # �ޥ͡���������ꤷ�����Хåե���������롣
  #
  # @param self
  #
  # @return �ޥ͡���������ꤷ�����Хåե�
  #
  # @else
  #
  # @endif
  def getLogbuf(self,name="manager"):
    if not OpenRTM_aist.toBool(self._config.getProperty("logger.enable"), "YES", "NO", True):
      return OpenRTM_aist.LogStream()

    logbuf = OpenRTM_aist.LogStream(name)
    logbuf.setLogLevel(self._config.getProperty("logger.log_level"))
    return logbuf


  ##
  # @if jp
  # @brief �ޥ͡����㥳��ե�����졼�����μ���
  #
  # �ޥ͡���������ꤷ������ե�����졼������������롣
  #
  # @param self
  #
  # @return �ޥ͡�����Υ���ե�����졼�����
  #
  # @else
  #
  # @endif
  def getConfig(self):
    return self._config


  ##
  # @if jp
  # @brief ����ݡ��ͥ�ȥե�����(.py)����
  #
  # �ޥ͡���������ꤷ������ե�����졼������������롣
  #
  # @param self
  #
  # @return �ޥ͡�����Υ���ե�����졼�����
  #
  # @else
  #
  # @endif
  def __try_direct_load(self, file_name):
    try:
      pathChanged=False
      splitted_name = os.path.split(file_name)
      save_path = sys.path[:]
      sys.path.append(splitted_name[0])
      import_name = splitted_name[-1].split(".py")[0]
      mo = __import__(import_name)
      sys.path = save_path
      _spec = getattr(mo,import_name.lower()+"_spec",None)
      _klass = getattr(mo,import_name,None)
      if _spec and _klass:
        prof = OpenRTM_aist.Properties(defaults_str=_spec)
        self.registerFactory(prof,
                             _klass,
                             OpenRTM_aist.Delete)
    except:
      self._rtcout.RTC_ERROR("Module load error: %s", file_name)
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      
    return



  #============================================================
  # ����ݡ��ͥ�ȥޥ͡�����
  #============================================================
  ##
  # @if jp
  # @class InstanceName
  # @brief ObjectManager �����ѥե��󥯥�
  #
  # @else
  #
  # @endif
  class InstanceName:
    """
    """

    ##
    # @if jp
    # @brief ���󥹥ȥ饯��
    #
    # ���󥹥ȥ饯��
    #
    # @param self
    # @param name �����оݥ���ݡ��ͥ��̾��(�ǥե������:None)
    # @param factory �����оݥե����ȥ�̾��(�ǥե������:None)
    #
    # @else
    #
    # @endif
    def __init__(self, name=None, factory=None, prop=None):
      if prop:
        self._name = prop.getInstanceName()
      if factory:
        self._name = factory.getInstanceName()
      elif name:
        self._name = name

    def __call__(self, factory):
      return self._name == factory.getInstanceName()



  #============================================================
  # ����ݡ��ͥ�ȥե����ȥ�
  #============================================================
  ##
  # @if jp
  # @class FactoryPredicate
  # @brief ����ݡ��ͥ�ȥե����ȥ긡���ѥե��󥯥�
  #
  # @else
  #
  # @endif
  class FactoryPredicate:

    def __init__(self, name=None, prop=None, factory=None):
      if name:
        self._vendor   = ""
        self._category = ""
        self._impleid  = name
        self._version  = ""
      elif prop:
        self._vendor   = prop.getProperty("vendor")
        self._category = prop.getProperty("category")
        self._impleid  = prop.getProperty("implementation_id")
        self._version  = prop.getProperty("version")
      elif factory:
        self._vendor   = factory.profile().getProperty("vendor")
        self._category = factory.profile().getProperty("category")
        self._impleid  = factory.profile().getProperty("implementation_id")
        self._version  = factory.profile().getProperty("version")


    def __call__(self, factory):
      if self._impleid == "":
        return False

      _prop = OpenRTM_aist.Properties(prop=factory.profile())

      if self._impleid != _prop.getProperty("implementation_id"):
        return False

      if self._vendor != "" and self._vendor != _prop.getProperty("vendor"):
        return False

      if self._category != "" and self._category != _prop.getProperty("category"):
        return False

      if self._version != "" and self._version != _prop.getProperty("version"):
        return False

      return True



  #============================================================
  # ExecutionContext�ե����ȥ�
  #============================================================
  ##
  # @if jp
  # @class ECFactoryPredicate
  # @brief ExecutionContext�ե����ȥ긡���ѥե��󥯥�
  #
  # @else
  #
  # @endif
  class ECFactoryPredicate:



    def __init__(self, name=None, factory=None):
      if name:
        self._name = name
      elif factory:
        self._name = factory.name()

    def __call__(self, factory):
      return self._name == factory.name()


  #============================================================
  # Module Fanctor
  #============================================================
  ##
  # @if jp
  # @class ModulePredicate
  # @brief Module�����ѥե��󥯥�
  #
  # @else
  #
  # @endif
  class ModulePredicate:

      # ModulePredicate(coil::Properties& prop)
      def __init__(self, prop):
        self._prop = prop
        return

      # bool operator()(coil::Properties& prop)
      def __call__(self, prop):

        if self._prop.getProperty("implementation_id") != prop.getProperty("implementation_id"):
          return False

        if self._prop.getProperty("vendor") and \
              self._prop.getProperty("vendor") != prop.getProperty("vendor"):
          return False
        
        if self._prop.getProperty("category") and \
              self._prop.getProperty("category") != prop.getProperty("category"):
          return False

        if self._prop.getProperty("version") and \
              self._prop.getProperty("version") != prop.getProperty("version"):
          return False

        return True


  #------------------------------------------------------------
  # ORB runner
  #------------------------------------------------------------
  ##
  # @if jp
  # @class OrbRunner
  # @brief OrbRunner ���饹
  #
  # ORB �¹��ѥإ�ѡ����饹��
  #
  # @since 0.4.0
  #
  # @else
  # @class OrbRunner
  # @brief OrbRunner class
  # @endif
  class OrbRunner:
    """
    """

    ##
    # @if jp
    # @brief ���󥹥ȥ饯��
    #
    # ���󥹥ȥ饯��
    #
    # @param self
    # @param orb ORB
    #
    # @else
    # @brief Constructor
    #
    # @endif
    def __init__(self, orb):
      self._orb = orb
      self._th = threading.Thread(target=self.run)
      self._th.start()


    def __del__(self):
      self._th.join()
      self._th = None
      return


    ##
    # @if jp
    # @brief ORB �¹Խ���
    #
    # ORB �¹�
    #
    # @param self
    #
    # @else
    #
    # @endif
    def run(self):
      try:
        self._orb.run()
        #Manager.instance().shutdown()
      except:
        print OpenRTM_aist.Logger.print_exception()
        pass
      return


    ##
    # @if jp
    # @brief ORB wait����
    #
    # ORB wait
    #
    # @param self
    #
    # @else
    #
    # @endif
    def wait(self):
      return

    ##
    # @if jp
    # @brief ORB ��λ����(̤����)
    #
    # ORB ��λ����
    #
    # @param self
    # @param flags ��λ�����ե饰
    #
    # @return ��λ�������
    #
    # @else
    #
    # @endif
    def close(self, flags):
      return 0


  #------------------------------------------------------------
  # Manager Terminator
  #------------------------------------------------------------
  ##
  # @if jp
  # @class Terminator
  # @brief Terminator ���饹
  #
  # ORB ��λ�ѥإ�ѡ����饹��
  #
  # @since 0.4.0
  #
  # @else
  #
  # @endif
  class Terminator:
    """
    """

    ##
    # @if jp
    # @brief ���󥹥ȥ饯��
    #
    # ���󥹥ȥ饯��
    #
    # @param self
    # @param manager �ޥ͡����㡦���֥�������
    #
    # @else
    # @brief Constructor
    #
    # @endif
    def __init__(self, manager):
      self._manager = manager


    ##
    # @if jp
    # @brief ��λ����
    #
    # ORB���ޥ͡����㽪λ�����򳫻Ϥ��롣
    #
    # @param self
    #
    # @else
    #
    # @endif
    def terminate(self):
      self._manager.shutdown()



  ##
  # @if jp
  # @class Term
  # @brief Term ���饹
  #
  # ��λ�ѥإ�ѡ����饹��
  #
  # @since 0.4.0
  #
  # @else
  #
  # @endif
  class Term:
    def __init__(self):
      self.waiting = 0
      self.mutex   = threading.RLock()


  class Finalized:
    def __init__(self):
      self.mutex = threading.RLock()
      self.comps = []
