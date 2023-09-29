#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file RTObject.py
# @brief RT component base class
# @date $Date: $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.



import string
import sys
import copy

from omniORB import any
from omniORB import CORBA

import OpenRTM__POA
import RTC
import SDOPackage
import OpenRTM_aist

ECOTHER_OFFSET = 1000

default_conf = [
  "implementation_id","",
  "type_name",         "",
  "description",       "",
  "version",           "",
  "vendor",            "",
  "category",          "",
  "activity_type",     "",
  "max_instance",      "",
  "language",          "",
  "lang_type",         "",
  "conf",              "",
  "" ]



##
# @if jp
# @brief RT����ݡ��ͥ�ȥ��饹
#
# ��RT����ݡ��ͥ�ȤΥ١����Ȥʤ륯�饹��
# Robotic Technology Component ������� lightweightRTComponent�μ������饹��
# ����ݡ��ͥ�Ȥε�ǽ���󶡤��� ComponentAction ���󥿡��ե�������
# ����ݡ��ͥ�ȤΥ饤�ե������������Ԥ������ LightweightRTObject �μ�����
# �󶡤��롣
# �ºݤ˥桼��������ݡ��ͥ�Ȥ����������ˤϡ�Execution Semantics ���б�
# �����ƥ��֥��饹�����Ѥ��롣<BR>
# (�����μ����Ǥ� Periodic Sampled Data Processing �Τߥ��ݡ��Ȥ��Ƥ��뤿�ᡢ
#  dataFlowComponent ��ľ�ܷѾ����Ƥ���)
#
# @since 0.2.0
#
# @else
#
# @endif
class RTObject_impl(OpenRTM__POA.DataFlowComponent):
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param manager �ޥ͡����㥪�֥�������(�ǥե������:None)
  # @param orb ORB(�ǥե������:None)
  # @param poa POA(�ǥե������:None)
  #
  # @else
  #
  # @brief Consructor
  #
  # @param orb ORB
  # @param poa POA
  #
  # @endif
  def __init__(self, manager=None, orb=None, poa=None):
    if manager:
      self._manager = manager
      self._orb = self._manager.getORB()
      self._poa = self._manager.getPOA()
      self._portAdmin = OpenRTM_aist.PortAdmin(self._manager.getORB(),self._manager.getPOA())
    else:
      self._manager = None
      self._orb = orb
      self._poa = poa
      self._portAdmin = OpenRTM_aist.PortAdmin(self._orb,self._poa)
      
    if self._manager:
      self._rtcout = self._manager.getLogbuf("rtobject")
    else:
      self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("rtobject")

    self._created = True
    self._properties = OpenRTM_aist.Properties(defaults_str=default_conf)
    self._configsets = OpenRTM_aist.ConfigAdmin(self._properties.getNode("conf"))
    self._profile = RTC.ComponentProfile("","","","","","",[],None,[])

    self._sdoservice = OpenRTM_aist.SdoServiceAdmin(self)
    self._SdoConfigImpl = OpenRTM_aist.Configuration_impl(self._configsets,self._sdoservice)
    self._SdoConfig = self._SdoConfigImpl.getObjRef()
    self._execContexts = []
    self._objref = self._this()
    self._sdoOwnedOrganizations = [] #SDOPackage.OrganizationList()
    self._sdoSvcProfiles        = [] #SDOPackage.ServiceProfileList()
    self._sdoOrganizations      = [] #SDOPackage.OrganizationList()
    self._sdoStatus             = [] #SDOPackage.NVList()
    self._ecMine  = []
    self._ecOther = []
    self._eclist  = []
    self._exiting = False
    self._readAll = False
    self._writeAll = False
    self._readAllCompletion = False
    self._writeAllCompletion = False
    self._inports = []
    self._outports = []
    self._actionListeners = OpenRTM_aist.ComponentActionListeners()
    self._portconnListeners = OpenRTM_aist.PortConnectListeners()
    return


  ##
  # @if jp
  #
  # @brief �ǥ��ȥ饯��
  #
  # @param self
  # 
  # @else
  # 
  # @brief destructor
  # 
  # @endif
  def __del__(self):
    return


  #============================================================
  # Overridden functions
  #============================================================

  ##
  # @if jp
  #
  # @brief ����������ѥ�����Хå��ؿ�
  # 
  # ComponentAction::on_initialize ���ƤФ줿�ݤ˼¹Ԥ���륳����Хå�
  # �ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�Ȥμºݤν���������ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣
  #
  # @param self
  # 
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onInitialize(self):
    self._rtcout.RTC_TRACE("onInitialize()")
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief ��λ�����ѥ�����Хå��ؿ�
  # 
  # ComponentAction::on_finalize ���ƤФ줿�ݤ˼¹Ԥ���륳����Хå�
  # �ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�Ȥμºݤν�λ�����ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣
  #
  # @param self
  # 
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onFinalize(self):
    self._rtcout.RTC_TRACE("onFinalize()")
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief ���Ͻ����ѥ�����Хå��ؿ�
  # 
  # ComponentAction::on_startup ���ƤФ줿�ݤ˼¹Ԥ���륳����Хå�
  # �ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�Ȥμºݤγ��Ͻ����ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣
  # 
  # @param self
  # @param ec_id ���ä��Ƥ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onStartup(self, ec_id):
    self._rtcout.RTC_TRACE("onStartup(%d)",ec_id)
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief ��߽����ѥ�����Хå��ؿ�
  # 
  # ComponentAction::on_shutdown ���ƤФ줿�ݤ˼¹Ԥ���륳����Хå�
  # �ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�Ȥμºݤ���߽����ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣
  # 
  # @param self
  # @param ec_id ���ä��Ƥ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onShutdown(self, ec_id):
    self._rtcout.RTC_TRACE("onShutdown(%d)",ec_id)
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief �����������ѥ�����Хå��ؿ�
  # 
  # ComponentAction::on_activated ���ƤФ줿�ݤ˼¹Ԥ���륳����Хå�
  # �ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�Ȥμºݤγ����������ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣
  # 
  # @param self
  # @param ec_id ���ä��Ƥ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onActivated(self, ec_id):
    self._rtcout.RTC_TRACE("onActivated(%d)",ec_id)
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief ������������ѥ�����Хå��ؿ�
  # 
  # ComponentAction::on_deactivated ���ƤФ줿�ݤ˼¹Ԥ���륳����Хå�
  # �ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�Ȥμºݤ�������������ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣
  # 
  # @param self
  # @param ec_id ���ä��Ƥ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onDeactivated(self, ec_id):
    self._rtcout.RTC_TRACE("onDeactivated(%d)",ec_id)
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief ���������ѥ�����Хå��ؿ�
  # 
  # DataFlowComponentAction::on_execute ���ƤФ줿�ݤ˼¹Ԥ����
  # ������Хå��ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�Ȥμºݤμ��������ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣<BR>
  # �ܴؿ��� Periodic Sampled Data Processing �ˤ����� Two-Pass Execution��
  # �����ܤμ¹ԥѥ��Ȥ������Ū�˸ƤӽФ���롣
  # 
  # @param self
  # @param ec_id ���ä��Ƥ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onExecute(self, ec_id):
    self._rtcout.RTC_TRACE("onExecute(%d)",ec_id)
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief ���ǽ����ѥ�����Хå��ؿ�
  # 
  # ComponentAction::on_aborting ���ƤФ줿�ݤ˼¹Ԥ���륳����Хå�
  # �ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�Ȥμºݤ����ǽ����ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣
  # 
  # @param self
  # @param ec_id ���ä��Ƥ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onAborting(self, ec_id):
    self._rtcout.RTC_TRACE("onAborting(%d)",ec_id)
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief ���顼�����ѥ�����Хå��ؿ�
  # 
  # ComponentAction::on_error ���ƤФ줿�ݤ˼¹Ԥ���륳����Хå��ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�ȤμºݤΥ��顼�����ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣
  # 
  # @param self
  # @param ec_id ���ä��Ƥ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onError(self, ec_id):
    self._rtcout.RTC_TRACE("onError(%d)",ec_id)
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief �ꥻ�åȽ����ѥ�����Хå��ؿ�
  # 
  # ComponentAction::on_reset ���ƤФ줿�ݤ˼¹Ԥ���륳����Хå��ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�ȤμºݤΥꥻ�åȽ����ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣
  # 
  # @param self
  # @param ec_id ���ä��Ƥ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onReset(self, ec_id):
    self._rtcout.RTC_TRACE("onReset(%d)",ec_id)
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief �����ѹ������ѥ�����Хå��ؿ�
  # 
  # DataFlowComponentAction::on_state_update ���ƤФ줿�ݤ˼¹Ԥ����
  # ������Хå��ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�Ȥμºݤξ����ѹ������ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣<BR>
  # �ܴؿ��� Periodic Sampled Data Processing �ˤ����� Two-Pass Execution��
  # �����ܤμ¹ԥѥ��Ȥ������Ū�˸ƤӽФ���롣
  #
  # @param self
  # @param ec_id ���ä��Ƥ��� ExecutionContext �� ID
  # 
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onStateUpdate(self, ec_id):
    self._rtcout.RTC_TRACE("onStateupdate(%d)",ec_id)
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief ư������ѹ������ѥ�����Хå��ؿ�
  # 
  # DataFlowComponentAction::on_rate_changed ���ƤФ줿�ݤ˼¹Ԥ����
  # ������Хå��ؿ���<BR>
  # �ܴؿ���̵���� RTC::RTC_OK ���֤��褦�˥��ߡ���������Ƥ���Τǡ�
  # �ƥ���ݡ��ͥ�Ȥμºݤξ����ѹ������ϡ��ܴؿ��򥪡��С��饤�ɤ��Ƽ�������
  # ɬ�פ����롣<BR>
  # �ܴؿ��� Periodic Sampled Data Processing �ˤ����� ExecutionContext ��
  # �¹Ԥ��������줿�ݤ˸ƤӽФ���롣
  #
  # @param self
  # @param ec_id ���ä��Ƥ��� ExecutionContext �� ID
  # 
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  # 
  # @endif
  def onRateChanged(self, ec_id):
    self._rtcout.RTC_TRACE("onRatechanged(%d)",ec_id)
    return RTC.RTC_OK 


  #============================================================
  # RTC::LightweightRTObject
  #============================================================

  ##
  # @if jp
  #
  # @brief [CORBA interface] RTC����������
  #
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��ơ�ComponentAction::on_initialize
  # ������Хå��ؿ����ƤФ�롣
  # 
  # ����
  # - RTC �� Created���֤ξ��߽�������Ԥ��롣¾�ξ��֤ˤ�����ˤ�
  #   ReturnCode_t::PRECONDITION_NOT_MET ���֤���ƤӽФ��ϼ��Ԥ��롣
  # - ���Υ��ڥ졼������ RTC �Υߥɥ륦��������ƤФ�뤳�Ȥ����ꤷ�Ƥ��ꡢ
  #   ���ץꥱ�������ȯ�Ԥ�ľ�ܤ��Υ��ڥ졼������Ƥ֤��Ȥ�����
  #   ����Ƥ��ʤ���
  #
  # @param self
  # 
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  #
  # @brief Initialize the RTC that realizes this interface.
  #
  # The invocation of this operation shall result in the invocation of the
  # callback ComponentAction::on_initialize.
  #
  # Constraints
  # - An RTC may be initialized only while it is in the Created state. Any
  #   attempt to invoke this operation while in another state shall fail
  #   with ReturnCode_t::PRECONDITION_NOT_MET.
  # - Application developers are not expected to call this operation
  #   directly; it exists for use by the RTC infrastructure.
  #
  # @return
  # 
  # @endif
  def initialize(self):
    self._rtcout.RTC_TRACE("initialize()")

    ec_args = self._properties.getProperty("exec_cxt.periodic.type")
    ec_args += "?"
    ec_args += "rate="
    ec_args += self._properties.getProperty("exec_cxt.periodic.rate")

    ec = OpenRTM_aist.Manager.instance().createContext(ec_args)
    if ec is None:
      return RTC.RTC_ERROR

    ec.set_rate(float(self._properties.getProperty("exec_cxt.periodic.rate")))
    self._eclist.append(ec)
    ecv = ec.getObjRef()
    if CORBA.is_nil(ecv):
      return RTC.RTC_ERROR

    ec.bindComponent(self)

    # at least one EC must be attached
    if len(self._ecMine) == 0:
      return RTC.PRECONDITION_NOT_MET

    ret = self.on_initialize()
    if ret is not RTC.RTC_OK:
      return ret
    self._created = False

    # -- entering alive state --
    for i in range(len(self._ecMine)):
      self._rtcout.RTC_DEBUG("EC[%d] starting.", i)
      self._ecMine[i].start()

    # ret must be RTC_OK
    return ret


  ##
  # @if jp
  #
  # @brief [CORBA interface] RTC ��λ����
  #
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� ComponentAction::on_finalize()
  # ��ƤӽФ���
  #
  # ����
  # - RTC �� ExecutionContext �˽�°���Ƥ���֤Ͻ�λ����ʤ������ξ��ϡ�
  #   �ޤ��ǽ�� ExecutionContextOperations::remove_component �ˤ�äƻ��ä�
  #   ������ʤ���Фʤ�ʤ�������ʳ��ξ��ϡ����Υ��ڥ졼�����ƤӽФ���
  #   �����ʤ���� ReturnCode_t::PRECONDITION_NOT_ME �Ǽ��Ԥ��롣
  # - RTC �� Created ���֤Ǥ����硢��λ�����ϹԤ��ʤ���
  #   ���ξ�硢���Υ��ڥ졼�����ƤӽФ��Ϥ����ʤ����
  #   ReturnCode_t::PRECONDITION_NOT_MET �Ǽ��Ԥ��롣
  # - ���Υ��ڥ졼������RTC�Υߥɥ륦��������ƤФ�뤳�Ȥ����ꤷ�Ƥ��ꡢ
  #   ���ץꥱ�������ȯ�Ԥ�ľ�ܤ��Υ��ڥ졼������Ƥ֤��Ȥ�����
  #   ����Ƥ��ʤ���
  #
  # @param self
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  #
  # @brief Finalize the RTC for preparing it for destruction
  # 
  # This invocation of this operation shall result in the invocation of the
  # callback ComponentAction::on_finalize.
  #
  # Constraints
  # - An RTC may not be finalized while it is participating in any execution
  #   context. It must first be removed with 
  #   ExecutionContextOperations::remove_component. Otherwise, this operation
  #   shall fail with ReturnCode_t::PRECONDITION_NOT_MET. 
  # - An RTC may not be finalized while it is in the Created state. Any 
  #   attempt to invoke this operation while in that state shall fail with 
  #   ReturnCode_t::PRECONDITION_NOT_MET.
  # - Application developers are not expected to call this operation directly;
  #  it exists for use by the RTC infrastructure.
  #
  # @return
  # 
  # @endif
  def finalize(self):
    self._rtcout.RTC_TRACE("finalize()")
    if self._created or not self._exiting:
      return RTC.PRECONDITION_NOT_MET

    # Return RTC::PRECONDITION_NOT_MET,
    # When the component is registered in ExecutionContext.
    if len(self._ecOther) != 0:
      for ec in self._ecOther:
        if not CORBA.is_nil(ec):
          return RTC.PRECONDITION_NOT_MET
      
      self._ecOther = []

    ret = self.on_finalize()
    self.shutdown()
    return ret


  ##
  # @if jp
  #
  # @brief [CORBA interface] RTC �������ʡ��Ǥ��� ExecutionContext ��
  #        ��ߤ��������Υ���ƥ�Ĥȶ��˽�λ������
  #
  # ���� RTC �������ʡ��Ǥ��뤹�٤Ƥμ¹ԥ���ƥ����Ȥ���ߤ��롣
  # ���� RTC ��¾�μ¹ԥ���ƥ����Ȥ��ͭ���� RTC ��°����¹ԥ���ƥ�����
  # (i.e. �¹ԥ���ƥ����Ȥ��ͭ���� RTC �Ϥ��ʤ�����μ¹ԥ���ƥ����Ȥ�
  # �����ʡ��Ǥ��롣)�˻��ä��Ƥ����硢���� RTC �Ϥ����Υ���ƥ����Ⱦ�
  # �������������ʤ���Фʤ�ʤ���
  # RTC ���¹���Τɤ� ExecutionContext �Ǥ� Active ���֤ǤϤʤ��ʤä��塢
  # ���� RTC �Ȥ���˴ޤޤ�� RTC ����λ���롣
  # 
  # ����
  # - RTC �����������Ƥ��ʤ���С���λ�����뤳�ȤϤǤ��ʤ���
  #   Created ���֤ˤ��� RTC �� exit() ��ƤӽФ�����硢
  #   ReturnCode_t::PRECONDITION_NOT_MET �Ǽ��Ԥ��롣
  #
  # @param self
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # 
  # @else
  #
  # @brief Stop the RTC's execution context(s) and finalize it along with its
  #        contents.
  # 
  # Any execution contexts for which the RTC is the owner shall be stopped. 
  # If the RTC participates in any execution contexts belonging to another
  # RTC that contains it, directly or indirectly (i.e. the containing RTC
  # is the owner of the ExecutionContext), it shall be deactivated in those
  # contexts.
  # After the RTC is no longer Active in any Running execution context, it
  # and any RTCs contained transitively within it shall be finalized.
  #
  # Constraints
  # - An RTC cannot be exited if it has not yet been initialized. Any
  #   attempt to exit an RTC that is in the Created state shall fail with
  #   ReturnCode_t::PRECONDITION_NOT_MET.
  #
  # @return
  # 
  # @endif
  def exit(self):
    self._rtcout.RTC_TRACE("exit()")
    if self._created:
      return RTC.PRECONDITION_NOT_MET

    # deactivate myself on owned EC
    OpenRTM_aist.CORBA_SeqUtil.for_each(self._ecMine,
                                        self.deactivate_comps(self._objref))
    # deactivate myself on other EC
    OpenRTM_aist.CORBA_SeqUtil.for_each(self._ecOther,
                                        self.deactivate_comps(self._objref))

    # stop and detach myself from owned EC
    for ec in self._ecMine:
      if not CORBA.is_nil(ec) or not ec._non_existent():
        # ret = ec.stop()
        # ec.remove_component(self._this())
        pass

    # detach myself from other EC
    for ec in self._ecOther:
      if not CORBA.is_nil(ec):
        # ec.stop()
        ec.remove_component(self._this())

    self._exiting = True
    return self.finalize()


  ##
  # @if jp
  #
  # @brief [CORBA interface] RTC �� Alive ���֤Ǥ��뤫�ɤ�����ǧ���롣
  #
  # RTC �����ꤷ�� ExecutionContext ���Ф��� Alive���֤Ǥ��뤫�ɤ�����ǧ���롣
  # RTC �ξ��֤� Active �Ǥ��뤫��Inactive �Ǥ��뤫��Error �Ǥ��뤫�ϼ¹����
  # ExecutionContext �˰�¸���롣���ʤ�������� ExecutionContext ���Ф��Ƥ�
  # Active  ���֤Ǥ��äƤ⡢¾�� ExecutionContext ���Ф��Ƥ� Inactive ���֤�
  # �ʤ���⤢�ꤨ�롣���äơ����Υ��ڥ졼�����ϻ��ꤵ�줿
  # ExecutionContext ���䤤��碌�ơ����� RTC �ξ��֤� Active��Inactive��
  # Error �ξ��ˤ� Alive ���֤Ȥ����֤���
  #
  # @param self
  #
  # @param exec_context �����о� ExecutionContext �ϥ�ɥ�
  #
  # @return Alive ���ֳ�ǧ���
  #
  # @else
  #
  # @brief Confirm whether RTC is an Alive state or NOT.
  #
  # A component is alive or not regardless of the execution context from
  # which it is observed. However, whether or not it is Active, Inactive,
  # or in Error is dependent on the execution context(s) in which it is
  # running. That is, it may be Active in one context but Inactive in
  # another. Therefore, this operation shall report whether this RTC is
  # either Active, Inactive or in Error; which of those states a component
  # is in with respect to a particular context may be queried from the
  # context itself.
  #
  # @return Result of Alive state confirmation
  #
  # @endif
  # virtual CORBA::Boolean is_alive(ExecutionContext_ptr exec_context)
  def is_alive(self, exec_context):
    self._rtcout.RTC_TRACE("is_alive()")
    for ec in self._ecMine:
      if exec_context._is_equivalent(ec):
        return True

    for ec in self._ecOther:
      if not CORBA.is_nil(ec):
        if exec_context._is_equivalent(ec):
          return True

    return False


  ##
  # @if jp
  # @brief [CORBA interface] ExecutionContextList���������
  #
  # ���� RTC ����ͭ���� ExecutionContext �Υꥹ�Ȥ�������롣
  #
  # @param self
  #
  # @return ExecutionContext �ꥹ��
  #
  # @else
  # @brief [CORBA interface] Get ExecutionContextList.
  #
  # This operation returns a list of all execution contexts owned by this RTC.
  #
  # @return ExecutionContext List
  #
  # @endif
  #def get_contexts(self):
  #  execlist = []
  #  OpenRTM_aist.CORBA_SeqUtil.for_each(self._execContexts, self.ec_copy(execlist))
  #  return execlist


  ##
  # @if jp
  # @brief [CORBA interface] ExecutionContext���������
  #
  # ���ꤷ���ϥ�ɥ�� ExecutionContext ��������롣
  # �ϥ�ɥ뤫�� ExecutionContext �ؤΥޥåԥ󥰤ϡ������ RTC ���󥹥��󥹤�
  # ��ͭ�Ǥ��롣�ϥ�ɥ�Ϥ��� RTC �� attach_context �����ݤ˼����Ǥ��롣
  #
  # @param self
  # @param ec_id �����о� ExecutionContext �ϥ�ɥ�
  #
  # @return ExecutionContext
  #
  # @else
  # @brief [CORBA interface] Get ExecutionContext.
  #
  # Obtain a reference to the execution context represented by the given 
  # handle.
  # The mapping from handle to context is specific to a particular RTC 
  # instance. The given handle must have been obtained by a previous call to 
  # attach_context on this RTC.
  #
  # @param ec_id ExecutionContext handle
  #
  # @return ExecutionContext
  #
  # @endif
  # virtual ExecutionContext_ptr get_context(UniqueId exec_handle)
  def get_context(self, ec_id):
    global ECOTHER_OFFSET

    self._rtcout.RTC_TRACE("get_context(%d)", ec_id)
    # owned EC
    if ec_id < ECOTHER_OFFSET:
      if ec_id < len(self._ecMine):
        return self._ecMine[ec_id]
      else:
        return RTC.ExecutionContext._nil

    # participating EC
    index = ec_id - ECOTHER_OFFSET

    if index < len(self._ecOther):
      if not CORBA.is_nil(self._ecOther[index]):
        return self._ecOther[index]

    return RTC.ExecutionContext._nil


  ##
  # @if jp
  # @brief [CORBA interface] ��ͭ���� ExecutionContextList�� ��������
  #
  # ���� RTC ����ͭ���� ExecutionContext �Υꥹ�Ȥ�������롣
  #
  # @return ExecutionContext �ꥹ��
  #
  # @else
  # @brief [CORBA interface] Get ExecutionContextList.
  #
  # This operation returns a list of all execution contexts owned by this
  # RTC.
  #
  # @return ExecutionContext List
  #
  # @endif
  # virtual ExecutionContextList* get_owned_contexts()
  def get_owned_contexts(self):
    self._rtcout.RTC_TRACE("get_owned_contexts()")
    execlist = []
    OpenRTM_aist.CORBA_SeqUtil.for_each(self._ecMine, self.ec_copy(execlist))
    return execlist

  ##
  # @if jp
  # @brief [CORBA interface] ���ä��Ƥ��� ExecutionContextList ���������
  #
  # ���� RTC �����ä��Ƥ��� ExecutionContext �Υꥹ�Ȥ�������롣
  #
  # @return ExecutionContext �ꥹ��
  #
  # @else
  # @brief [CORBA interface] Get participating ExecutionContextList.
  #
  # This operation returns a list of all execution contexts in
  # which this RTC participates.
  #
  # @return ExecutionContext List
  #
  # @endif
  # virtual ExecutionContextList* get_participating_contexts()
  def get_participating_contexts(self):
    self._rtcout.RTC_TRACE("get_participating_contexts()")
    execlist = []
    OpenRTM_aist.CORBA_SeqUtil.for_each(self._ecOther, self.ec_copy(execlist))
    return execlist


  #
  # @if jp
  # @brief [CORBA interface] ExecutionContext �Υϥ�ɥ���֤�
  #
  # @param ExecutionContext �¹ԥ���ƥ�����
  #
  # @return ExecutionContextHandle
  #
  # Ϳ����줿�¹ԥ���ƥ����Ȥ˴�Ϣ�դ���줿�ϥ�ɥ���֤���
  #
  # @else
  # @brief [CORBA interface] Return a handle of a ExecutionContext
  #
  # @param ExecutionContext
  #
  # @return ExecutionContextHandle
  #
  # This operation returns a handle that is associated with the given
  # execution context.
  #
  # @endif
  #
  # virtual ExecutionContextHandle_t
  #   get_context_handle(ExecutionContext_ptr cxt)
  def get_context_handle(self, cxt):
    self._rtcout.RTC_TRACE("get_context_handle()")

    num = OpenRTM_aist.CORBA_SeqUtil.find(self._ecMine, self.ec_find(cxt))
    if num != -1:
      return long(num)

    num = OpenRTM_aist.CORBA_SeqUtil.find(self._ecOther, self.ec_find(cxt))
    if num != -1:
      return long(num)

    return long(-1)


  #============================================================
  # RTC::RTObject
  #============================================================

  ##
  # @if jp
  #
  # @brief [RTObject CORBA interface] ����ݡ��ͥ�ȥץ�ե�������������
  #
  # ��������ݡ��ͥ�ȤΥץ�ե����������֤��� 
  #
  # @param self
  #
  # @return ����ݡ��ͥ�ȥץ�ե�����
  #
  # @else
  #
  # @brief [RTObject CORBA interface] Get RTC's profile
  #
  # This operation returns the ComponentProfile of the RTC
  #
  # @return ComponentProfile
  #
  # @endif
  # virtual ComponentProfile* get_component_profile()
  def get_component_profile(self):
    self._rtcout.RTC_TRACE("get_component_profile()")
    try:
      prop_ = RTC.ComponentProfile(self._properties.getProperty("instance_name"),
                                   self._properties.getProperty("type_name"),
                                   self._properties.getProperty("description"),
                                   self._properties.getProperty("version"),
                                   self._properties.getProperty("vendor"),
                                   self._properties.getProperty("category"),
                                   self._portAdmin.getPortProfileList(),
                                   self._profile.parent,
                                   self._profile.properties) 
      OpenRTM_aist.NVUtil.copyFromProperties(self._profile.properties, self._properties)
      return prop_
      # return RTC.ComponentProfile(self._profile.instance_name,
      #               self._profile.type_name,
      #               self._profile.description,
      #               self._profile.version,
      #               self._profile.vendor,
      #               self._profile.category,
      #               self._portAdmin.getPortProfileList(),
      #               self._profile.parent,
      #               self._profile.properties)
    
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    assert(False)
    return None


  ##
  # @if jp
  #
  # @brief [RTObject CORBA interface] �ݡ��Ȥ��������
  #
  # ��������ݡ��ͥ�Ȥ���ͭ����ݡ��Ȥλ��Ȥ��֤���
  #
  # @param self
  #
  # @return �ݡ��ȥꥹ��
  #
  # @else
  #
  # @brief [RTObject CORBA interface] Get Ports
  #
  # This operation returns a list of the RTCs ports.
  #
  # @return PortList
  #
  # @endif
  # virtual PortServiceList* get_ports()
  def get_ports(self):
    self._rtcout.RTC_TRACE("get_ports()")
    try:
      return self._portAdmin.getPortServiceList()
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    assert(False)
    return []



  # RTC::ComponentAction

  ##
  # @if jp
  # @brief [CORBA interface] ExecutionContext��attach����
  #
  # ���ꤷ�� ExecutionContext �ˤ��� RTC ���°�����롣���� RTC �ȴ�Ϣ���� 
  # ExecutionContext �Υϥ�ɥ���֤���
  # ���Υ��ڥ졼�����ϡ�ExecutionContextOperations::add_component ���ƤФ줿
  # �ݤ˸ƤӽФ���롣�֤��줿�ϥ�ɥ��¾�Υ��饤����Ȥǻ��Ѥ��뤳�Ȥ�����
  # ���Ƥ��ʤ���
  #
  # @param self
  # @param exec_context ��°�� ExecutionContext
  #
  # @return ExecutionContext �ϥ�ɥ�
  #
  # @else
  # @brief [CORBA interface] Attach ExecutionContext.
  #
  # Inform this RTC that it is participating in the given execution context. 
  # Return a handle that represents the association of this RTC with the 
  # context.
  # This operation is intended to be invoked by 
  # ExecutionContextOperations::add_component. It is not intended for use by 
  # other clients.
  #
  # @param exec_context Prticipating ExecutionContext
  #
  # @return ExecutionContext Handle
  #
  # @endif
  # UniqueId attach_context(ExecutionContext_ptr exec_context)
  def attach_context(self, exec_context):
    global ECOTHER_OFFSET
    self._rtcout.RTC_TRACE("attach_context()")
    # ID: 0 - (offset-1) : owned ec
    # ID: offset -       : participating ec
    # owned       ec index = ID
    # participate ec index = ID - offset
    ecs = exec_context._narrow(RTC.ExecutionContextService)
    if CORBA.is_nil(ecs):
      return -1
    
    # if m_ecOther has nil element, insert attached ec to there.
    for i in range(len(self._ecOther)):
      if CORBA.is_nil(self._ecOther[i]):
        self._ecOther[i] = ecs
        ec_id = i + ECOTHER_OFFSET
        self.onAttachExecutionContext(ec_id)
        return ec_id

    # no space in the list, push back ec to the last.
    OpenRTM_aist.CORBA_SeqUtil.push_back(self._ecOther,ecs)
    ec_id = long(len(self._ecOther) - 1 + ECOTHER_OFFSET)
    self.onAttachExecutionContext(ec_id)
    return ec_id


  # UniqueId bindContext(ExecutionContext_ptr exec_context);
  def bindContext(self, exec_context):
    global ECOTHER_OFFSET
    self._rtcout.RTC_TRACE("bindContext()")
    # ID: 0 - (offset-1) : owned ec
    # ID: offset -       : participating ec
    # owned       ec index = ID
    # participate ec index = ID - offset
    ecs = exec_context._narrow(RTC.ExecutionContextService)

    if CORBA.is_nil(ecs):
      return -1
    
    # if m_ecMine has nil element, insert attached ec to there.
    for i in range(len(self._ecMine)):
      if CORBA.is_nil(self._ecMine[i]):
        self._ecMine[i] = ecs
        self.onAttachExecutionContext(i)
        return i
        #return i + ECOTHER_OFFSET

    # no space in the list, push back ec to the last.
    OpenRTM_aist.CORBA_SeqUtil.push_back(self._ecMine,ecs)
    
    return long(len(self._ecMine) - 1)
    #return long(len(self._ecMine) - 1 + ECOTHER_OFFSET)


  ##
  # @if jp
  # @brief [CORBA interface] ExecutionContext��detach����
  #
  # ���ꤷ�� ExecutionContext ���餳�� RTC �ν�°�������롣
  # ���Υ��ڥ졼�����ϡ�ExecutionContextOperations::remove_component ���Ƥ�
  # �줿�ݤ˸ƤӽФ���롣�֤��줿�ϥ�ɥ��¾�Υ��饤����Ȥǻ��Ѥ��뤳�Ȥ�
  # ���ꤷ�Ƥ��ʤ���
  # 
  # ����
  # - ���ꤵ�줿 ExecutionContext �� RTC �����Ǥ˽�°���Ƥ��ʤ����ˤϡ�
  #   ReturnCode_t::PRECONDITION_NOT_MET ���֤���롣
  # - ���ꤵ�줿 ExecutionContext �ˤ��������Ф��� RTC ��Active ���֤Ǥ����
  #   ��ˤϡ� ReturnCode_t::PRECONDITION_NOT_MET ���֤���롣
  #
  # @param self
  # @param ec_id ����о� ExecutionContext�ϥ�ɥ�
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  # @brief [CORBA interface] Attach ExecutionContext.
  #
  # Inform this RTC that it is no longer participating in the given execution 
  # context.
  # This operation is intended to be invoked by 
  # ExecutionContextOperations::remove_component. It is not intended for use 
  # by other clients.
  # Constraints
  # - This operation may not be invoked if this RTC is not already 
  #   participating in the execution context. Such a call shall fail with 
  #   ReturnCode_t::PRECONDITION_NOT_MET.
  # - This operation may not be invoked if this RTC is Active in the indicated
  #   execution context. Otherwise, it shall fail with 
  #   ReturnCode_t::PRECONDITION_NOT_MET.
  #
  # @param ec_id Dettaching ExecutionContext Handle
  #
  # @return
  #
  # @endif
  # ReturnCode_t detach_context(UniqueId exec_handle)
  def detach_context(self, ec_id):
    global ECOTHER_OFFSET
    self._rtcout.RTC_TRACE("detach_context(%d)", ec_id)
    len_ = len(self._ecOther)

    # ID: 0 - (offset-1) : owned ec
    # ID: offset -       : participating ec
    # owned       ec index = ID
    # participate ec index = ID - offset
    if (long(ec_id) < long(ECOTHER_OFFSET)) or \
          (long(ec_id - ECOTHER_OFFSET) > len_):
      return RTC.BAD_PARAMETER
    
    index = long(ec_id - ECOTHER_OFFSET)

    if index < 0 or CORBA.is_nil(self._ecOther[index]):
      return RTC.BAD_PARAMETER
    
    #OpenRTM_aist.CORBA_SeqUtil.erase(self._ecOther, index)
    self._ecOther[index] = RTC.ExecutionContextService._nil
    self.onDetachExecutionContext(ec_id)
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �ν����
  #
  # RTC ����������졢Alive ���֤����ܤ��롣
  # RTC ��ͭ�ν���������Ϥ����Ǽ¹Ԥ��롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onInitialize() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # @param self
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] Initialize RTC
  #
  # The RTC has been initialized and entered the Alive state.
  # Any RTC-specific initialization logic should be performed here.
  #
  # @return
  #
  # @endif
  def on_initialize(self):
    self._rtcout.RTC_TRACE("on_initialize()")
    ret = RTC.RTC_ERROR
    try:
      self.preOnInitialize(0)
      ret = self.onInitialize()
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      ret = RTC.RTC_ERROR

    active_set = self._properties.getProperty("configuration.active_config",
                                              "default")

    if self._configsets.haveConfig(active_set):
      self._configsets.update(active_set)
    else:
      self._configsets.update("default")

    self.postOnInitialize(0,ret)
    return ret


  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �ν�λ
  #
  # RTC ���˴�����롣
  # RTC ��ͭ�ν�λ�����Ϥ����Ǽ¹Ԥ��롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onFinalize() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # @param self
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] Finalize RTC
  #
  # The RTC is being destroyed.
  # Any final RTC-specific tear-down logic should be performed here.
  #
  # @return
  #
  # @endif
  def on_finalize(self):
    self._rtcout.RTC_TRACE("on_finalize()")
    ret = RTC.RTC_ERROR
    try:
      self.preOnFinalize(0)
      ret = self.onFinalize()
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      ret = RTC.RTC_ERROR
    self.postOnFinalize(0, ret)
    return ret


  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �γ���
  #
  # RTC ����°���� ExecutionContext �� Stopped ���֤��� Running ���֤�����
  # �������˸ƤӽФ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onStartup() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # @param self
  # @param ec_id �������ܤ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] StartUp RTC
  #
  # The given execution context, in which the RTC is participating, has 
  # transitioned from Stopped to Running.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_startup(self, ec_id):
    self._rtcout.RTC_TRACE("on_startup(%d)", ec_id)
    ret = RTC.RTC_ERROR
    try:
      self.preOnStartup(ec_id)
      ret = self.onStartup(ec_id)
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      ret = RTC.RTC_ERROR
    self.postOnStartup(ec_id, ret)
    return ret


  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �����
  #
  # RTC ����°���� ExecutionContext �� Running ���֤��� Stopped ���֤�����
  # �������˸ƤӽФ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onShutdown() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # @param self
  # @param ec_id �������ܤ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] ShutDown RTC
  #
  # The given execution context, in which the RTC is participating, has 
  # transitioned from Running to Stopped.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_shutdown(self, ec_id):
    self._rtcout.RTC_TRACE("on_shutdown(%d)", ec_id)
    ret = RTC.RTC_ERROR
    try:
      self.preOnShutdown(ec_id)
      ret = self.onShutdown(ec_id)
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      ret = RTC.RTC_ERROR
    self.postOnShutdown(ec_id, ret)
    return ret


  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �γ�����
  #
  # ��°���� ExecutionContext ���� RTC �����������줿�ݤ˸ƤӽФ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onActivated() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # @param self
  # @param ec_id ������ ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] Activate RTC
  #
  # The RTC has been activated in the given execution context.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_activated(self, ec_id):
    self._rtcout.RTC_TRACE("on_activated(%d)", ec_id)
    ret = RTC.RTC_ERROR
    try:
      self.preOnActivated(ec_id)
      self._configsets.update()
      ret = self.onActivated(ec_id)
      self._portAdmin.activatePorts()
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      ret = RTC.RTC_ERROR
    self.postOnActivated(ec_id, ret)
    return ret


  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC ���������
  #
  # ��°���� ExecutionContext ���� RTC ������������줿�ݤ˸ƤӽФ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onDeactivated() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # @param self
  # @param ec_id ������� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] Deactivate RTC
  #
  # The RTC has been deactivated in the given execution context.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_deactivated(self, ec_id):
    self._rtcout.RTC_TRACE("on_deactivated(%d)", ec_id)
    ret = RTC.RTC_ERROR
    try:
      self.preOnDeactivated(ec_id)
      self._portAdmin.deactivatePorts()
      ret = self.onDeactivated(ec_id)
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      ret = RTC.RTC_ERROR
    self.postOnDeactivated(ec_id, ret)
    return ret


  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �Υ��顼���֤ؤ�����
  #
  # RTC ����°���� ExecutionContext �� Active ���֤��� Error ���֤����ܤ���
  # ���˸ƤӽФ���롣
  # ���Υ��ڥ졼������ RTC �� Error ���֤����ܤ����ݤ˰��٤����ƤӽФ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onAborting() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # @param self
  # @param ec_id �������ܤ��� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] Transition Error State
  #
  # The RTC is transitioning from the Active state to the Error state in some
  # execution context.
  # This callback is invoked only a single time for time that the RTC 
  # transitions into the Error state from another state. This behavior is in 
  # contrast to that of on_error.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_aborting(self, ec_id):
    self._rtcout.RTC_TRACE("on_aborting(%d)", ec_id)
    ret = RTC.RTC_ERROR
    try:
      self.preOnAborting(ec_id)
      ret = self.onAborting(ec_id)
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      ret = RTC.RTC_ERROR
    self.postOnAborting(ec_id, ret)
    return ret


  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �Υ��顼����
  #
  # RTC �����顼���֤ˤ���ݤ˸ƤӽФ���롣
  # RTC �����顼���֤ξ��ˡ��оݤȤʤ� ExecutionContext ��ExecutionKind ��
  # �����������ߥ󥰤ǸƤӽФ���롣�㤨�С�
  # - ExecutionKind �� PERIODIC �ξ�硢�ܥ��ڥ졼������
  #   DataFlowComponentAction::on_execute �� on_state_update ���ؤ��ˡ�
  #   ���ꤵ�줿���֡����ꤵ�줿�����ǸƤӽФ���롣
  # - ExecutionKind �� EVENT_DRIVEN �ξ�硢�ܥ��ڥ졼������
  #   FsmParticipantAction::on_action ���ƤФ줿�ݤˡ��ؤ��˸ƤӽФ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onError() ������Хå��ؿ����Ƥӽ�
  # ����롣
  #
  # @param self
  # @param ec_id �о� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] Error Processing of RTC
  #
  # The RTC remains in the Error state.
  # If the RTC is in the Error state relative to some execution context when
  # it would otherwise be invoked from that context (according to the 
  # context��s ExecutionKind), this callback shall be invoked instead. 
  # For example,
  # - If the ExecutionKind is PERIODIC, this operation shall be invoked in 
  #   sorted order at the rate of the context instead of 
  #   DataFlowComponentAction::on_execute and on_state_update.
  # - If the ExecutionKind is EVENT_DRIVEN, this operation shall be invoked 
  #   whenever FsmParticipantAction::on_action would otherwise have been 
  #   invoked.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_error(self, ec_id):
    self._rtcout.RTC_TRACE("on_error(%d)", ec_id)
    ret = RTC.RTC_ERROR
    try:
      self.preOnError(ec_id)
      ret = self.onError(ec_id)
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      ret = RTC.RTC_ERROR
    self._configsets.update()
    self.postOnError(ec_id, ret)
    return ret


  ##
  # @if jp
  #
  # @brief [ComponentAction CORBA interface] RTC �Υꥻ�å�
  #
  # Error ���֤ˤ��� RTC �Υꥫ�Х������¹Ԥ���Inactive ���֤�����������
  # ���˸ƤӽФ���롣
  # RTC �Υꥫ�Х������������������ Inactive ���֤��������뤬������ʳ���
  # ���ˤ� Error ���֤�α�ޤ롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onReset() ������Хå��ؿ����Ƥ�
  # �Ф���롣
  #
  # @param self
  # @param ec_id �ꥻ�å��о� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [ComponentAction CORBA interface] Resetting RTC
  #
  # The RTC is in the Error state. An attempt is being made to recover it such
  # that it can return to the Inactive state.
  # If the RTC was successfully recovered and can safely return to the
  # Inactive state, this method shall complete with ReturnCode_t::OK. Any
  # other result shall indicate that the RTC should remain in the Error state.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_reset(self, ec_id):
    self._rtcout.RTC_TRACE("on_reset(%d)", ec_id)
    ret = RTC.RTC_ERROR
    try:
      self.preOnReset(ec_id)
      ret = self.onReset(ec_id)
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      ret = RTC.RTC_ERROR
    self.postOnReset(ec_id, ret)
    return ret


  ##
  # @if jp
  #
  # @brief [DataFlowComponentAction CORBA interface] RTC ��������(������)
  #
  # �ʲ��ξ��֤��ݻ�����Ƥ�����ˡ����ꤵ�줿���������Ū�˸ƤӽФ���롣
  # - RTC �� Alive ���֤Ǥ��롣
  # - ���ꤵ�줿 ExecutionContext �� Running ���֤Ǥ��롣
  # �ܥ��ڥ졼�����ϡ�Two-Pass Execution ���������Ǽ¹Ԥ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onExecute() ������Хå��ؿ����Ƥ�
  # �Ф���롣
  #
  # ����
  # - ���ꤵ�줿 ExecutionContext �� ExecutionKind �ϡ� PERIODIC �Ǥʤ���Ф�
  #   ��ʤ�
  #
  # @param self
  # @param ec_id �������о� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [DataFlowComponentAction CORBA interface] Primary Periodic 
  #        Operation of RTC
  #
  # This operation will be invoked periodically at the rate of the given
  # execution context as long as the following conditions hold:
  # - The RTC is Active.
  # - The given execution context is Running
  # This callback occurs during the first execution pass.
  #
  # Constraints
  # - The execution context of the given context shall be PERIODIC.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_execute(self, ec_id):
    self._rtcout.RTC_TRACE("on_execute(%d)", ec_id)
    ret = RTC.RTC_ERROR
    try:
      self.preOnExecute(ec_id)
      if self._readAll:
        self.readAll()
      
      ret = self.onExecute(ec_id)

      if self._writeAll:
        self.writeAll()
      
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      ret = RTC.RTC_ERROR
    self.postOnExecute(ec_id, ret)
    return ret


  ##
  # @if jp
  #
  # @brief [DataFlowComponentAction CORBA interface] RTC ��������(�������)
  #
  # �ʲ��ξ��֤��ݻ�����Ƥ�����ˡ����ꤵ�줿���������Ū�˸ƤӽФ���롣
  # - RTC �� Alive ���֤Ǥ��롣
  # - ���ꤵ�줿 ExecutionContext �� Running ���֤Ǥ��롣
  # �ܥ��ڥ졼�����ϡ�Two-Pass Execution ����������Ǽ¹Ԥ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onStateUpdate() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # ����
  # - ���ꤵ�줿 ExecutionContext �� ExecutionKind �ϡ� PERIODIC �Ǥʤ���Ф�
  #   ��ʤ�
  #
  # @param self
  # @param ec_id �������о� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [DataFlowComponentAction CORBA interface] Secondary Periodic 
  #        Operation of RTC
  #
  # This operation will be invoked periodically at the rate of the given
  # execution context as long as the following conditions hold:
  # - The RTC is Active.
  # - The given execution context is Running
  # This callback occurs during the second execution pass.
  #
  # Constraints
  # - The execution context of the given context shall be PERIODIC.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_state_update(self, ec_id):
    self._rtcout.RTC_TRACE("on_state_update(%d)", ec_id)
    ret = RTC.RTC_ERROR
    try:
      self.preOnStateUpdate(ec_id)
      ret = self.onStateUpdate(ec_id)
      self._configsets.update()
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      ret = RTC.RTC_ERROR
    self.postOnStateUpdate(ec_id, ret)
    return ret


  ##
  # @if jp
  #
  # @brief [DataFlowComponentAction CORBA interface] �¹Լ����ѹ�����
  #
  # �ܥ��ڥ졼�����ϡ�ExecutionContext �μ¹Լ������ѹ����줿���Ȥ����Τ���
  # �ݤ˸ƤӽФ���롣
  # ���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��� onRateChanged() ������Хå��ؿ���
  # �ƤӽФ���롣
  #
  # ����
  # - ���ꤵ�줿 ExecutionContext �� ExecutionKind �ϡ� PERIODIC �Ǥʤ���Ф�
  #   ��ʤ�
  #
  # @param self
  # @param ec_id �������о� ExecutionContext �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [DataFlowComponentAction CORBA interface] Notify rate chenged
  #
  # This operation is a notification that the rate of the indicated execution 
  # context has changed.
  #
  # Constraints
  # - The execution context of the given context shall be PERIODIC.
  #
  # @param ec_id
  #
  # @return
  #
  # @endif
  def on_rate_changed(self, ec_id):
    self._rtcout.RTC_TRACE("on_rate_changed(%d)", ec_id)
    ret = RTC.RTC_ERROR
    try:
      self.preOnRateChanged(ec_id)
      ret = self.onRateChanged(ec_id)
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      ret = RTC.RTC_ERROR
    self.postOnRateChanged(ec_id, ret)
    return ret


  #============================================================
  # SDOPackage::SdoSystemElement
  #============================================================

  ##
  # @if jp
  # 
  # @brief [SDO interface] Organization �ꥹ�Ȥμ��� 
  #
  # SDOSystemElement ��0�Ĥ⤷���Ϥ���ʾ�� Organization ���ͭ���뤳�Ȥ�
  # ����롣 SDOSystemElement ��1�İʾ�� Organization ���ͭ���Ƥ�����
  # �ˤϡ����Υ��ڥ졼�����Ͻ�ͭ���� Organization �Υꥹ�Ȥ��֤���
  # �⤷Organization���Ĥ��ͭ���Ƥ��ʤ�����ж��Υꥹ�Ȥ��֤���
  #
  # @param self
  #
  # @return ��ͭ���Ƥ��� Organization �ꥹ��
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  #
  # @else
  #
  # @brief [SDO interface] Getting Organizations
  #
  # SDOSystemElement can be the owner of zero or more organizations.
  # If the SDOSystemElement owns one or more Organizations, this operation
  # returns the list of Organizations that the SDOSystemElement owns.
  # If it does not own any Organization, it returns empty list.
  #
  # @return Owned Organization List
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable if the target SDO is reachable but cannot
  #                         respond.
  # @exception InternalError if the target SDO cannot execute the operation
  #                          completely due to some internal error.
  #
  # @endif
  # virtual SDOPackage::OrganizationList* get_owned_organizations()
  def get_owned_organizations(self):
    self._rtcout.RTC_TRACE("get_owned_organizations()")
    try:
      return self._sdoOwnedOrganizations
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      raise SDOPackage.NotAvailable("NotAvailable: get_owned_organizations")

    return []


  #============================================================
  # SDOPackage::SDO
  #============================================================

  ##
  # @if jp
  # 
  # @brief [SDO interface] SDO ID �μ���
  #
  # SDO ID ���֤����ڥ졼�����
  # ���Υ��ڥ졼�����ϰʲ��η����㳰��ȯ�������롣
  #
  # @param self
  # 
  # @return    �꥽�����ǡ�����ǥ���������Ƥ��� SDO �� ID
  # 
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  #
  # @else
  #
  # @brief [SDO interface] Getting SDO ID
  #
  # This operation returns id of the SDO.
  # This operation throws SDOException with one of the following types.
  #
  # @return    id of the SDO defined in the resource data model.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable if the target SDO is reachable but cannot
  #                         respond.
  # @exception InternalError if the target SDO cannot execute the operation
  #                          completely due to some internal error.
  #
  # @endif
  # virtual char* get_sdo_id()
  def get_sdo_id(self):
    self._rtcout.RTC_TRACE("get_sdo_id()")
    try:
      return self._profile.instance_name
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      raise SDOPackage.InternalError("get_sdo_id()")


  ##
  # @if jp
  # 
  # @brief [SDO interface] SDO �����פμ���
  # 
  # SDO Type ���֤����ڥ졼�����
  # ���Υ��ڥ졼�����ϰʲ��η����㳰��ȯ�������롣
  #
  # @param self
  #
  # @return    �꥽�����ǡ�����ǥ���������Ƥ��� SDO �� Type
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  #
  # @else
  #
  # @brief [SDO interface] Getting SDO type
  #
  # This operation returns sdoType of the SDO.
  # This operation throws SDOException with one of the following types.
  #
  # @return    Type of the SDO defined in the resource data model.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable if the target SDO is reachable but cannot
  #                         respond.
  # @exception InternalError if the target SDO cannot execute the operation
  #                          completely due to some internal error.
  #
  # @endif
  # virtual char* get_sdo_type()
  def get_sdo_type(self):
    self._rtcout.RTC_TRACE("get_sdo_type()")
    try:
      return self._profile.description
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      raise SDOPackage.InternalError("get_sdo_type()")
    return ""


  ##
  # @if jp
  # 
  # @brief [SDO interface] SDO DeviceProfile �ꥹ�Ȥμ��� 
  #
  # SDO �� DeviceProfile ���֤����ڥ졼����� SDO ���ϡ��ɥ������ǥХ���
  # �˴�Ϣ�դ����Ƥ��ʤ����ˤϡ����� DeviceProfile ���֤���롣
  # ���Υ��ڥ졼�����ϰʲ��η����㳰��ȯ�������롣
  #
  # @param self
  #
  # @return    SDO DeviceProfile
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  #
  # @else
  #
  # @brief [SDO interface] Getting SDO DeviceProfile
  #
  # This operation returns the DeviceProfile of the SDO. If the SDO does not
  # represent any hardware device, then a DeviceProfile with empty values
  # are returned.
  # This operation throws SDOException with one of the following types.
  #
  # @return    The DeviceProfile of the SDO.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable if the target SDO is reachable but cannot
  #                         respond.
  # @exception InternalError if the target SDO cannot execute the operation
  #                          completely due to some internal error.
  #
  # @endif
  # virtual SDOPackage::DeviceProfile* get_device_profile()
  def get_device_profile(self):
    self._rtcout.RTC_TRACE("get_device_profile()")
    try:
      return self._SdoConfigImpl.getDeviceProfile()
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      raise SDOPackage.InternalError("get_device_profile()")

    return SDOPackage.DeviceProfile("","","","",[])


  ##
  # @if jp
  # 
  # @brief [SDO interface] SDO ServiceProfile �μ��� 
  #
  # SDO ����ͭ���Ƥ��� Service �� ServiceProfile ���֤����ڥ졼�����
  # SDO �������ӥ����Ĥ��ͭ���Ƥ��ʤ����ˤϡ����Υꥹ�Ȥ��֤���
  # ���Υ��ڥ졼�����ϰʲ��η����㳰��ȯ�������롣
  #
  # @param self
  # 
  # @return    SDO ���󶡤������Ƥ� Service �� ServiceProfile��
  # 
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  #
  # @else
  #
  # @brief [SDO interface] Getting SDO ServiceProfile
  # 
  # This operation returns a list of ServiceProfiles that the SDO has.
  # If the SDO does not provide any service, then an empty list is returned.
  # This operation throws SDOException with one of the following types.
  # 
  # @return    List of ServiceProfiles of all the services the SDO is
  #            providing.
  # 
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable if the target SDO is reachable but cannot
  #                         respond.
  # @exception InternalError if the target SDO cannot execute the operation
  #                          completely due to some internal error.
  #
  # @endif
  # virtual SDOPackage::ServiceProfileList* get_service_profiles()
  def get_service_profiles(self):
    self._rtcout.RTC_TRACE("get_service_profiles()")
    self._sdoSvcProfiles = self._SdoConfigImpl.getServiceProfiles()
    try:
      return self._sdoSvcProfiles
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      raise SDOPackage.InternalError("get_service_profiles()")

    return []


  ##
  # @if jp
  # 
  # @brief [SDO interface] �����ServiceProfile�μ��� 
  #
  # ���� "id" �ǻ��ꤵ�줿̾���Υ����ӥ��� ServiceProfile ���֤���
  # 
  # @param     self
  # @param     _id SDO Service �� ServiceProfile �˴�Ϣ�դ���줿���̻ҡ�
  # 
  # @return    ���ꤵ�줿 SDO Service �� ServiceProfile��
  # 
  # @exception InvalidParameter "id" �ǻ��ꤷ�� ServiceProfile ��¸�ߤ��ʤ���
  #                             "id" �� null��
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  #
  # @else
  #
  # @brief [SDO interface] Getting Organizations
  #
  # This operation returns the ServiceProfile that is specified by the
  # argument "id."
  # 
  # @param     _id The identifier referring to one of the ServiceProfiles.
  # 
  # @return    The profile of the specified service.
  # 
  # @exception InvalidParameter if the ServiceProfile that is specified by 
  #                             the argument 'id' does not exist or if 'id'
  #                             is 'null.'
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable If the target SDO is reachable but cannot
  #                         respond.
  # @exception InternalError If the target SDO cannot execute the operation
  #                          completely due to some internal error.
  #
  # @endif
  # virtual SDOPackage::ServiceProfile* get_service_profile(const char* id)
  def get_service_profile(self, _id):
    self._rtcout.RTC_TRACE("get_service_profile(%s)", _id)
    self._sdoSvcProfiles = self._SdoConfigImpl.getServiceProfiles()
    if not _id:
      raise SDOPackage.InvalidParameter("get_service_profile(): Empty name.")

    try:
      index = OpenRTM_aist.CORBA_SeqUtil.find(self._sdoSvcProfiles, self.svc_name(_id))

      if index < 0:
        raise SDOPackage.InvalidParameter("get_service_profile(): Not found")

      return self._sdoSvcProfiles[index]
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      raise SDOPackage.InternalError("get_service_profile()")

    return SDOPackage.ServiceProfile("", "", [], None)


  ##
  # @if jp
  # 
  # @brief [SDO interface] ���ꤵ�줿 SDO Service �μ���
  #
  # ���Υ��ڥ졼�����ϰ��� "id" �ǻ��ꤵ�줿̾���ˤ�äƶ��̤����
  # SDO �� Service �ؤΥ��֥������Ȼ��Ȥ��֤��� SDO �ˤ���󶡤����
  # Service �Ϥ��줾���դμ��̻Ҥˤ����̤���롣
  #
  # @param self
  # @param _id SDO Service �˴�Ϣ�դ���줿���̻ҡ�
  #
  # @return �׵ᤵ�줿 SDO Service �ؤλ��ȡ�
  #
  # 
  # @exception InvalidParameter "id" �ǻ��ꤷ�� ServiceProfile ��¸�ߤ��ʤ���
  #                             "id" �� null��
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  #
  # @else
  #
  # @brief [SDO interface] Getting specified SDO Service's reference
  #
  # This operation returns an object implementing an SDO's service that
  # is identified by the identifier specified as an argument. Different
  # services provided by an SDO are distinguished with different
  # identifiers. See OMG SDO specification Section 2.2.8, "ServiceProfile,"
  # on page 2-12 for more details.
  #
  # @param _id The identifier referring to one of the SDO Service
  # @return The object implementing the requested service.
  # @exception InvalidParameter if argument ��id�� is null, or if the 
  #                             ServiceProfile that is specified by argument
  #                            ��id�� does not exist.
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable If the target SDO is reachable but cannot
  #                         respond.
  # @exception InternalError If the target SDO cannot execute the operation
  #                          completely due to some internal error.
  #
  # @endif
  # virtual SDOPackage::SDOService_ptr get_sdo_service(const char* id)
  def get_sdo_service(self, _id):
    self._rtcout.RTC_TRACE("get_sdo_service(%s)", _id)
    self._sdoSvcProfiles = self._SdoConfigImpl.getServiceProfiles()

    if not _id:
      raise SDOPackage.InvalidParameter("get_service(): Empty name.")

    index = OpenRTM_aist.CORBA_SeqUtil.find(self._sdoSvcProfiles, self.svc_name(_id))

    if index < 0:
      raise SDOPackage.InvalidParameter("get_service(): Not found")

    try:
      return self._sdoSvcProfiles[index].service
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      raise SDOPackage.InternalError("get_service()")
    return SDOPackage.SDOService._nil


  ##
  # @if jp
  # 
  # @brief [SDO interface] Configuration ���֥������Ȥμ��� 
  #
  # ���Υ��ڥ졼������ Configuration interface �ؤλ��Ȥ��֤���
  # Configuration interface �ϳ� SDO ��������뤿��Υ��󥿡��ե�������
  # �ҤȤĤǤ��롣���Υ��󥿡��ե������� DeviceProfile, ServiceProfile,
  # Organization ��������줿 SDO ��°���ͤ����ꤹ�뤿��˻��Ѥ���롣
  # Configuration ���󥿡��ե������ξܺ٤ˤĤ��Ƥϡ�OMG SDO specification
  # �� 2.3.5��, p.2-24 �򻲾ȤΤ��ȡ�
  #
  # @param self
  #
  # @return SDO �� Configuration ���󥿡��ե������ؤλ���
  #
  # @exception InterfaceNotImplemented SDO��Configuration���󥿡��ե�������
  #                                    �����ʤ���
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  #
  # @else
  #
  # @brief [SDO interface] Getting Configuration object
  #
  # This operation returns an object implementing the Configuration
  # interface. The Configuration interface is one of the interfaces that
  # each SDO maintains. The interface is used to configure the attributes
  # defined in DeviceProfile, ServiceProfile, and Organization.
  # See OMG SDO specification Section 2.3.5, "Configuration Interface,"
  # on page 2-24 for more details about the Configuration interface.
  #
  # @return The Configuration interface of an SDO.
  #
  # @exception InterfaceNotImplemented The target SDO has no Configuration
  #                                    interface.
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  # virtual SDOPackage::Configuration_ptr get_configuration()
  def get_configuration(self):
    self._rtcout.RTC_TRACE("get_configuration()")
    if self._SdoConfig is None:
      raise SODPackage.InterfaceNotImplemented("InterfaceNotImplemented: get_configuration")
    try:
      return self._SdoConfig
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      raise SDOPackage.InternalError("get_configuration()")
    return SDOPackage.Configuration._nil


  ##
  # @if jp
  # 
  # @brief [SDO interface] Monitoring ���֥������Ȥμ��� 
  #
  # ���Υ��ڥ졼������ Monitoring interface �ؤλ��Ȥ��֤���
  # Monitoring interface �� SDO ���������륤�󥿡��ե������ΰ�ĤǤ��롣
  # ���Υ��󥿡��ե������� SDO �Υץ�ѥƥ����˥���󥰤��뤿���
  # ���Ѥ���롣
  # Monitoring interface �ξܺ٤ˤĤ��Ƥ� OMG SDO specification ��
  # 2.3.7�� "Monitoring Interface" p.2-35 �򻲾ȤΤ��ȡ�
  #
  # @param self
  #
  # @return SDO �� Monitoring interface �ؤλ���
  #
  # @exception InterfaceNotImplemented SDO��Configuration���󥿡��ե�������
  #                                    �����ʤ���
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  #
  # @else
  #
  # @brief [SDO interface] Get Monitoring object
  #
  # This operation returns an object implementing the Monitoring interface.
  # The Monitoring interface is one of the interfaces that each SDO
  # maintains. The interface is used to monitor the properties of an SDO.
  # See OMG SDO specification Section 2.3.7, "Monitoring Interface," on
  # page 2-35 for more details about the Monitoring interface.
  #
  # @return The Monitoring interface of an SDO.
  #
  # @exception InterfaceNotImplemented The target SDO has no Configuration
  #                                    interface.
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  # virtual SDOPackage::Monitoring_ptr get_monitoring()
  def get_monitoring(self):
    self._rtcout.RTC_TRACE("get_monitoring()")
    raise SDOPackage.InterfaceNotImplemented("Exception: get_monitoring")
    return SDOPackage.Monitoring._nil


  ##
  # @if jp
  # 
  # @brief [SDO interface] Organization �ꥹ�Ȥμ��� 
  #
  # SDO ��0�İʾ�� Organization (�ȿ�)�˽�°���뤳�Ȥ��Ǥ��롣 �⤷ SDO ��
  # 1�İʾ�� Organization �˽�°���Ƥ����硢���Υ��ڥ졼�����Ͻ�°����
  # Organization �Υꥹ�Ȥ��֤���SDO �� �ɤ� Organization �ˤ��°���Ƥ��ʤ�
  # ���ˤϡ����Υꥹ�Ȥ��֤���롣
  #
  # @param self
  #
  # @return SDO ����°���� Organization �Υꥹ�ȡ�
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  #
  # @brief [SDO interface] Getting Organizations
  #
  # An SDO belongs to zero or more organizations. If the SDO belongs to one
  # or more organizations, this operation returns the list of organizations
  # that the SDO belongs to. An empty list is returned if the SDO does not
  # belong to any Organizations.
  #
  # @return The list of Organizations that the SDO belong to.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  # virtual SDOPackage::OrganizationList* get_organizations()
  def get_organizations(self):
    self._rtcout.RTC_TRACE("get_organizations()")
    self._sdoOrganizations = self._SdoConfigImpl.getOrganizations()
    try:
      return self._sdoOrganizations
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      raise SDOPackage.InternalError("get_organizations()")
    return []


  ##
  # @if jp
  # 
  # @brief [SDO interface] SDO Status �ꥹ�Ȥμ��� 
  #
  # ���Υ��ڥ졼������ SDO �Υ��ơ�������ɽ�� NVList ���֤���
  #
  # @param self
  #
  # @return SDO �Υ��ơ�������
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  #
  # @else
  #
  # @brief [SDO interface] Get SDO Status
  #
  # This operation returns an NVlist describing the status of an SDO.
  #
  # @return The actual status of an SDO.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  #
  # @endif
  # virtual SDOPackage::NVList* get_status_list()
  def get_status_list(self):
    self._rtcout.RTC_TRACE("get_status_list()")
    try:
      return self._sdoStatus
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      raise SDOPackage.InternalError("get_status_list()")
    return []


  ##
  # @if jp
  # 
  # @brief [SDO interface] SDO Status �μ��� 
  #
  # This operation returns the value of the specified status parameter.
  #
  # @param self
  # @param name SDO �Υ��ơ��������������ѥ�᡼����
  # 
  # @return ���ꤵ�줿�ѥ�᡼���Υ��ơ������͡�
  # 
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InvalidParameter ���� "name" �� null ���뤤��¸�ߤ��ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  #
  # @brief [SDO interface] Get SDO Status
  #
  # @param name One of the parameters defining the "status" of an SDO.
  #
  # @return The value of the specified status parameter.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InvalidParameter The parameter defined by "name" is null or
  #                             does not exist.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  #
  #
  # @endif
  # virtual CORBA::Any* get_status(const char* name)
  def get_status(self, name):
    self._rtcout.RTC_TRACE("get_status(%s)", name)
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._sdoStatus, self.nv_name(name))
    if index < 0:
      raise SDOPackage.InvalidParameter("get_status(): Not found")

    try:
      return any.to_any(self._sdoStatus[index].value)
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      raise SDOPackage.InternalError("get_status()")
    return any.to_any("")


  #============================================================
  # Local interfaces
  #============================================================

  ##
  # @if jp
  #
  # @brief [local interface] ���󥹥���̾�μ���
  # 
  # ComponentProfile �����ꤵ�줿���󥹥���̾���֤���
  #
  # @param self
  # 
  # @return ���󥹥���̾
  # 
  # @else
  # 
  # @endif
  # const char* getInstanceName()
  def getInstanceName(self):
    self._rtcout.RTC_TRACE("getInstanceName()")
    return self._profile.instance_name


  ##
  # @if jp
  #
  # @brief [local interface] ���󥹥���̾������
  # 
  # ComponentProfile �˻��ꤵ�줿���󥹥���̾�����ꤹ�롣
  #
  # @param self
  # 
  # @param instance_name ���󥹥���̾
  # 
  # @else
  # 
  # @endif
  # void setInstanceName(const char* instance_name);
  def setInstanceName(self, instance_name):
    self._rtcout.RTC_TRACE("setInstanceName(%s)", instance_name)
    self._properties.setProperty("instance_name",instance_name)
    self._profile.instance_name = self._properties.getProperty("instance_name")


  ##
  # @if jp
  #
  # @brief [local interface] ��̾�μ���
  # 
  # ComponentProfile �����ꤵ�줿��̾���֤���
  #
  # @param self
  # 
  # @return ��̾
  # 
  # @else
  # 
  # @endif
  # const char* getTypeName()
  def getTypeName(self):
    self._rtcout.RTC_TRACE("getTypeName()")
    return self._profile.type_name


  ##
  # @if jp
  #
  # @brief [local interface] Description �μ���
  # 
  # ComponentProfile �����ꤵ�줿 Description ���֤���
  #
  # @param self
  # 
  # @return Description
  # 
  # @else
  # 
  # @endif
  # const char* getDescription()
  def getDescription(self):
    self._rtcout.RTC_TRACE("getDescription()")
    return self._profile.description


  ##
  # @if jp
  #
  # @brief [local interface] �С���������μ���
  # 
  # ComponentProfile �����ꤵ�줿�С�����������֤���
  #
  # @param self
  # 
  # @return �С���������
  # 
  # @else
  # 
  # @endif
  # const char* getVersion()
  def getVersion(self):
    self._rtcout.RTC_TRACE("getVersion()")
    return self._profile.version


  ##
  # @if jp
  #
  # @brief [local interface] �٥��������μ���
  # 
  # ComponentProfile �����ꤵ�줿�٥����������֤���
  #
  # @param self
  # 
  # @return �٥��������
  # 
  # @else
  # 
  # @endif
  # const char* getVendor()
  def getVendor(self):
    self._rtcout.RTC_TRACE("getVendor()")
    return self._profile.vendor


  ##
  # @if jp
  #
  # @brief [local interface] ���ƥ������μ���
  # 
  # ComponentProfile �����ꤵ�줿���ƥ��������֤���
  #
  # @param self
  # 
  # @return ���ƥ������
  # 
  # @else
  # 
  # @endif
  # const char* getCategory()
  def getCategory(self):
    self._rtcout.RTC_TRACE("getCategory()")
    return self._profile.category


  ##
  # @if jp
  #
  # @brief [local interface] Naming Server ����μ���
  # 
  # ���ꤵ�줿 Naming Server ������֤���
  #
  # @param self
  # 
  # @return Naming Server �ꥹ��
  # 
  # @else
  # 
  # @endif
  # std::vector<std::string> getNamingNames();
  def getNamingNames(self):
    self._rtcout.RTC_TRACE("getNamingNames()")
    return [s.strip() for s in self._properties.getProperty("naming.names").split(",")]


  ##
  # @if jp
  #
  # @brief [local interface] ���֥������ȥ�ե���󥹤�����
  # 
  # RTC �� CORBA ���֥������ȥ�ե���󥹤����ꤹ�롣
  # 
  # @param self
  # @param rtobj ���֥������ȥ�ե����
  # 
  # @else
  # 
  # @endif
  # void setObjRef(const RTObject_ptr rtobj);
  def setObjRef(self, rtobj):
    self._rtcout.RTC_TRACE("setObjRef()")
    self._objref = rtobj
    return


  ##
  # @if jp
  #
  # @brief [local interface] ���֥������ȥ�ե���󥹤μ���
  # 
  # ���ꤵ�줿 CORBA ���֥������ȥ�ե���󥹤�������롣
  # 
  # @param self
  # 
  # @return ���֥������ȥ�ե����
  # 
  # @else
  # 
  # @endif
  # RTObject_ptr getObjRef() const;
  def getObjRef(self):
    self._rtcout.RTC_TRACE("getObjRef()")
    return self._objref


  ##
  # @if jp
  # 
  # @brief [local interface] RTC �Υץ�ѥƥ������ꤹ��
  #
  # RTC ���ݻ����٤��ץ�ѥƥ������ꤹ�롣Ϳ������ץ�ѥƥ��ϡ�
  # ComponentProfile �������ꤵ���٤����������ʤ���Фʤ�ʤ���
  # ���Υ��ڥ졼�������̾� RTC ������������ݤ� Manager ����
  # �ƤФ�뤳�Ȥ�տޤ��Ƥ��롣
  # 
  # @param self
  # @param prop RTC �Υץ�ѥƥ�
  #
  # @else
  #
  # @brief [local interface] Set RTC property
  #
  # This operation sets the properties to the RTC. The given property
  # values should include information for ComponentProfile.
  # Generally, this operation is designed to be called from Manager, when
  # RTC is initialized
  #
  # @param prop Property for RTC.
  #
  # @endif
  # void setProperties(const coil::Properties& prop);
  def setProperties(self, prop):
    self._rtcout.RTC_TRACE("setProperties()")
    self._properties.mergeProperties(prop)
    self._profile.instance_name = self._properties.getProperty("instance_name")
    self._profile.type_name     = self._properties.getProperty("type_name")
    self._profile.description   = self._properties.getProperty("description")
    self._profile.version       = self._properties.getProperty("version")
    self._profile.vendor        = self._properties.getProperty("vendor")
    self._profile.category      = self._properties.getProperty("category")


  ##
  # @if jp
  # 
  # @brief [local interface] RTC �Υץ�ѥƥ����������
  #
  # RTC ���ݻ����Ƥ���ץ�ѥƥ����֤���
  # RTC���ץ�ѥƥ�������ʤ����϶��Υץ�ѥƥ����֤���롣
  # 
  # @param self
  # 
  # @return RTC �Υץ�ѥƥ�
  #
  # @else
  #
  # @brief [local interface] Get RTC property
  #
  # This operation returns the properties of the RTC.
  # Empty property would be returned, if RTC has no property.
  #
  # @return Property for RTC.
  #
  # @endif
  # coil::Properties& getProperties();
  def getProperties(self):
    self._rtcout.RTC_TRACE("getProperties()")
    return self._properties


  ##
  # @if jp
  #
  # @brief ����ե�����졼�����ѥ�᡼��������
  # 
  # ����ե�����졼�����ѥ�᡼�����ѿ���Х���ɤ���
  # \<VarType\>�Ȥ��ƥ���ե�����졼�����ѥ�᡼���Υǡ���������ꤹ�롣
  #
  # @param self
  # @param param_name ����ե�����졼�����ѥ�᡼��̾
  # @param var ����ե�����졼�����ѥ�᡼����Ǽ���ѿ�
  # @param def_val ����ե�����졼�����ѥ�᡼���ǥե������
  # @param trans ʸ�����Ѵ��Ѵؿ�(�ǥե������:None)
  #
  # @return ������(��������:true�����꼺��:false)
  # 
  # @else
  #
  # @endif
  #  template <typename VarType>
  #  bool bindParameter(const char* param_name, VarType& var,
  #                     const char* def_val,
  #                     bool (*trans)(VarType&, const char*) = coil::stringTo)
  def bindParameter(self, param_name, var,
                    def_val, trans=None):
    self._rtcout.RTC_TRACE("bindParameter()")
    if trans is None:
      trans_ = OpenRTM_aist.stringTo
    else:
      trans_ = trans
    self._configsets.bindParameter(param_name, var, def_val, trans_)
    return True


  ##
  # @if jp
  #
  # @brief ����ե�����졼�����ѥ�᡼���ι���(ID����)
  # 
  # ���ꤷ��ID�Υ���ե�����졼����󥻥åȤ����ꤷ���ͤǡ�
  # ����ե�����졼�����ѥ�᡼�����ͤ򹹿�����
  #
  # @param self
  # @param config_set �����оݤΥ���ե�����졼����󥻥å�ID
  # 
  # @else
  #
  # @endif
  # void updateParameters(const char* config_set);
  def updateParameters(self, config_set):
    self._rtcout.RTC_TRACE("updateParameters(%s)", config_set)
    self._configsets.update(config_set)
    return


  ##
  # @if jp
  # 
  # @brief [local interface] Port ����Ͽ����
  #
  # RTC ���ݻ�����Port����Ͽ���롣
  # Port �������饢��������ǽ�ˤ��뤿��ˤϡ����Υ��ڥ졼�����ˤ��
  # ��Ͽ����Ƥ��ʤ���Фʤ�ʤ�����Ͽ����� Port �Ϥ��� RTC �����ˤ�����
  # PortProfile.name �ˤ����̤���롣�������äơ�Port �� RTC ��ˤ����ơ�
  # ��ˡ����� PortProfile.name ������ʤ���Фʤ�ʤ���
  # ��Ͽ���줿 Port ��������Ŭ�ڤ˥����ƥ��ֲ����줿�塢���λ��Ȥ�
  # ���֥������Ȼ��Ȥ��ꥹ�������¸����롣
  # 
  # @param self
  # @param port RTC ����Ͽ���� Port
  # @param port_type if port is PortBase, port_type is None,
  #                  if port is PortService, port_type is True
  #
  # @else
  #
  # @brief [local interface] Register Port
  #
  # This operation registers a Port to be held by this RTC.
  # In order to enable access to the Port from outside of RTC, the Port
  # must be registered by this operation. The Port that is registered by
  # this operation would be identified by PortProfile.name in the inside of
  # RTC. Therefore, the Port should have unique PortProfile.name in the RTC.
  # The registering Port would be activated properly, and the reference
  # and the object reference would be stored in lists in RTC.
  #
  # @param port Port which is registered in the RTC
  #
  # @endif
  # void registerPort(PortBase& port);
  def registerPort(self, port):
    self._rtcout.RTC_TRACE("registerPort()")
    if not self.addPort(port):
      self._rtcout.RTC_ERROR("addPort(PortBase&) failed.")
    return

  # void registerPort(PortService_ptr port);
  # def registerPortByReference(self, port_ref):
  #   self._rtcout.RTC_TRACE("registerPortByReference()")
  #   self.addPortByReference(port_ref)
  #   return

  # new interface. since 1.0.0-RELEASE
  # void addPort(PortBase& port);
  def addPort(self, port):
    self._rtcout.RTC_TRACE("addPort()")
    if isinstance(port, OpenRTM_aist.CorbaPort):
      self._rtcout.RTC_TRACE("addPort(CorbaPort)")
      propkey = "port.corbaport."
      prop = self._properties.getNode(propkey)
      if prop:
        self._properties.getNode(propkey).mergeProperties(self._properties.getNode("port.corba"))
      port.init(self._properties.getNode(propkey))
      port.setOwner(self.getObjRef())

    elif isinstance(port, OpenRTM_aist.PortBase):
      self._rtcout.RTC_TRACE("addPort(PortBase)")
      port.setOwner(self.getObjRef())
      port.setPortConnectListenerHolder(self._portconnListeners)
      self.onAddPort(port.getPortProfile())

    elif isinstance(port, RTC._objref_PortService):
      self._rtcout.RTC_TRACE("addPort(PortService)")
    return self._portAdmin.addPort(port)


  # new interface. since 1.0.0-RELEASE
  # void addPort(PortService_ptr port);
  # def addPortByReference(self, port_ref):
  #   self._rtcout.RTC_TRACE("addPortByReference()")
  #   self._portAdmin.registerPortByReference(port_ref)
  #   return
    

  ##
  # @if jp
  # 
  # @brief [local interface] DataInPort ����Ͽ����
  #
  # RTC ���ݻ����� DataInPort ����Ͽ���롣
  # Port �Υץ�ѥƥ��˥ǡ����ݡ��ȤǤ��뤳��("port.dataport")��
  # TCP����Ѥ��뤳��("tcp_any")�����ꤹ��ȤȤ�ˡ� DataInPort ��
  # ���󥹥��󥹤�����������Ͽ���롣
  # 
  # @param self
  # @param name port ̾��
  # @param inport ��Ͽ�о� DataInPort
  #
  # @else
  #
  # @endif
  def registerInPort(self, name, inport):
    self._rtcout.RTC_TRACE("registerInPort(%s)", name)
    if not self.addInPort(name, inport):
      self._rtcout.RTC_ERROR("addInPort(%s) failed.", name)
    return

  # new interface. since 1.0.0-RELEASE
  def addInPort(self, name, inport):
    self._rtcout.RTC_TRACE("addInPort(%s)", name)

    propkey = "port.inport." + name
    prop_ = copy.copy(self._properties.getNode(propkey))
    prop_.mergeProperties(self._properties.getNode("port.inport.dataport"))

    ret = self.addPort(inport)

    if not ret:
      self._rtcout.RTC_ERROR("addInPort() failed.")
      return ret
      
    inport.init(self._properties.getNode(propkey))
    self._inports.append(inport)
    return ret


  ##
  # @if jp
  # 
  # @brief [local interface] DataOutPort ����Ͽ����
  #
  # RTC ���ݻ����� DataOutPor t����Ͽ���롣
  # Port �Υץ�ѥƥ��˥ǡ����ݡ��ȤǤ��뤳��("port.dataport")��
  # TCP����Ѥ��뤳��("tcp_any")�����ꤹ��ȤȤ�ˡ� DataOutPort ��
  # ���󥹥��󥹤�����������Ͽ���롣
  # 
  # @param self
  # @param name port ̾��
  # @param outport ��Ͽ�о� DataInPort
  #
  # @else
  #
  # @endif
  # void registerOutPort(const char* name, OutPortBase& outport);
  def registerOutPort(self, name, outport):
    self._rtcout.RTC_TRACE("registerOutPort(%s)", name)
    if not self.addOutPort(name, outport):
      self._rtcout.RTC_ERROR("addOutPort(%s) failed.", name)
    return

  # new interface. since 1.0.0-RELEASE
  # void addOutPort(const char* name, OutPortBase& outport);
  def addOutPort(self, name, outport):
    self._rtcout.RTC_TRACE("addOutPort(%s)", name)

    propkey = "port.outport." + name
    prop_ = copy.copy(self._properties.getNode(propkey))
    prop_.mergeProperties(self._properties.getNode("port.outport.dataport"))

    ret = self.addPort(outport)

    if not ret:
      self._rtcout.RTC_ERROR("addOutPort() failed.")
      return ret

    outport.init(self._properties.getNode(propkey))
    self._outports.append(outport)
    return ret


  ##
  # @if jp
  # 
  # @brief [local interface] InPort ����Ͽ��������
  #
  # RTC ���ݻ�����InPort����Ͽ�������롣
  # 
  # @param port ����о� Port
  # @return ������(�������:true���������:false)
  #
  # @else
  #
  # @brief [local interface] Unregister InPort
  #
  # This operation unregisters a InPort held by this RTC.
  #
  # @param port Port which is unregistered
  # @return Unregister result (Successful:true, Failed:false)
  #
  # @endif
  #
  # bool removeInPort(InPortBase& port);
  def removeInPort(self, port):
    self._rtcout.RTC_TRACE("removeInPort()")
    ret = self.removePort(inport)

    if ret:
      for inport in self._inports:
        if port == inport:
          try:
            self._inports.remove(port)
          except:
            self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
            
          return True

    return False


  ##
  # @if jp
  # 
  # @brief [local interface] OutPort ����Ͽ��������
  #
  # RTC ���ݻ�����OutPort����Ͽ�������롣
  # 
  # @param port ����о� Port
  # @return ������(�������:true���������:false)
  #
  # @else
  #
  # @brief [local interface] Unregister OutPort
  #
  # This operation unregisters a OutPort held by this RTC.
  #
  # @param port Port which is unregistered
  # @return Unregister result (Successful:true, Failed:false)
  #
  # @endif
  #
  # bool removeOutPort(OutPortBase& port);
  def removeOutPort(self, port):
    self._rtcout.RTC_TRACE("removeOutPort()")
    ret = self.removePort(outport)

    if ret:
      for outport in self._outports:
        if port == outport:
          try:
            self._outports.remove(port)
          except:
            self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
            
          return True

    return False


  ##
  # @if jp
  # 
  # @brief [local interface] Port ����Ͽ��������
  #
  # RTC ���ݻ�����Port����Ͽ�������롣
  # 
  # @param self
  # @param port ����о� Port
  #
  # @else
  #
  # @brief [local interface] Unregister Port
  #
  # This operation unregisters a Port to be held by this RTC.
  #
  # @param port Port which is unregistered in the RTC
  #
  # @endif
  # void RTObject_impl::deletePort(PortBase& port)
  def deletePort(self, port):
    self._rtcout.RTC_TRACE("deletePort()")
    if not self.removePort(port):
      self._rtcout.RTC_ERROR("removePort() failed.")
    return

  # new interface. since 1.0.0-RELEASE
  def removePort(self, port):
    self._rtcout.RTC_TRACE("removePort()")
    if isinstance(port, OpenRTM_aist.PortBase) or isinstance(port, OpenRTM_aist.CorbaPort):
      self.onRemovePort(port.getPortProfile())
    return self._portAdmin.removePort(port)


  ##
  # @if jp
  # 
  # @brief [local interface] ̾������ˤ�� Port ����Ͽ��������
  #
  # ̾�Τ���ꤷ�� RTC ���ݻ�����Port����Ͽ�������롣
  # 
  # @param self
  # @param port_name ����о� Port ̾
  #
  # @else
  #
  # @endif
  def deletePortByName(self, port_name):
    self._rtcout.RTC_TRACE("deletePortByName(%s)", port_name)
    self._portAdmin.deletePortByName(port_name)
    return


  ##
  # @if jp
  #
  # @brief [local interface] �¹ԥ���ƥ����Ȥ��������
  #
  # get_context() ��Ʊ����ǽ�Υ������ǡ��㤤�Ϥʤ���
  # ���δؿ��ϰʲ��δؿ���ǸƤФ�뤳�Ȥ�����Ȥ��Ƥ��롣
  #
  # - onStartup()
  # - onShutdown()
  # - onActivated()
  # - onDeactivated()
  # - onExecute()
  # - onAborting()
  # - onError()
  # - onReset()
  # - onStateUpdate()
  # - onRateChanged()
  # 
  # ���δؿ��ΰ����Ϥ����δؿ��ΰ��� UniquieID exec_handle �Ǥʤ�
  # ��Фʤ�ʤ���
  # 
  # @param ec_id �嵭�ؿ�����1���� exec_handle ���Ϥ�ɬ�פ����롣
  # 
  # @else
  # 
  # @brief [local interface] Getting current execution context
  # 
  # This function is the local version of get_context(). completely
  # same as get_context() function. This function is assumed to be
  # called from the following functions.
  # 
  # - onStartup()
  # - onShutdown()
  # - onActivated()
  # - onDeactivated()
  # - onExecute()
  # - onAborting()
  # - onError()
  # - onReset()
  # - onStateUpdate()
  # - onRateChanged()
  # 
  # The argument of this function should be the first argument
  # (UniqueId ec_id) of the above functions.
  # 
  # @param ec_id The above functions' first argument "exec_handle."
  # 
  # @endif
  #
  # ExecutionContext_ptr getExecutionContext(RTC::UniqueId ec_id);
  def getExecutionContext(self, ec_id):
    return self.get_context(ec_id)

  ##
  # @if jp
  # 
  # @brief [local interface] �¹ԥ���ƥ����Ȥμ¹ԥ졼�Ȥ��������
  #
  # ���߼¹���μ¹ԥ���ƥ����Ȥμ¹ԥ졼�Ȥ�������롣�¹ԥ���ƥ�
  # ���Ȥ�Kind��PERIODIC�ʳ��ξ���ư���̤����Ǥ��롣���δؿ��ϰ�
  # ���δؿ���ǸƤФ�뤳�Ȥ�����Ȥ��Ƥ��롣
  #
  # - onStartup()
  # - onShutdown()
  # - onActivated()
  # - onDeactivated()
  # - onExecute()
  # - onAborting()
  # - onError()
  # - onReset()
  # - onStateUpdate()
  # - onRateChanged()
  #
  # ���δؿ��ΰ����Ϥ����δؿ��ΰ��� UniquieID exec_handle �Ǥʤ�
  # ��Фʤ�ʤ���
  #
  # @param ec_id �嵭�ؿ�����1���� exec_handle ���Ϥ�ɬ�פ����롣
  #
  # @else
  # 
  # @brief [local interface] Getting current context' execution rate
  #
  # This function returns current execution rate in this
  # context. If this context's kind is not PERIODC, behavior is not
  # defined. This function is assumed to be called from the
  # following functions.
  #
  # - onStartup()
  # - onShutdown()
  # - onActivated()
  # - onDeactivated()
  # - onExecute()
  # - onAborting()
  # - onError()
  # - onReset()
  # - onStateUpdate()
  # - onRateChanged()
  #
  # The argument of this function should be the first argument
  # (UniqueId ec_id) of the above functions.
  #
  # @param ec_id The above functions' first argument "exec_handle."
  #
  # @endif
  #
  # double getExecutionRate(RTC::UniqueId ec_id);
  def getExecutionRate(self, ec_id):
    ec = self.getExecutionContext(ec_id)
    if CORBA.is_nil(ec):
      return 0.0

    return ec.get_rate()


  ##
  # @if jp
  # 
  # @brief [local interface] �¹ԥ���ƥ����Ȥμ¹ԥ졼�Ȥ����ꤹ��
  #
  # ���߼¹���μ¹ԥ���ƥ����Ȥμ¹ԥ졼�Ȥ����ꤹ�롣�¹ԥ���ƥ�
  # ���Ȥ�Kind��PERIODIC�ʳ��ξ���ư���̤����Ǥ��롣���δؿ��ϰ�
  # ���δؿ���ǸƤФ�뤳�Ȥ�����Ȥ��Ƥ��롣
  #
  # - onStartup()
  # - onShutdown()
  # - onActivated()
  # - onDeactivated()
  # - onExecute()
  # - onAborting()
  # - onError()
  # - onReset()
  # - onStateUpdate()
  # - onRateChanged()
  #
  # ���δؿ��ΰ����Ϥ����δؿ��ΰ��� UniquieID exec_handle �Ǥʤ�
  # ��Фʤ�ʤ���
  #
  # @param ec_id �嵭�ؿ�����1���� exec_handle ���Ϥ�ɬ�פ����롣
  # @param rate �¹ԥ졼�Ȥ� [Hz] ��Ϳ����
  #
  # @else
  # 
  # @brief [local interface] Setting current context' execution rate
  #
  # This function sets a execution rate in the context. If this
  # context's kind is not PERIODC, behavior is not defined. This
  # function is assumed to be called from the following functions.
  #
  # - onStartup()
  # - onShutdown()
  # - onActivated()
  # - onDeactivated()
  # - onExecute()
  # - onAborting()
  # - onError()
  # - onReset()
  # - onStateUpdate()
  # - onRateChanged()
  #
  # The argument of this function should be the first argument
  # (UniqueId ec_id) of the above functions.
  #
  # @param ec_id The above functions' first argument "exec_handle."
  # @param rate Execution rate in [Hz].
  #
  # @endif
  #
  # ReturnCode_t setExecutionRate(RTC::UniqueId ec_id, double rate);
  def setExecutionRate(self, ec_id, rate):
    ec = self.getExecutionContext(ec_id)
    if CORBA.is_nil(ec):
      return RTC.RTC_ERROR
    ec.set_rate(rate)
    return RTC.RTC_OK


  ##
  # @if jp
  # 
  # @brief [local interface] �¹ԥ���ƥ����Ȥν�ͭ����Ĵ�٤�
  #
  # ���߼¹���μ¹ԥ���ƥ����Ȥν�ͭ����Ĵ�٤롣���δؿ��ϰʲ��δ�
  # ����ǸƤФ�뤳�Ȥ�����Ȥ��Ƥ��롣
  #
  # - onStartup()
  # - onShutdown()
  # - onActivated()
  # - onDeactivated()
  # - onExecute()
  # - onAborting()
  # - onError()
  # - onReset()
  # - onStateUpdate()
  # - onRateChanged()
  #
  # ���δؿ��ΰ����Ϥ����δؿ��ΰ��� UniquieID exec_handle �Ǥʤ�
  # ��Фʤ�ʤ���
  #
  # @param ec_id �嵭�ؿ�����1���� exec_handle ���Ϥ�ɬ�פ����롣
  # @return true: ���Ȥμ¹ԥ���ƥ����ȡ�false: ¾�μ¹ԥ���ƥ�����
  #
  # @else
  # 
  # @brief [local interface] Checking if the current context is own context
  #
  # This function checks if the current context is own execution
  # context. This function is assumed to be called from the
  # following functions.
  #
  # - onStartup()
  # - onShutdown()
  # - onActivated()
  # - onDeactivated()
  # - onExecute()
  # - onAborting()
  # - onError()
  # - onReset()
  # - onStateUpdate()
  # - onRateChanged()
  #
  # The argument of this function should be the first argument
  # (UniqueId ec_id) of the above functions.
  #
  # @param ec_id The above functions' first argument "exec_handle."
  # @return true: Own context, false: other's context
  #
  # @endif
  #
  # bool isOwnExecutionContext(RTC::UniqueId ec_id);
  def isOwnExecutionContext(self, ec_id):
    global ECOTHER_OFFSET
    if ec_id < ECOTHER_OFFSET:
      return True
    return False


  ##
  # @if jp
  # 
  # @brief [local interface] ���֤� Inactive �����ܤ�����
  #
  # ���֤� Active ���� Inactive �����ܤ����롣���δؿ��ϰʲ��δ�
  # ����ǸƤФ�뤳�Ȥ�����Ȥ��Ƥ��롣
  #
  # - onActivated()
  # - onExecute()
  # - onStateUpdate()
  #
  # ���δؿ��ΰ����Ͼ嵭�δؿ��ΰ��� UniquieID exec_handle �Ǥʤ�
  # ��Фʤ�ʤ���
  #
  # @param ec_id �嵭�ؿ�����1���� exec_handle ���Ϥ�ɬ�פ����롣
  # @return �꥿���󥳡���
  #
  # @else
  # 
  # @brief [local interface] Make transition to Inactive state
  #
  # This function makes transition from Active to Inactive
  # state. This function is assumed to be called from the following
  # functions.
  #
  # - onActivated()
  # - onExecute()
  # - onStateUpdate()
  #
  # The argument of this function should be the first argument
  # (UniqueId ec_id) of the above function.
  #
  # @param ec_id The above functions' first argument "exec_handle."
  # @return Return code
  #
  # @endif
  #
  # ReturnCode_t deactivate(RTC::UniqueId ec_id);
  def deactivate(self, ec_id):
    ec = self.getExecutionContext(ec_id)
    if CORBA.is_nil(ec):
      return RTC.RTC_ERROR
    return ec.deactivate_component(self.getObjRef())


  ##
  # @if jp
  # 
  # @brief [local interface] ���֤� Active �����ܤ�����
  #
  # ���֤� Inactive ���� Active �����ܤ����롣���δؿ��ϰʲ��δ�
  # ����ǸƤФ�뤳�Ȥ�����Ȥ��Ƥ��롣
  #
  # - onStartup()
  # - onDeactivated()
  #
  # ���δؿ��ΰ����Ͼ嵭�δؿ��ΰ��� UniquieID exec_handle �Ǥʤ�
  # ��Фʤ�ʤ���
  #
  # @param ec_id �嵭�ؿ�����1���� exec_handle ���Ϥ�ɬ�פ����롣
  # @return �꥿���󥳡���
  #
  # @else
  # 
  # @brief [local interface] Make transition to Active state
  #
  # This function makes transition from Inactive to Active
  # state. This function is assumed to be called from the following
  # functions.
  #
  # - onStartup()
  # - onDeactivated()
  #
  # The argument of this function should be the first argument
  # (UniqueId ec_id) of the above function.
  #
  # @param ec_id The above functions' first argument "exec_handle."
  # @return Return code
  #
  # @endif
  #
  # ReturnCode_t activate(RTC::UniqueId ec_id);
  def activate(self, ec_id):
    ec = self.getExecutionContext(ec_id)
    if CORBA.is_nil(ec):
      return RTC.RTC_ERROR
    return ec.activate_component(self.getObjRef())


  ##
  # @if jp
  # 
  # @brief [local interface] ���֤�ꥻ�åȤ� Inactive �����ܤ�����
  #
  # ���֤� Error ���� Inactive �����ܤ����롣���δؿ��ϰʲ��δ�
  # ����ǸƤФ�뤳�Ȥ�����Ȥ��Ƥ��롣
  #
  # - onError()
  #
  # ���δؿ��ΰ����Ͼ嵭�δؿ��ΰ��� UniquieID exec_handle �Ǥʤ�
  # ��Фʤ�ʤ���
  #
  # @param ec_id �嵭�ؿ�����1���� exec_handle ���Ϥ�ɬ�פ����롣
  # @return �꥿���󥳡���
  #
  # @else
  # 
  # @brief [local interface] Resetting and go to Inactive state
  #
  # This function reset RTC and makes transition from Error to Inactive
  # state. This function is assumed to be called from the following
  # functions.
  #
  # - onError()
  #
  # The argument of this function should be the first argument
  # (UniqueId ec_id) of the above function.
  #
  # @param ec_id The above functions' first argument "exec_handle."
  # @return Return code
  #
  # @endif
  #
  # ReturnCode_t reset(RTC::UniqueId ec_id);
  def reset(self, ec_id):
    ec = self.getExecutionContext(ec_id)
    if CORBA.is_nil(ec):
      return RTC.RTC_ERROR
    return ec.reset_component(self.getObjRef())
    

  ##
  # @if jp
  # @brief [local interface] SDO service provider �򥻥åȤ���
  # @else
  # @brief [local interface] Set a SDO service provider
  # @endif
  #
  # bool addSdoServiceProvider(const SDOPackage::ServiceProfile& prof,
  #                            SdoServiceProviderBase* provider);
  def addSdoServiceProvider(self, prof, provider):
    return self._sdoservice.addSdoServiceProvider(prof, provider)


  ##
  # @if jp
  # @brief [local interface] SDO service provider ��������
  # @else
  # @brief [local interface] Remove a SDO service provider
  # @endif
  #
  # bool removeSdoServiceProvider(const char* id);
  def removeSdoServiceProvider(self, id):
    return self._sdoservice.removeSdoServiceProvider(id)


  ##
  # @if jp
  # @brief [local interface] SDO service consumer �򥻥åȤ���
  # @else
  # @brief [local interface] Set a SDO service consumer
  # @endif
  #
  # bool addSdoServiceConsumer(const SDOPackage::ServiceProfile& prof);
  def addSdoServiceConsumer(self, prof):
    return self._sdoservice.addSdoServiceConsumer(prof)


  ##
  # @if jp
  # @brief [local interface] SDO service consumer ��������
  # @else
  # @brief [local interface] Remove a SDO service consumer
  # @endif
  #
  # bool removeSdoServiceConsumer(const char* id);
  def removeSdoServiceConsumer(self, id):
    return self._sdoservice.removeSdoServiceConsumer(id)


  ##
  # @if jp
  #
  # @brief �� InPort �Υǡ������ɤ߹��ࡣ
  #
  # RTC ���ݻ��������Ƥ� InPort �Υǡ������ɤ߹��ࡣ
  #
  # @return �ɤ߹��߷��(���ݡ��Ȥ��ɤ߹�������:true������:false)
  #
  # @else
  #
  # @brief Readout the value from All InPorts.
  #
  # This operation read the value from all InPort
  # registered in the RTC.
  #
  # @return result (Successful:true, Failed:false)
  #
  # @endif
  #
  # bool readAll();
  def readAll(self):
    self._rtcout.RTC_TRACE("readAll()")
    ret = True
    for inport in self._inports:
      if not inport.read():
        self._rtcout.RTC_DEBUG("The error occurred in readAll().")
        ret = False
        if not self._readAllCompletion:
          return False

    return ret


  ##
  # @if jp
  #
  # @brief �� OutPort ��write()�᥽�åɤ򥳡��뤹�롣
  #
  # RTC ���ݻ��������Ƥ� OutPort ��write()�᥽�åɤ򥳡��뤹�롣
  #
  # @return �ɤ߹��߷��(���ݡ��Ȥؤν񤭹�������:true������:false)
  #
  # @else
  #
  # @brief The write() method of all OutPort is called. 
  #
  # This operation call the write() method of all OutPort
  # registered in the RTC.
  #
  # @return result (Successful:true, Failed:false)
  #
  # @endif
  #
  # bool writeAll();
  def writeAll(self):
    self._rtcout.RTC_TRACE("writeAll()")
    ret = True
    for outport in self._outports:
      if not outport.write():
        self._rtcout.RTC_DEBUG("The error occurred in writeAll().")
        ret = False
        if not self._writeAllCompletion:
          return False

    return ret


  ##
  # @if jp
  #
  # @brief onExecute()�¹����Ǥ�readAll()�᥽�åɤθƽФ�ͭ���ޤ���̵���ˤ��롣
  #
  # ���Υ᥽�åɤ�ѥ�᡼����true�Ȥ��ƸƤֻ��ˤ�ꡢonExecute()�¹�����
  # readAll()���ƽФ����褦�ˤʤ롣
  # �ѥ�᡼����false�ξ��ϡ�readAll()�ƽФ�̵���ˤ��롣
  #
  # @param read(default:true) 
  #        (readAll()�᥽�åɸƽФ���:true, readAll()�᥽�åɸƽФʤ�:false)
  #
  # @param completion(default:false) 
  #    readAll()�ˤơ��ɤ줫�ΰ�Ĥ�InPort��read()�����Ԥ��Ƥ����Ƥ�InPort��read()��ƤӽФ�:true,
  #    readAll()�ˤơ��ɤ줫�ΰ�Ĥ�InPort��read()�����Ԥ�����硢������false��ȴ����:false
  #
  # @else
  #
  # @brief Set whether to execute the readAll() method. 
  #
  # Set whether to execute the readAll() method. 
  #
  # @param read(default:true)
  #        (readAll() is called:true, readAll() isn't called:false)
  #
  # @param completion(default:false)
  #     All InPort::read() calls are completed.:true,
  #     If one InPort::read() is False, return false.:false
  #
  # @param completion(default:false)
  #
  # @endif
  #
  # void setReadAll(bool read=true, bool completion=false);
  def setReadAll(self, read=True, completion=False):
    self._readAll = read
    self._readAllCompletion = completion


  ##
  # @if jp
  #
  # @brief onExecute()�¹Ը��writeAll()�᥽�åɤθƽФ�ͭ���ޤ���̵���ˤ��롣
  #
  # ���Υ᥽�åɤ�ѥ�᡼����true�Ȥ��ƸƤֻ��ˤ�ꡢonExecute()�¹Ը��
  # writeAll()���ƽФ����褦�ˤʤ롣
  # �ѥ�᡼����false�ξ��ϡ�writeAll()�ƽФ�̵���ˤ��롣
  #
  # @param write(default:true) 
  #        (writeAll()�᥽�åɸƽФ���:true, writeAll()�᥽�åɸƽФʤ�:false)
  #
  # @param completion(default:false) 
  #    writeAll()�ˤơ��ɤ줫�ΰ�Ĥ�OutPort��write()�����Ԥ��Ƥ����Ƥ�OutPort��write()��ƤӽФ���Ԥ�:true,
  #    writeAll()�ˤơ��ɤ줫�ΰ�Ĥ�OutPort��write()�����Ԥ�����硢������false��ȴ����:false
  #
  # @else
  #
  # @brief Set whether to execute the writeAll() method. 
  #
  # Set whether to execute the writeAll() method. 
  #
  # @param write(default:true)
  #        (writeAll() is called:true, writeAll() isn't called:false)
  #
  # @param completion(default:false)
  #     All OutPort::write() calls are completed.:true,
  #     If one OutPort::write() is False, return false.:false
  #
  # @endif
  #
  # void setWriteAll(bool write=true, bool completion=false);
  def setWriteAll(self, write=True, completion=False):
    self._writeAll = write
    self._writeAllCompletion = completion


  ##
  # @if jp
  #
  # @brief �� Port ����Ͽ��������
  #
  # RTC ���ݻ��������Ƥ� Port �������롣
  # 
  # @param self
  #
  # @else
  #
  # @brief Unregister the All Portse
  #
  # This operation deactivates the all Port and deletes the all Port's
  # registrations in the RTC..
  #
  # @endif
  def finalizePorts(self):
    self._rtcout.RTC_TRACE("finalizePorts()")
    self._portAdmin.finalizePorts()
    self._inports = []
    self._outports = []
    return


  def finalizeContexts(self):
    self._rtcout.RTC_TRACE("finalizeContexts()")
    len_ = len(self._eclist)
    for i in range(len_):
      idx = (len_ - 1) - i
      self._eclist[idx].stop()
      try:
        self._poa.deactivate_object(self._poa.servant_to_id(self._eclist[idx]))
      except:
        self._rtcout.RTC_TRACE(OpenRTM_aist.Logger.print_exception())
      del self._eclist[idx]

    if self._eclist:
      self._eclist = []
    return


  ##
  # @if jp
  # @brief PreComponentActionListener �ꥹ�ʤ��ɲä���
  #
  # ComponentAction �����ؿ��θƤӽФ�ľ���Υ��٥�Ȥ˴�Ϣ����Ƽ��
  # ���ʤ����ꤹ�롣
  #
  # ����Ǥ���ꥹ�ʤΥ����פȥ�����Хå����٥�Ȥϰʲ����̤�
  #
  # - PRE_ON_INITIALIZE:    onInitialize ľ��
  # - PRE_ON_FINALIZE:      onFinalize ľ��
  # - PRE_ON_STARTUP:       onStartup ľ��
  # - PRE_ON_SHUTDOWN:      onShutdown ľ��
  # - PRE_ON_ACTIVATED:     onActivated ľ��
  # - PRE_ON_DEACTIVATED:   onDeactivated ľ��
  # - PRE_ON_ABORTING:       onAborted ľ��
  # - PRE_ON_ERROR:         onError ľ��
  # - PRE_ON_RESET:         onReset ľ��
  # - PRE_ON_EXECUTE:       onExecute ľ��
  # - PRE_ON_STATE_UPDATE:  onStateUpdate ľ��
  #
  # �ꥹ�ʤ� PreComponentActionListener ��Ѿ������ʲ��Υ����˥�������
  # operator() ��������Ƥ���ɬ�פ����롣
  #
  # PreComponentActionListener::operator()(UniqueId ec_id)
  #
  # �ǥե���ȤǤϡ����δؿ���Ϳ�����ꥹ�ʥ��֥������Ȥν�ͭ����
  # RTObject�˰ܤꡢRTObject���λ��⤷���ϡ�
  # removePreComponentActionListener() �ˤ�������˼�ưŪ�˲��Τ���롣
  # �ꥹ�ʥ��֥������Ȥν�ͭ����ƤӽФ�¦�ǰݻ����������ϡ���3��
  # ���� false ����ꤷ����ưŪ�ʲ��Τ��������뤳�Ȥ��Ǥ��롣
  #
  # @param listener_type �ꥹ�ʥ�����
  # @param memfunc �ؿ����֥�������
  # @param autoclean �ꥹ�ʥ��֥������Ȥμ�ưŪ���Τ�Ԥ����ɤ����Υե饰
  #
  # @else
  # @brief Adding PreComponentAction type listener
  #
  # This operation adds certain listeners related to ComponentActions
  # pre events.
  # The following listener types are available.
  #
  # - PRE_ON_INITIALIZE:    before onInitialize
  # - PRE_ON_FINALIZE:      before onFinalize
  # - PRE_ON_STARTUP:       before onStartup
  # - PRE_ON_SHUTDOWN:      before onShutdown
  # - PRE_ON_ACTIVATED:     before onActivated
  # - PRE_ON_DEACTIVATED:   before onDeactivated
  # - PRE_ON_ABORTING:       before onAborted
  # - PRE_ON_ERROR:         before onError
  # - PRE_ON_RESET:         before onReset
  # - PRE_ON_EXECUTE:       before onExecute
  # - PRE_ON_STATE_UPDATE:  before onStateUpdate
  #
  # Listeners should have the following function operator().
  #
  # PreComponentActionListener::operator()(UniqueId ec_id)
  #
  # The ownership of the given listener object is transferred to
  # this RTObject object in default.  The given listener object will
  # be destroied automatically in the RTObject's dtor or if the
  # listener is deleted by removePreComponentActionListener() function.
  # If you want to keep ownership of the listener object, give
  # "false" value to 3rd argument to inhibit automatic destruction.
  #
  # @param listener_type A listener type
  # @param memfunc  member function object
  # @param autoclean A flag for automatic listener destruction
  #
  # @endif
  #
  # template <class Listener>
  # PreComponentActionListener*
  # addPreComponentActionListener(PreCompActionListenerType listener_type,
  #                               void (Listener::*memfunc)(UniqueId ec_id),
  #                               bool autoclean = true)
  def addPreComponentActionListener(self, listener_type,
                                    memfunc, autoclean = True):
    class Noname(OpenRTM_aist.PreComponentActionListener):
      def __init__(self, memfunc):
        self._memfunc = memfunc

      def __call__(self, ec_id):
        self._memfunc(ec_id)
        return

    listener = Noname(memfunc)
    self._actionListeners.preaction_[listener_type].addListener(listener, autoclean)
    return listener


  ##
  # @if jp
  # @brief PreComponentActionListener �ꥹ�ʤ�������
  #
  # ���ꤷ���Ƽ�ꥹ�ʤ������롣
  # 
  # @param listener_type �ꥹ�ʥ�����
  # @param listener �ꥹ�ʥ��֥������ȤؤΥݥ���
  #
  # @else
  # @brief Removing PreComponentAction type listener
  #
  # This operation removes a specified listener.
  #     
  # @param listener_type A listener type
  # @param listener A pointer to a listener object
  #
  # @endif
  #
  # void 
  # removePreComponentActionListener(PreComponentActionListenerType listener_type,
  #                                  PreComponentActionListener* listener);
  def removePreComponentActionListener(self, listener_type, listener):
    self._actionListeners.preaction_[listener_type].removeListener(listener)
    return


  ##
  # @if jp
  # @brief PostComponentActionListener �ꥹ�ʤ��ɲä���
  #
  # ComponentAction �����ؿ��θƤӽФ�ľ��Υ��٥�Ȥ˴�Ϣ����Ƽ��
  # ���ʤ����ꤹ�롣
  #
  # ����Ǥ���ꥹ�ʤΥ����פȥ�����Хå����٥�Ȥϰʲ����̤�
  #
  # - POST_ON_INITIALIZE:    onInitialize ľ��
  # - POST_ON_FINALIZE:      onFinalize ľ��
  # - POST_ON_STARTUP:       onStartup ľ��
  # - POST_ON_SHUTDOWN:      onShutdown ľ��
  # - POST_ON_ACTIVATED:     onActivated ľ��
  # - POST_ON_DEACTIVATED:   onDeactivated ľ��
  # - POST_ON_ABORTING:       onAborted ľ��
  # - POST_ON_ERROR:         onError ľ��
  # - POST_ON_RESET:         onReset ľ��
  # - POST_ON_EXECUTE:       onExecute ľ��
  # - POST_ON_STATE_UPDATE:  onStateUpdate ľ��
  #
  # �ꥹ�ʤ� PostComponentActionListener ��Ѿ������ʲ��Υ����˥�������
  # operator() ��������Ƥ���ɬ�פ����롣
  #
  # PostComponentActionListener::operator()(UniqueId ec_id, ReturnCode_t ret)
  #
  # �ǥե���ȤǤϡ����δؿ���Ϳ�����ꥹ�ʥ��֥������Ȥν�ͭ����
  # RTObject�˰ܤꡢRTObject���λ��⤷���ϡ�
  # removePostComponentActionListener() �ˤ�������˼�ưŪ�˲��Τ���롣
  # �ꥹ�ʥ��֥������Ȥν�ͭ����ƤӽФ�¦�ǰݻ����������ϡ���3��
  # ���� false ����ꤷ����ưŪ�ʲ��Τ��������뤳�Ȥ��Ǥ��롣
  #
  # @param listener_type �ꥹ�ʥ�����
  # @param memfunc �ؿ����֥�������
  # @param autoclean �ꥹ�ʥ��֥������Ȥμ�ưŪ���Τ�Ԥ����ɤ����Υե饰
  #
  # @else
  # @brief Adding PostComponentAction type listener
  #
  # This operation adds certain listeners related to ComponentActions
  # post events.
  # The following listener types are available.
  #
  # - POST_ON_INITIALIZE:    after onInitialize
  # - POST_ON_FINALIZE:      after onFinalize
  # - POST_ON_STARTUP:       after onStartup
  # - POST_ON_SHUTDOWN:      after onShutdown
  # - POST_ON_ACTIVATED:     after onActivated
  # - POST_ON_DEACTIVATED:   after onDeactivated
  # - POST_ON_ABORTING:       after onAborted
  # - POST_ON_ERROR:         after onError
  # - POST_ON_RESET:         after onReset
  # - POST_ON_EXECUTE:       after onExecute
  # - POST_ON_STATE_UPDATE:  after onStateUpdate
  #
  # Listeners should have the following function operator().
  #
  # PostComponentActionListener::operator()(UniqueId ec_id, ReturnCode_t ret)
  #
  # The ownership of the given listener object is transferred to
  # this RTObject object in default.  The given listener object will
  # be destroied automatically in the RTObject's dtor or if the
  # listener is deleted by removePostComponentActionListener() function.
  # If you want to keep ownership of the listener object, give
  # "false" value to 3rd argument to inhibit automatic destruction.
  #
  # @param listener_type A listener type
  # @param memfunc  member function object
  # @param autoclean A flag for automatic listener destruction
  #
  # @endif
  #
  # template <class Listener>
  # PostComponentActionListener*
  # addPostComponentActionListener(PostCompActionListenerType listener_type,
  #                                void (Listener::*memfunc)(UniqueId ec_id,
  #                                                          ReturnCode_t ret),
  #                                bool autoclean = true)
  def addPostComponentActionListener(self, listener_type,
                                     memfunc, autoclean = True):
    class Noname(OpenRTM_aist.PostComponentActionListener):
      def __init__(self, memfunc):
        self._memfunc = memfunc
        return
      def __call__(self, ec_id, ret):
        self._memfunc(ec_id, ret)
        return
      
    listener = Noname(memfunc)
    self._actionListeners.postaction_[listener_type].addListener(listener, autoclean)
    return listener


  ##
  # @if jp
  # @brief PostComponentActionListener �ꥹ�ʤ�������
  #
  # ���ꤷ���Ƽ�ꥹ�ʤ������롣
  # 
  # @param listener_type �ꥹ�ʥ�����
  # @param listener �ꥹ�ʥ��֥������ȤؤΥݥ���
  #
  # @else
  # @brief Removing PostComponentAction type listener
  #
  # This operation removes a specified listener.
  #     
  # @param listener_type A listener type
  # @param listener A pointer to a listener object
  #
  # @endif
  ##
  # void 
  # removePostComponentActionListener(PostComponentActionListenerType listener_type,
  #                                   PostComponentActionListener* listener);
  def removePostComponentActionListener(self, listener_type, listener):
    self._actionListeners.postaction_[listener_type].removeListener(listener)
    return


  ##
  # @if jp
  # @brief PortActionListener �ꥹ�ʤ��ɲä���
  #
  # Port���ɲá�������˥�����Хå������Ƽ�ꥹ�ʤ����ꤹ�롣
  #
  # ����Ǥ���ꥹ�ʤΥ����פȥ�����Хå����٥�Ȥϰʲ����̤�
  #
  # - ADD_PORT:    Port�ɲû�
  # - REMOVE_PORT: Port�����
  #
  # �ꥹ�ʤ� PortActionListener ��Ѿ������ʲ��Υ����˥�������
  # operator() ��������Ƥ���ɬ�פ����롣
  #
  # PortActionListener::operator()(PortProfile& pprof)
  #
  # �ǥե���ȤǤϡ����δؿ���Ϳ�����ꥹ�ʥ��֥������Ȥν�ͭ����
  # RTObject�˰ܤꡢRTObject���λ��⤷���ϡ�
  # removePortActionListener() �ˤ�������˼�ưŪ�˲��Τ���롣
  # �ꥹ�ʥ��֥������Ȥν�ͭ����ƤӽФ�¦�ǰݻ����������ϡ���3��
  # ���� false ����ꤷ����ưŪ�ʲ��Τ��������뤳�Ȥ��Ǥ��롣
  #
  # @param listener_type �ꥹ�ʥ�����
  # @param memfunc �ؿ����֥�������
  # @param autoclean �ꥹ�ʥ��֥������Ȥμ�ưŪ���Τ�Ԥ����ɤ����Υե饰
  #
  # @else
  # @brief Adding PortAction type listener
  #
  # This operation adds certain listeners related to ComponentActions
  # post events.
  # The following listener types are available.
  #
  # - ADD_PORT:    At adding Port
  # - REMOVE_PORT: At removing Port
  #
  # Listeners should have the following function operator().
  #
  # PortActionListener::operator()(RTC::PortProfile pprof)
  #
  # The ownership of the given listener object is transferred to
  # this RTObject object in default.  The given listener object will
  # be destroied automatically in the RTObject's dtor or if the
  # listener is deleted by removePortActionListener() function.
  # If you want to keep ownership of the listener object, give
  # "false" value to 3rd argument to inhibit automatic destruction.
  #
  # @param listener_type A listener type
  # @param memfunc  member function object
  # @param autoclean A flag for automatic listener destruction
  #
  # @endif
  #
  # template <class Listener>
  # PortActionListener*
  # addPortActionListener(PortActionListenerType listener_type,
  #                       void (Listener::*memfunc)(const RTC::PortProfile&),
  #                       bool autoclean=true)
  def addPortActionListener(self, listener_type,
                            memfunc, autoclean = True):
    class Noname(OpenRTM_aist.PortActionListener):
      def __init__(self, memfunc):
        self._memfunc = memfunc
        return

      def __call__(self, pprofile):
        self._memfunc(pprofile)
        return

    listener = Noname(memfunc)
    self._actionListeners.portaction_[listener_type].addListener(listener, autoclean)
    return listener


  ##
  # @if jp
  # @brief PortActionListener �ꥹ�ʤ�������
  #
  # ���ꤷ���Ƽ�ꥹ�ʤ������롣
  # 
  # @param listener_type �ꥹ�ʥ�����
  # @param listener �ꥹ�ʥ��֥������ȤؤΥݥ���
  #
  # @else
  # @brief Removing PortAction type listener
  #
  # This operation removes a specified listener.
  #     
  # @param listener_type A listener type
  # @param listener A pointer to a listener object
  #
  # @endif
  # void 
  # removePortActionListener(PortActionListenerType listener_type,
  #                          PortActionListener* listener);
  def removePortActionListener(self, listener_type, listener):
    self._actionListeners.portaction_[listener_type].removeListener(listener)
    return


  ##
  # @if jp
  # @brief ExecutionContextActionListener �ꥹ�ʤ��ɲä���
  #
  # ExecutionContext���ɲá�������˥�����Хå������Ƽ�ꥹ�ʤ����ꤹ�롣
  #
  # ����Ǥ���ꥹ�ʤΥ����פȥ�����Хå����٥�Ȥϰʲ����̤�
  #
  # - ATTACH_EC:    ExecutionContext �����å���
  # - DETACH_EC:    ExecutionContext �ǥ��å���
  #
  # �ꥹ�ʤ� ExecutionContextActionListener ��Ѿ������ʲ��Υ����˥�������
  # operator() ��������Ƥ���ɬ�פ����롣
  #
  # ExecutionContextActionListener::operator()(UniqueId��ec_id)
  #
  # �ǥե���ȤǤϡ����δؿ���Ϳ�����ꥹ�ʥ��֥������Ȥν�ͭ����
  # RTObject�˰ܤꡢRTObject���λ��⤷���ϡ�
  # removeExecutionContextActionListener() �ˤ�������˼�ưŪ�˲��Τ���롣
  # �ꥹ�ʥ��֥������Ȥν�ͭ����ƤӽФ�¦�ǰݻ����������ϡ���3��
  # ���� false ����ꤷ����ưŪ�ʲ��Τ��������뤳�Ȥ��Ǥ��롣
  #
  # @param listener_type �ꥹ�ʥ�����
  # @param memfunc �ؿ����֥�������
  # @param autoclean �ꥹ�ʥ��֥������Ȥμ�ưŪ���Τ�Ԥ����ɤ����Υե饰
  #
  # @else
  # @brief Adding ExecutionContextAction type listener
  #
  # This operation adds certain listeners related to ComponentActions
  # post events.
  # The following listener types are available.
  #
  # - ADD_PORT:    At adding ExecutionContext
  # - REMOVE_PORT: At removing ExecutionContext
  #
  # Listeners should have the following function operator().
  #
  # ExecutionContextActionListener::operator()(UniqueId ec_id)
  #
  # The ownership of the given listener object is transferred to
  # this RTObject object in default.  The given listener object will
  # be destroied automatically in the RTObject's dtor or if the
  # listener is deleted by removeExecutionContextActionListener() function.
  # If you want to keep ownership of the listener object, give
  # "false" value to 3rd argument to inhibit automatic destruction.
  #
  # @param listener_type A listener type
  # @param memfunc  member function object
  # @param autoclean A flag for automatic listener destruction
  #
  # @endif
  #
  # template <class Listener>
  # ECActionListener*
  # addExecutionContextActionListener(ECActionListenerType listener_type,
  #                                   void (Listener::*memfunc)(UniqueId),
  #                                   bool autoclean = true);
  def addExecutionContextActionListener(self, listener_type,
                                        memfunc, autoclean = True):
    class Noname(OpenRTM_aist.ExecutionContextActionListener):
      def __init__(self, memfunc):
        self._memfunc = memfunc
        return

      def __call__(self, ec_id):
        self._memfunc(ec_id)
        return

    listener = Noname(memfunc)
    self._actionListeners.ecaction_[listener_type].addListener(listener, autoclean)
    return listener
    

  ##
  # @if jp
  # @brief ExecutionContextActionListener �ꥹ�ʤ�������
  #
  # ���ꤷ���Ƽ�ꥹ�ʤ������롣
  # 
  # @param listener_type �ꥹ�ʥ�����
  # @param listener �ꥹ�ʥ��֥������ȤؤΥݥ���
  #
  # @else
  # @brief Removing ExecutionContextAction type listener
  #
  # This operation removes a specified listener.
  #     
  # @param listener_type A listener type
  # @param listener A pointer to a listener object
  #
  # @endif
  #
  # void 
  # removeExecutionContextActionListener(ECActionListenerType listener_type,
  #                                      ECActionListener* listener);
  def removeExecutionContextActionListener(self, listener_type, listener):
    self._actionListeners.ecaction_[listener_type].removeListener(listener)
    return


  ##
  # @if jp
  # @brief PortConnectListener �ꥹ�ʤ��ɲä���
  #
  # Port����³������³������˸ƤӽФ����Ƽ�ꥹ�ʤ����ꤹ�롣
  #
  # ����Ǥ���ꥹ�ʤΥ����פȥ�����Хå����٥�Ȥϰʲ����̤�
  #
  # - ON_NOTIFY_CONNECT: notify_connect() �ؿ���ƤӽФ�ľ��
  # - ON_NOTIFY_DISCONNECT: notify_disconnect() �ƤӽФ�ľ��
  # - ON_UNSUBSCRIBE_INTERFACES: notify_disconnect() ���IF���ɲ����
  #
  # �ꥹ�ʤ� PortConnectListener ��Ѿ������ʲ��Υ����˥�������
  # operator() ��������Ƥ���ɬ�פ����롣
  #
  # PortConnectListener::operator()(const char*, ConnectorProfile)
  #
  # �ǥե���ȤǤϡ����δؿ���Ϳ�����ꥹ�ʥ��֥������Ȥν�ͭ����
  # RTObject�˰ܤꡢRTObject���λ��⤷���ϡ�
  # removePortConnectListener() �ˤ�������˼�ưŪ�˲��Τ���롣
  # �ꥹ�ʥ��֥������Ȥν�ͭ����ƤӽФ�¦�ǰݻ����������ϡ���3��
  # ���� false ����ꤷ����ưŪ�ʲ��Τ��������뤳�Ȥ��Ǥ��롣
  #
  # @param listener_type �ꥹ�ʥ�����
  # @param memfunc �ؿ����֥�������
  # @param autoclean �ꥹ�ʥ��֥������Ȥμ�ưŪ���Τ�Ԥ����ɤ����Υե饰
  #
  # @else
  # @brief Adding PortConnect type listener
  #
  # This operation adds certain listeners related to Port's connect actions.
  # The following listener types are available.
  #
  # - ON_NOTIFY_CONNECT: right after entering into notify_connect()
  # - ON_NOTIFY_DISCONNECT: right after entering into notify_disconnect()
  # - ON_UNSUBSCRIBE_INTERFACES: unsubscribing IF in notify_disconnect()
  #
  # Listeners should have the following function operator().
  #
  # PortConnectListener::operator()(const char*, ConnectorProfile)
  #
  # The ownership of the given listener object is transferred to
  # this RTObject object in default.  The given listener object will
  # be destroied automatically in the RTObject's dtor or if the
  # listener is deleted by removePortConnectListener() function.
  # If you want to keep ownership of the listener object, give
  # "false" value to 3rd argument to inhibit automatic destruction.
  #
  # @param listener_type A listener type
  # @param memfunc  member function object
  # @param autoclean A flag for automatic listener destruction
  #
  # @endif
  #
  # template <class Listener>
  # PortConnectListener*
  # addPortConnectListener(PortConnectListenerType listener_type,
  #                        void (Listener::*memfunc)(const char*,
  #                                                  ConnectorProfile&),
  #                        bool autoclean = true)
  def addPortConnectListener(self, listener_type,
                             memfunc, autoclean = True):
    class Noname(OpenRTM_aist.PortConnectListener):
      def __init__(self, memfunc):
        self._memfunc = memfunc
        return

      def __call__(self, portname, cprofile):
        self._memfunc(portname, cprofile)
        return

    listener = Noname(memfunc)
    self._portconnListeners.portconnect_[listener_type].addListener(listener, autoclean)
    return listener
    

  ##
  # @if jp
  # @brief PortConnectListener �ꥹ�ʤ�������
  #
  # ���ꤷ���Ƽ�ꥹ�ʤ������롣
  # 
  # @param listener_type �ꥹ�ʥ�����
  # @param listener �ꥹ�ʥ��֥������ȤؤΥݥ���
  #
  # @else
  # @brief Removing PortConnect type listener
  #
  # This operation removes a specified listener.
  #     
  # @param listener_type A listener type
  # @param listener A pointer to a listener object
  #
  # @endif
  #
  # void 
  # removePortConnectListener(PortConnectListenerType listener_type,
  #                           PortConnectListener* listener);
  def removePortConnectListener(self, listener_type, listener):
    self._portconnListeners.portconnect_[listener_type].removeListener(listener)
    return


  ##
  # @if jp
  # @brief PortConnectRetListener �ꥹ�ʤ��ɲä���
  #
  # Port����³������³������˸ƤӽФ����Ƽ�ꥹ�ʤ����ꤹ�롣
  #
  # ����Ǥ���ꥹ�ʤΥ����פȥ�����Хå����٥�Ȥϰʲ����̤�
  #
  # - ON_CONNECT_NEXTPORT: notify_connect() ��Υ��������ɸƤӽФ�ľ��
  # - ON_SUBSCRIBE_INTERFACES: notify_connect() ��Υ��󥿡��ե���������ľ��
  # - ON_CONNECTED: nofity_connect() ��³������λ���˸ƤӽФ����
  # - ON_DISCONNECT_NEXT: notify_disconnect() ��˥��������ɸƤӽФ�ľ��
  # - ON_DISCONNECTED: notify_disconnect() �꥿�����
  #
  # �ꥹ�ʤ� PortConnectRetListener ��Ѿ������ʲ��Υ����˥�������
  # operator() ��������Ƥ���ɬ�פ����롣
  #
  # PortConnectRetListener::operator()(const char*, ConnectorProfile)
  #
  # �ǥե���ȤǤϡ����δؿ���Ϳ�����ꥹ�ʥ��֥������Ȥν�ͭ����
  # RTObject�˰ܤꡢRTObject���λ��⤷���ϡ�
  # removePortConnectRetListener() �ˤ�������˼�ưŪ�˲��Τ���롣
  # �ꥹ�ʥ��֥������Ȥν�ͭ����ƤӽФ�¦�ǰݻ����������ϡ���3��
  # ���� false ����ꤷ����ưŪ�ʲ��Τ��������뤳�Ȥ��Ǥ��롣
  #
  # @param listener_type �ꥹ�ʥ�����
  # @param memfunc �ؿ����֥�������
  # @param autoclean �ꥹ�ʥ��֥������Ȥμ�ưŪ���Τ�Ԥ����ɤ����Υե饰
  #
  # @else
  # @brief Adding PortConnectRet type listener
  #
  # This operation adds certain listeners related to Port's connect actions.
  # The following listener types are available.
  #
  # - ON_CONNECT_NEXTPORT: after cascade-call in notify_connect()
  # - ON_SUBSCRIBE_INTERFACES: after IF subscribing in notify_connect()
  # - ON_CONNECTED: completed nofity_connect() connection process
  # - ON_DISCONNECT_NEXT: after cascade-call in notify_disconnect()
  # - ON_DISCONNECTED: completed notify_disconnect() disconnection process
  #
  # Listeners should have the following function operator().
  #
  # PortConnectRetListener::operator()(const char*, ConnectorProfile)
  #
  # The ownership of the given listener object is transferred to
  # this RTObject object in default.  The given listener object will
  # be destroied automatically in the RTObject's dtor or if the
  # listener is deleted by removePortConnectRetListener() function.
  # If you want to keep ownership of the listener object, give
  # "false" value to 3rd argument to inhibit automatic destruction.
  #
  # @param listener_type A listener type
  # @param memfunc  member function object
  # @param autoclean A flag for automatic listener destruction
  #
  # @endif
  #
  # template <class Listener>
  # PortConnectRetListener*
  # addPortConnectRetListener(PortConnectRetListenerType listener_type,
  #                           void (Listener::*memfunc)(const char*,
  #                                                     ConnectorProfile&,
  #                                                     ReturnCode_t))
  def addPortConnectRetListener(self, listener_type,
                                memfunc, autoclean = True):
    class Noname(OpenRTM_aist.PortConnectRetListener):
      def __init__(self, memfunc):
        self._memfunc = memfunc
        return

      def __call__(self, portname, cprofile, ret):
        self._memfunc(portname, cprofile, ret)
        return

    listener = Noname(memfunc)
    self._portconnListeners.portconnret_[listener_type].addListener(listener, autoclean)
    return listener
    

  ##
  # @if jp
  # @brief PortConnectRetListener �ꥹ�ʤ�������
  #
  # ���ꤷ���Ƽ�ꥹ�ʤ������롣
  # 
  # @param listener_type �ꥹ�ʥ�����
  # @param listener �ꥹ�ʥ��֥������ȤؤΥݥ���
  #
  # @else
  # @brief Removing PortConnectRet type listener
  #
  # This operation removes a specified listener.
  #     
  # @param listener_type A listener type
  # @param listener A pointer to a listener object
  #
  # @endif
  #
  # void 
  # removePortConnectRetListener(PortConnectRetListenerType listener_type,
  #                              PortConnectRetListener* listener);
  def removePortConnectRetListener(self, listener_type, listener):
    self._portconnListeners.portconnret_[listener_type].removeListener(listener)
    return


  ##
  # @if jp
  #
  # @brief ConfigurationParamListener ���ɲä���
  #
  # update(const char* config_set, const char* config_param) ���ƤФ줿�ݤ�
  # �����뤵���ꥹ�� ConfigurationParamListener ���ɲä��롣
  # type �ˤϸ��ߤΤȤ��� ON_UPDATE_CONFIG_PARAM �Τߤ����롣
  #
  # @param type ConfigurationParamListenerType�����͡�
  #             ON_UPDATE_CONFIG_PARAM �����롣
  #
  # @param memfunc �ؿ����֥�������
  # @param autoclean �ꥹ�ʥ��֥������Ȥ�ư�Ǻ�����뤫�ɤ����Υե饰
  # 
  # @else
  #
  # @brief Adding ConfigurationParamListener 
  # 
  # This function adds a listener object which is called when
  # update(const char* config_set, const char* config_param) is
  # called. In the type argument, currently only
  # ON_UPDATE_CONFIG_PARAM is allowed.
  #
  # @param type ConfigurationParamListenerType value
  #             ON_UPDATE_CONFIG_PARAM is only allowed.
  #
  # @param memfunc  member function object
  # @param autoclean a flag whether if the listener object autocleaned.
  #
  # @endif
  #
  # template <class Listener>
  # ConfigurationParamListener*
  # addConfigurationParamListener(ConfigurationParamListenerType listener_type,
  #                               void (Listener::*memfunc)(const char*,
  #                                                         const char*),
  #                               bool autoclean = true)
  def addConfigurationParamListener(self, type,
                                    memfunc, autoclean = True):
    class Noname(OpenRTM_aist.ConfigurationParamListener):
      def __init__(self, memfunc):
        self._memfunc = memfunc
        return

      def __call__(self, config_set_name, config_param_name):
        self._memfunc(config_set_name, config_param_name)
        return

    listener = Noname(memfunc)
    self._configsets.addConfigurationParamListener(type, listener, autoclean)
    return listener


  ##
  # @if jp
  #
  # @brief ConfigurationParamListener ��������
  #
  # addConfigurationParamListener ���ɲä��줿�ꥹ�ʥ��֥������Ȥ������롣
  #
  # @param type ConfigurationParamListenerType�����͡�
  #             ON_UPDATE_CONFIG_PARAM �����롣
  # @param listener Ϳ�����ꥹ�ʥ��֥������ȤؤΥݥ���
  # 
  # @else
  #
  # @brief Removing ConfigurationParamListener 
  # 
  # This function removes a listener object which is added by
  # addConfigurationParamListener() function.
  #
  # @param type ConfigurationParamListenerType value
  #             ON_UPDATE_CONFIG_PARAM is only allowed.
  # @param listener a pointer to ConfigurationParamListener listener object.
  #
  # @endif
  #
  # void removeConfigurationParamListener(ConfigurationParamListenerType type,
  #                                       ConfigurationParamListener* listener);
  def removeConfigurationParamListener(self, type, listener):
    self._configsets.removeConfigurationParamListener(type, listener)
    return
    

  ##
  # @if jp
  #
  # @brief ConfigurationSetListener ���ɲä���
  #
  # ConfigurationSet ���������줿�Ȥ��ʤɤ˸ƤФ��ꥹ��
  # ConfigurationSetListener ���ɲä��롣�����ǽ�ʥ��٥�Ȥϰʲ���
  # 2���ब���롣
  #
  # - ON_SET_CONFIG_SET: setConfigurationSetValues() ��
  #                      ConfigurationSet ���ͤ����ꤵ�줿��硣
  # - ON_ADD_CONFIG_SET: addConfigurationSet() �ǿ�����
  #                      ConfigurationSet ���ɲä��줿��硣
  #
  # @param type ConfigurationSetListenerType�����͡�
  # @param memfunc �ؿ����֥�������
  # @param autoclean �ꥹ�ʥ��֥������Ȥ�ư�Ǻ�����뤫�ɤ����Υե饰
  # 
  # @else
  #
  # @brief Adding ConfigurationSetListener 
  # 
  # This function add a listener object which is called when
  # ConfigurationSet is updated. Available events are the followings.
  #
  # @param type ConfigurationSetListenerType value
  # @param memfunc  member function object
  # @param autoclean a flag whether if the listener object autocleaned.
  #
  # @endif
  #
  # template <class Listener>
  # ConfigurationSetListener*
  # addConfigurationSetListener(ConfigurationSetListenerType listener_type,
  #                             void (Listener::*memfunc)
  #                             (const coil::Properties& config_set))
  def addConfigurationSetListener(self, listener_type,
                                  memfunc, autoclean = True):
    class Noname(OpenRTM_aist.ConfigurationSetListener):
      def __init__(self, memfunc):
        self._memfunc = memfunc
        return

      def __call__(self, config_set):
        self._memfunc(config_set)
        return

    listener = Noname(memfunc)
    self._configsets.addConfigurationSetListener(listener_type, listener, autoclean)
    return listener


  ##
  # @if jp
  #
  # @brief ConfigurationSetListener ��������
  #
  # addConfigurationSetListener ���ɲä��줿�ꥹ�ʥ��֥������Ȥ������롣
  #
  # @param type ConfigurationSetListenerType�����͡�
  # @param listener Ϳ�����ꥹ�ʥ��֥������ȤؤΥݥ���
  # 
  # @else
  #
  # @brief Removing ConfigurationSetListener 
  # 
  # This function removes a listener object which is added by
  # addConfigurationSetListener() function.
  #
  # @param type ConfigurationSetListenerType value
  # @param listener a pointer to ConfigurationSetListener listener object.
  #
  # @endif
  #
  # void removeConfigurationSetListener(ConfigurationSetListenerType type,
  #                                     ConfigurationSetListener* listener);
  def removeConfigurationSetListener(self, type, listener):
    self._configsets.removeConfigurationSetListener(type, listener)
    return


  ##
  # @if jp
  #
  # @brief ConfigurationSetNameListener ���ɲä���
  #
  # ConfigurationSetName ���������줿�Ȥ��ʤɤ˸ƤФ��ꥹ��
  # ConfigurationSetNameListener ���ɲä��롣�����ǽ�ʥ��٥�Ȥϰʲ���
  # 3���ब���롣
  #
  # - ON_UPDATE_CONFIG_SET: ���� ConfigurationSet �����åץǡ��Ȥ��줿
  # - ON_REMOVE_CONFIG_SET: ���� ConfigurationSet ��������줿
  # - ON_ACTIVATE_CONFIG_SET: ���� ConfigurationSet �������ƥ��ֲ����줿
  #
  # @param type ConfigurationSetNameListenerType�����͡�
  # @param memfunc �ؿ����֥�������
  # @param autoclean �ꥹ�ʥ��֥������Ȥ�ư�Ǻ�����뤫�ɤ����Υե饰
  # 
  # @else
  #
  # @brief Adding ConfigurationSetNameListener 
  # 
  # This function add a listener object which is called when
  # ConfigurationSetName is updated. Available events are the followings.
  #
  # - ON_UPDATE_CONFIG_SET: A ConfigurationSet has been updated.
  # - ON_REMOVE_CONFIG_SET: A ConfigurationSet has been deleted.
  # - ON_ACTIVATE_CONFIG_SET: A ConfigurationSet has been activated.
  #
  # @param type ConfigurationSetNameListenerType value
  # @param memfunc  member function object
  # @param autoclean a flag whether if the listener object autocleaned.
  #
  # @endif
  #
  # template <class Listener>
  # ConfigurationSetNameListener*
  # addConfigurationSetNameListener(ConfigurationSetNameListenerType type,
  #                                 void (Listener::*memfunc)(const char*))
  def addConfigurationSetNameListener(self, type, memfunc, autoclean = True):
    class Noname(OpenRTM_aist.ConfigurationSetNameListener):
      def __init__(self, memfunc):
        self._memfunc = memfunc
        return

      def __call__(self, config_set_name):
        self._memfunc(config_set_name)
        return

    listener = Noname(memfunc)
    self._configsets.addConfigurationSetNameListener(type, listener, autoclean)
    return listener


  ##
  # @if jp
  #
  # @brief ConfigurationSetNameListener ��������
  #
  # addConfigurationSetNameListener ���ɲä��줿�ꥹ�ʥ��֥������Ȥ�
  # ������롣
  #
  # @param type ConfigurationSetNameListenerType�����͡�
  #             ON_UPDATE_CONFIG_PARAM �����롣
  # @param listener Ϳ�����ꥹ�ʥ��֥������ȤؤΥݥ���
  # 
  # @else
  #
  # @brief Removing ConfigurationSetNameListener 
  # 
  # This function removes a listener object which is added by
  # addConfigurationSetNameListener() function.
  #
  # @param type ConfigurationSetNameListenerType value
  #             ON_UPDATE_CONFIG_PARAM is only allowed.
  # @param listener a pointer to ConfigurationSetNameListener
  #             listener object.
  #
  # @endif
  # void
  # removeConfigurationSetNameListener(ConfigurationSetNameListenerType type,
  #                                    ConfigurationSetNameListener* listener);
  def removeConfigurationSetNameListener(self, type, listener):
    self._configsets.removeConfigurationSetNameListener(type, listener)
    return


  ##
  # @if jp
  #
  # @brief RTC ��λ����
  #
  # RTC �ν�λ������¹Ԥ��롣
  # �ݻ����Ƥ����� Port ����Ͽ��������ȤȤ�ˡ��������� CORBA ���֥�������
  # �������������RTC ��λ���롣
  # 
  # @param self
  #
  # @else
  #
  # @endif
  def shutdown(self):
    self._rtcout.RTC_TRACE("shutdown()")
    try:
      self.finalizePorts()
      self.finalizeContexts()
      self._poa.deactivate_object(self._poa.servant_to_id(self._SdoConfigImpl))
      self._poa.deactivate_object(self._poa.servant_to_id(self))
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if self._manager:
      self._rtcout.RTC_DEBUG("Cleanup on Manager")
      self._manager.notifyFinalized(self)

    return

  # inline void preOnInitialize(UniqueId ec_id)
  def preOnInitialize(self, ec_id):
    self._actionListeners.preaction_[OpenRTM_aist.PreComponentActionListenerType.PRE_ON_INITIALIZE].notify(ec_id)
    return

  # inline void preOnFinalize(UniqueId ec_id)
  def preOnFinalize(self, ec_id):
    self._actionListeners.preaction_[OpenRTM_aist.PreComponentActionListenerType.PRE_ON_FINALIZE].notify(ec_id)
    return

  # inline void preOnStartup(UniqueId ec_id)
  def preOnStartup(self, ec_id):
    self._actionListeners.preaction_[OpenRTM_aist.PreComponentActionListenerType.PRE_ON_STARTUP].notify(ec_id)
    return

  # inline void preOnShutdown(UniqueId ec_id)
  def preOnShutdown(self, ec_id):
    self._actionListeners.preaction_[OpenRTM_aist.PreComponentActionListenerType.PRE_ON_SHUTDOWN].notify(ec_id)
    return

  # inline void preOnActivated(UniqueId ec_id)
  def preOnActivated(self, ec_id):
    self._actionListeners.preaction_[OpenRTM_aist.PreComponentActionListenerType.PRE_ON_ACTIVATED].notify(ec_id)
    return

  # inline void preOnDeactivated(UniqueId ec_id)
  def preOnDeactivated(self, ec_id):
    self._actionListeners.preaction_[OpenRTM_aist.PreComponentActionListenerType.PRE_ON_DEACTIVATED].notify(ec_id)
    return

  # inline void preOnAborting(UniqueId ec_id)
  def preOnAborting(self, ec_id):
    self._actionListeners.preaction_[OpenRTM_aist.PreComponentActionListenerType.PRE_ON_ABORTING].notify(ec_id)
    return

  # inline void preOnError(UniqueId ec_id)
  def preOnError(self, ec_id):
    self._actionListeners.preaction_[OpenRTM_aist.PreComponentActionListenerType.PRE_ON_ERROR].notify(ec_id)
    return

  # inline void preOnReset(UniqueId ec_id)
  def preOnReset(self, ec_id):
    self._actionListeners.preaction_[OpenRTM_aist.PreComponentActionListenerType.PRE_ON_RESET].notify(ec_id)
    return

  # inline void preOnExecute(UniqueId ec_id)
  def preOnExecute(self, ec_id):
    self._actionListeners.preaction_[OpenRTM_aist.PreComponentActionListenerType.PRE_ON_EXECUTE].notify(ec_id)
    return

  # inline void preOnStateUpdate(UniqueId ec_id)
  def preOnStateUpdate(self, ec_id):
    self._actionListeners.preaction_[OpenRTM_aist.PreComponentActionListenerType.PRE_ON_STATE_UPDATE].notify(ec_id)
    return
    

  # inline void preOnRateChanged(UniqueId ec_id)
  def preOnRateChanged(self, ec_id):
    self._actionListeners.preaction_[OpenRTM_aist.PreComponentActionListenerType.PRE_ON_RATE_CHANGED].notify(ec_id)
    return
    

  # inline void postOnInitialize(UniqueId ec_id, ReturnCode_t ret)
  def postOnInitialize(self, ec_id, ret):
    self._actionListeners.postaction_[OpenRTM_aist.PostComponentActionListenerType.POST_ON_INITIALIZE].notify(ec_id, ret)
    return
    

  # inline void postOnFinalize(UniqueId ec_id, ReturnCode_t ret)
  def postOnFinalize(self, ec_id, ret):
    self._actionListeners.postaction_[OpenRTM_aist.PostComponentActionListenerType.POST_ON_FINALIZE].notify(ec_id, ret)
    return
    

  # inline void postOnStartup(UniqueId ec_id, ReturnCode_t ret)
  def postOnStartup(self, ec_id, ret):
    self._actionListeners.postaction_[OpenRTM_aist.PostComponentActionListenerType.POST_ON_STARTUP].notify(ec_id, ret)
    return
    

  # inline void postOnShutdown(UniqueId ec_id, ReturnCode_t ret)
  def postOnShutdown(self, ec_id, ret):
    self._actionListeners.postaction_[OpenRTM_aist.PostComponentActionListenerType.POST_ON_SHUTDOWN].notify(ec_id, ret)
    return
    

  # inline void postOnActivated(UniqueId ec_id, ReturnCode_t ret)
  def postOnActivated(self, ec_id, ret):
    self._actionListeners.postaction_[OpenRTM_aist.PostComponentActionListenerType.POST_ON_ACTIVATED].notify(ec_id, ret)
    return
    

  # inline void postOnDeactivated(UniqueId ec_id, ReturnCode_t ret)
  def postOnDeactivated(self, ec_id, ret):
    self._actionListeners.postaction_[OpenRTM_aist.PostComponentActionListenerType.POST_ON_DEACTIVATED].notify(ec_id, ret)
    return
    

  # inline void postOnAborting(UniqueId ec_id, ReturnCode_t ret)
  def postOnAborting(self, ec_id, ret):
    self._actionListeners.postaction_[OpenRTM_aist.PostComponentActionListenerType.POST_ON_ABORTING].notify(ec_id, ret)
    return
    

  # inline void postOnError(UniqueId ec_id, ReturnCode_t ret)
  def postOnError(self, ec_id, ret):
    self._actionListeners.postaction_[OpenRTM_aist.PostComponentActionListenerType.POST_ON_ERROR].notify(ec_id, ret)
    return
    

  # inline void postOnReset(UniqueId ec_id, ReturnCode_t ret)
  def postOnReset(self, ec_id, ret):
    self._actionListeners.postaction_[OpenRTM_aist.PostComponentActionListenerType.POST_ON_RESET].notify(ec_id, ret)
    return
    

  # inline void postOnExecute(UniqueId ec_id, ReturnCode_t ret)
  def postOnExecute(self, ec_id, ret):
    self._actionListeners.postaction_[OpenRTM_aist.PostComponentActionListenerType.POST_ON_EXECUTE].notify(ec_id, ret)
    return
    

  # inline void postOnStateUpdate(UniqueId ec_id, ReturnCode_t ret)
  def postOnStateUpdate(self, ec_id, ret):
    self._actionListeners.postaction_[OpenRTM_aist.PostComponentActionListenerType.POST_ON_STATE_UPDATE].notify(ec_id, ret)
    return
    

  # inline void postOnRateChanged(UniqueId ec_id, ReturnCode_t ret)
  def postOnRateChanged(self, ec_id, ret):
    self._actionListeners.postaction_[OpenRTM_aist.PostComponentActionListenerType.POST_ON_RATE_CHANGED].notify(ec_id, ret)
    return
    

  # inline void onAddPort(const PortProfile& pprof)
  def onAddPort(self, pprof):
    self._actionListeners.portaction_[OpenRTM_aist.PortActionListenerType.ADD_PORT].notify(pprof)
    return
    
    
  # inline void onRemovePort(const PortProfile& pprof)
  def onRemovePort(self, pprof):
    self._actionListeners.portaction_[OpenRTM_aist.PortActionListenerType.REMOVE_PORT].notify(pprof)
    return
    
    
  # inline void onAttachExecutionContext(UniqueId ec_id)
  def onAttachExecutionContext(self, ec_id):
    self._actionListeners.ecaction_[OpenRTM_aist.ExecutionContextActionListenerType.EC_ATTACHED].notify(ec_id)
    return
    
    
  # inline void onDetachExecutionContext(UniqueId ec_id)
  def onDetachExecutionContext(self, ec_id):
    self._actionListeners.ecaction_[OpenRTM_aist.ExecutionContextActionListenerType.EC_DETACHED].notify(ec_id)
    return

    
  ##
  # @if jp
  # @class svc_name
  # @brief SDOService �Υץ�ե�����ꥹ�Ȥ���id�ǥ��������뤿���
  # �ե��󥯥����饹
  # @else
  #
  # @endif
  class svc_name:
    def __init__(self, _id):
      self._id= _id

    def __call__(self, prof):
      return self._id == prof.id


  #------------------------------------------------------------
  # Functor
  #------------------------------------------------------------

  ##
  # @if jp
  # @class nv_name
  # @brief NVList �����ѥե��󥯥�
  # @else
  #
  # @endif
  class nv_name:
    def __init__(self, _name):
      self._name = _name

    def __call__(self, nv):
      return self._name == nv.name


  ##
  # @if jp
  # @class ec_find
  # @brief ExecutionContext �����ѥե��󥯥�
  # @else
  #
  # @endif
  class ec_find:
    def __init__(self, _ec):
      self._ec = _ec

    def __call__(self, ecs):
      try:
        if not CORBA.is_nil(ecs):
          ec = ecs._narrow(RTC.ExecutionContext)
          return self._ec._is_equivalent(ec)
      except:
        print OpenRTM_aist.Logger.print_exception()
        return False

      return False


  ##
  # @if jp
  # @class ec_copy
  # @brief ExecutionContext Copy�ѥե��󥯥�
  # @else
  #
  # @endif
  class ec_copy:
    def __init__(self, eclist):
      self._eclist = eclist

    def __call__(self, ecs):
      if not CORBA.is_nil(ecs):
        self._eclist.append(ecs)


  ##
  # @if jp
  # @class deactivate_comps
  # @brief RTC ��������ѥե��󥯥�
  # @else
  #
  # @endif
  class deactivate_comps:
    def __init__(self, comp):
      self._comp = comp

    def __call__(self, ec):
      try:
        if not CORBA.is_nil(ec) and not ec._non_existent():
          ec.deactivate_component(self._comp)
          ec.stop()
      except:
        print OpenRTM_aist.Logger.print_exception()


# RtcBase = RTObject_impl
