#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file Factory.py
# @brief RTComponent factory class
# @date $Date: 2006/11/06 01:28:36 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2003-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import OpenRTM_aist


##
# @if jp
#
# @brief brief RT����ݡ��ͥ���˴��Ѵؿ�
#
# RT����ݡ��ͥ�ȤΥ��󥹥��󥹤��˴����뤿��δؿ���
# �����ˤƻ��ꤷ��RT����ݡ��ͥ�ȤΥ��󥹥��󥹤򡢽�λ������ƤӽФ���
# �˴����롣
#
# @param rtc �˴��о�RT����ݡ��ͥ�ȤΥ��󥹥���
#
# @else
#
# @endif
def Delete(rtc):
  del rtc



##
# @if jp
#
# @class FactoryBase
# @brief FactoryBase ���쥯�饹
# 
# RT����ݡ��ͥ�������ѥե����ȥ�δ��쥯�饹��
# �ºݤγƼ�ե����ȥꥯ�饹�����������ϡ��ܥ��饹��Ѿ�������Ǽ������롣
# �ºݤ���������������϶�ݥ��֥��饹�ˤƼ�������ɬ�פ����롣
#
# @since 0.2.0
#
# @else
#
# @class FactoryBase
# @brief FactoryBase base class
#
# RTComponent factory base class.
#
# @since 0.2.0
#
# @endif
class FactoryBase:
  """
  """

  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯����
  #
  # @param self
  # @param profile ����ݡ��ͥ�ȤΥץ�ե�����
  #
  # @else
  #
  # @brief Constructor.
  #
  # Constructor.
  #
  # @param profile component profile
  #
  # @endif
  def __init__(self, profile):
    ## self._Profile Component profile
    self._Profile = profile
    ## self._Number Number of current component instances.
    self._Number = -1
    
    pass


  ##
  # @if jp
  #
  # @brief ����ݡ��ͥ�Ȥ�����(���֥��饹������)
  #
  # RTComponent �Υ��󥹥��󥹤��������뤿��δؿ���<BR>
  # �ºݤν���������ϡ��ƶ�ݥ��饹��ˤƵ��Ҥ��롣
  #
  # @param self
  # @param mgr �ޥ͡����㥪�֥�������
  #
  # @return ������������ݡ��ͥ��
  #
  # @else
  #
  # @brief Create component
  #
  # @param mgr pointer to RtcManager
  #
  # @endif
  def create(self, mgr):
    pass


  ##
  # @if jp
  #
  # @brief ����ݡ��ͥ�Ȥ��˴�(���֥��饹������)
  #
  # RTComponent �Υ��󥹥��󥹤��˴����뤿��δؿ���<BR>
  # �ºݤν���������ϡ��ƶ�ݥ��饹��ˤƵ��Ҥ��롣
  #
  # @param self
  # @param comp �˴��о� RT����ݡ��ͥ��
  #
  # @else
  #
  # @brief Destroy component
  #
  # @param comp pointer to RtcBase
  #
  # @endif
  def destroy(self, comp):
    pass


  ##
  # @if jp
  #
  # @brief ����ݡ��ͥ�ȥץ�ե�����μ���
  #
  # ����ݡ��ͥ�ȤΥץ�ե�������������
  #
  # @param self
  #
  # @return ����ݡ��ͥ�ȤΥץ�ե�����
  #
  # @else
  #
  # @brief Get component profile
  #
  # Get component profile.
  #
  # @endif
  def profile(self):
    return self._Profile


  ##
  # @if jp
  #
  # @brief ���ߤΥ��󥹥��󥹿��μ���
  #
  # ����ݡ��ͥ�Ȥθ��ߤΥ��󥹥��󥹿���������롣
  #
  # @param self
  #
  # @return ����ݡ��ͥ�ȤΥ��󥹥��󥹿�
  #
  # @else
  #
  # @brief Get number of component instances
  #
  # Get number of current component instances.
  #
  # @endif
  def number(self):
    return self._Number




##
# @if jp
# @class FactoryPython
# @brief FactoryPython ���饹
# 
# Python�ѥ���ݡ��ͥ�ȥե����ȥꥯ�饹��
#
# @since 0.4.1
#
#
# @else
#
# @class FactoryPython
# @brief FactoryPython class
#
# RTComponent factory class for Python.
#
# @endif
class FactoryPython(FactoryBase):
  """
  """

  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯����
  # �����оݥ���ݡ��ͥ�ȤΥץ�ե����롢����ݡ��ͥ�������Ѵؿ���
  # ����ݡ��ͥ���˴��Ѵؿ�������ݡ��ͥ����������̿̾�ݥꥷ��������˼�ꡢ
  # Python �Ǽ������줿����ݡ��ͥ�ȤΥե����ȥꥯ�饹���������롣
  #
  # @param self
  # @param profile ����ݡ��ͥ�ȤΥץ�ե�����
  # @param new_func ����ݡ��ͥ�������Ѵؿ�
  # @param delete_func ����ݡ��ͥ���˴��Ѵؿ�
  # @param policy ����ݡ��ͥ����������̿̾�ݥꥷ��(�ǥե������:None)
  #
  # @else
  #
  # @brief Constructor.
  #
  # Constructor.
  # Create component factory class with three arguments:
  # component profile, function pointer to object create function and
  # object delete function.
  #
  # @param profile Component profile
  # @param new_func Pointer to component create function
  # @param delete_func Pointer to component delete function
  # @param policy Pointer to component delete function
  #
  # @endif
  def __init__(self, profile, new_func, delete_func, policy=None):
    FactoryBase.__init__(self, profile)
    
    if policy is None:
      self._policy = OpenRTM_aist.DefaultNumberingPolicy()
    else:
      self._policy = policy

    self._New = new_func
    
    self._Delete = delete_func


  ##
  # @if jp
  #
  # @brief ����ݡ��ͥ�Ȥ�����
  #
  # RTComponent �Υ��󥹥��󥹤��������롣
  #
  # @param self
  # @param mgr �ޥ͡����㥪�֥�������
  #
  # @return ������������ݡ��ͥ��
  #
  # @else
  #
  # @brief Create component
  #
  # Create component implemented in Python.
  #
  # @param mgr
  #
  # @endif
  def create(self, mgr):
    try:
      rtobj = self._New(mgr)
      if rtobj == 0:
        return None

      self._Number += 1
      
      rtobj.setProperties(self.profile())
      
      instance_name = rtobj.getTypeName()
      instance_name += self._policy.onCreate(rtobj)
      rtobj.setInstanceName(instance_name)

      return rtobj
    except:
      print OpenRTM_aist.Logger.print_exception()
      return None


  ##
  # @if jp
  #
  # @brief ����ݡ��ͥ�Ȥ��˴�
  #
  # RTComponent �Υ��󥹥��󥹤��˴����롣
  #
  # @param self
  # @param comp �˴��о� RTComponent
  #
  # @else
  #
  # @brief Destroy component
  #
  # Destroy component instance
  #
  # @param comp
  #
  # @endif
  def destroy(self, comp):
    self._Number -= 1
    self._policy.onDelete(comp)
    self._Delete(comp)
