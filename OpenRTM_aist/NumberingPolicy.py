#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file NumberingPolicy.py
# @brief Object numbering policy class
# @date $Date: 2007/08/23$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import string
import OpenRTM_aist

##
# @if jp
#
# @class NumberingPolicy
# @brief ���֥��������������͡��ߥ󥰡��ݥꥷ��(̿̾��§)��������ݥ��饹
#
# ���֥������Ȥ���������ݤΥ͡��ߥ󥰡��ݥꥷ��(̿̾��§)��������뤿���
# ��ݥ��饹��
# ��ݥ��饹�ϡ��ʲ��δؿ��μ������󶡤��ʤ���Фʤ�ʤ���
# - onCreate() : ���֥���������������̾�κ���
# - onDelete() : ���֥������Ⱥ������̾�β���
#
# @since 0.4.0
#
# @else
#
# @endif
class NumberingPolicy:
  """
  """



  ##
  # @if jp
  # @brief ���֥�������̤ȯ���㳰�������������饹(̤����)
  # @else
  #
  # @endif
  class ObjectNotFound:
    pass


  ##
  # @if jp
  #
  # @brief ���֥���������������̾�κ���(���֥��饹������)
  #
  # ���֥���������������̾�Τ��������뤿��δؿ�<BR>
  # �����֥��饹�Ǥμ���������
  # 
  # @param self
  # @param obj ̾�������оݥ��֥�������
  #
  # @return �����������֥�������̾��
  #
  # @else
  #
  # @endif
  def onCreate(self, obj):
    pass


  ##
  # @if jp
  #
  # @brief ���֥������Ⱥ������̾�β���(���֥��饹������)
  #
  # ���֥������Ⱥ������̾�Τ�������뤿��δؿ�<BR>
  # �����֥��饹�Ǥμ���������
  # 
  # @param self
  # @param obj ̾�β����оݥ��֥�������
  #
  # @else
  #
  # @endif
  def onDelete(self, obj):
    pass



##
# @if jp
#
# @class DefaultNumberingPolicy
# @brief ���֥��������������͡��ߥ󥰡��ݥꥷ��(̿̾��§)�����ѥ��饹
#
# ���֥������Ȥ���������ݤΥ͡��ߥ󥰡��ݥꥷ��(̿̾��§)��������뤿���
# ���饹��
#
# @since 0.4.0
#
# @else
#
# @endif
class DefaultNumberingPolicy(NumberingPolicy):
  """
  """

  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  # 
  # ���󥹥ȥ饯��
  # 
  # @param self
  # 
  # @else
  #
  # @brief virtual destractor
  #
  # @endif
  def __init__(self):
    self._num = 0
    self._objects = []


  ##
  # @if jp
  #
  # @brief ���֥���������������̾�κ���
  #
  # ���֥���������������̾�Τ��������롣
  # �����Ѥߥ��󥹥��󥹤ο��˱�����̾�Τ��������롣
  # 
  # @param self
  # @param obj ̾�������оݥ��֥�������
  #
  # @return �����������֥�������̾��
  #
  # @else
  #
  # @endif
  def onCreate(self, obj):
    self._num += 1

    pos = 0
    try:
      pos = self.find(None)
      self._objects[pos] = obj
      return OpenRTM_aist.otos(pos)
    except NumberingPolicy.ObjectNotFound:
      self._objects.append(obj)
      return OpenRTM_aist.otos(int(len(self._objects) - 1))


  ##
  # @if jp
  #
  # @brief ���֥������Ⱥ������̾�β���
  #
  # ���֥������Ⱥ������̾�Τ�������롣
  # ���֥������Ⱥ�����������Ѥߥ��󥹥��󥹿��򸺻����롣
  # 
  # @param self
  # @param obj ̾�β����оݥ��֥�������
  #
  # @else
  #
  # @endif
  def onDelete(self, obj):
    pos = 0
    try:
      pos = self.find(obj)
    except:
      return

    if (pos < len(self._objects)):
      self._objects[pos] = None
    self._num -= 1


  ##
  # @if jp
  #
  # @brief ���֥������Ȥθ���
  #
  # ���֥������ȥꥹ�Ȥ�����ꤵ�줿���֥������Ȥ򸡺�����
  # �������륪�֥������Ȥ���Ǽ����Ƥ�����ˤϥ���ǥå������֤���
  # 
  # @param self
  # @param obj �����оݥ��֥�������
  #
  # @return ���֥������ȳ�Ǽ����ǥå���
  #
  # @else
  #
  # @endif
  def find(self, obj):
    i = 0
    for obj_ in self._objects:
      if obj_ == obj:
        return i
      i += 1
    raise NumberingPolicy.ObjectNotFound()
       

