#!/usr/bin/env python
# -*- coding: euc-jp -*- 

##
# @file NVUtil.py
# @brief NameValue and NVList utility functions
# @date $Date: 2007/09/11$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import sys
import traceback
from omniORB import any

import OpenRTM_aist
import SDOPackage, SDOPackage__POA


##
# @if jp
#
# @brief NameValue ����������
#
# ���Υ��ڥ졼������NameValue��������롣
#
# @param name NameValue �� name
# @param value NameValue �� value
#
# @return NameValue
#
# @else
#
# @brief Create NameVale
#
# This operation creates NameVale.
#
# @param name name of NameValue
# @param value value of NameValue
#
# @return NameValue
#
# @endif
def newNV(name, value):
  try:
    any_val = any.to_any(value)
  except:
    print "ERROR  NVUtil.newNV : Can't convert to any. ", type(value)
    raise

    
  nv = SDOPackage.NameValue(name, any_val)
  return nv


##
# @if jp
#
# @brief Properties �� NVList �إ��ԡ�����
#
# ���Υ��ڥ졼������ Properties �� NVList �إ��ԡ����롣
# NVList �� value ������ CORBA::string ���Ȥ��ƥ��ԡ����롣
#
# @param nv Properties ���ͤ��Ǽ���� NVList
# @param prop ���ԡ����� Properties
#
# @else
#
# @brief Copy to NVList from Proeprties
#
# This operation copies Properties to NVList.
# Created NVList's values are CORBA::string.
#
# @param nv NVList to store Properties values
# @param prop Properties that is copies from
#
# @endif
# void copyFromProperties(SDOPackage::NVList& nv, const coil::Properties& prop);
def copyFromProperties(nv, prop):
  keys = prop.propertyNames()
  keys_len = len(keys)
  nv_len = len(nv)
  if nv_len > 0:
    for i in range(nv_len):
      del nv[-1]

  for i in range(keys_len):
    nv.append(newNV(keys[i], prop.getProperty(keys[i])))


##
# @if jp
#
# @brief NVList �� Properties �إ��ԡ�����
#
# ���Υ��ڥ졼������ NVList �� Properties �إ��ԡ����롣
#
# @param prop NVList ���ͤ��Ǽ���� Properties
# @param nv ���ԡ����� NVList
#
# @else
#
# @brief Copy to Proeprties from NVList
#
# This operation copies NVList to Properties.
#
# @param prop Properties to store NVList values
# @param nv NVList that is copies from
#
# @endif
# void copyToProperties(coil::Properties& prop, const SDOPackage::NVList& nv);
def copyToProperties(prop, nvlist):
  for nv in nvlist:
    try:
      val = str(any.from_any(nv.value, keep_structs=True))
      prop.setProperty(str(nv.name),val)
    except:
      print OpenRTM_aist.Logger.print_exception()
      pass



##
# @if jp
# @class to_prop
# @brief NVList �� Properties �Ѵ��ѥե��󥯥�
# @endif
class to_prop:
  def __init__(self):
    self._prop = OpenRTM_aist.Properties()
    
  def __call__(self, nv):
    self._prop.setProperty(nv.name, nv.value)



##
# @if jp
#
# @brief NVList �� Properties ���Ѵ�����
#
# ���Υ��ڥ졼������ NVList �� Properties ���Ѵ����롣
#
# @param nv �Ѵ����� NVList
#
# @return �Ѵ����Property
#
# @else
#
# @endif
# coil::Properties toProperties(const SDOPackage::NVList& nv);
def toProperties(nv):
  p = OpenRTM_aist.CORBA_SeqUtil.for_each(nv, to_prop())
  return p._prop



##
# @if jp
# @class nv_find
# @brief NVList �����ѥե��󥯥�
# @endif
class nv_find:
  """
  """

  def __init__(self, name):
    self._name = name

  def __call__(self, nv):
    return str(self._name) == str(nv.name)


##
# @if jp
#
# @brief NVList ���� name �ǻ��ꤵ�줿 value ���֤�
#
# ���Υ��ڥ졼������ name �ǻ��ꤵ�줿 value �� Any �����֤���
# ���ꤷ��̾�Τ����Ǥ�¸�ߤ��ʤ������㳰��ȯ�������롣
#
# @param nv �����оݤ� NVList
# @param name ��������̾��
#
# @return �������
#
# @else
#
# @brief Get value in NVList specified by name
#
# This operation returns Any type of value specified by name.
# Created NVList's values are CORBA::string.
#
# @param nv NVList to be searched
# @param prop name to seartch in NVList
#
# @endif
def find(nv, name):
  index = OpenRTM_aist.CORBA_SeqUtil.find(nv, nv_find(name))

  if index < 0:
    raise "Not found."

  return nv[index].value


##
# @if jp
#
# @brief name �ǻ��ꤵ�줿���ǤΥ���ǥå������֤�
#
# ���Υ��ڥ졼������ name �ǻ��ꤵ�줿���Ǥ���Ǽ����Ƥ�����֤�
# ����ǥå������֤���
#
# @param nv �����оݤ� NVList
# @param name ��������̾��
#
# @return �����оݤΥ���ǥå���
#
# @else
#
# @endif
def find_index(nv, name):
  return OpenRTM_aist.CORBA_SeqUtil.find(nv, nv_find(name))


##
# @if jp
#
# @brief ���ꤵ�줿 name �� value �η��� string �Ǥ��뤫���ڤ���
#
# ���Υ��ڥ졼������ name �ǻ��ꤵ�줿 value �η��� CORBA::string
# ���ɤ����� bool �ͤ��֤���
#
# @param nv �����оݤ� NVList
# @param name ��������̾��
#
# @return string���ڷ��(string:true������ʳ�:false)
#
# @else
#
# @endif
def isString(nv, name):
  try:
    value = find(nv, name)
    val = any.from_any(value, keep_structs=True)
    return type(val) == str
  except:
    return False


##
# @if jp
#
# @brief ���ꤵ�줿 name �� value �η������ꤷ��ʸ����Ȱ��פ��뤫���ڤ���
#
# ���Υ��ڥ졼������ name �ǻ��ꤵ�줿 value �η��� CORBA::string
# ���ɤ�����Ƚ�Ǥ���  CORBA::string �Ǥ�����ˤϻ��ꤷ��ʸ����Ȱ��פ��뤫
# ��bool �ͤ��֤���
#
# @param nv �����оݤ� NVList
# @param name ��������̾��
# @param value ����о�ʸ����
#
# @return ���ڷ��(ʸ����Ȱ���:true�������:false)
#
# @else
#
# @endif
def isStringValue(nv, name, value):
  if isString(nv, name):
    if toString(nv, name) == value:
      return True
  return False


##
# @if jp
#
# @brief ���ꤵ�줿 name �� NVList �� string �Ȥ����֤���
#
# ���Υ��ڥ졼������ name �ǻ��ꤵ�줿 NVList ���ͤ� string ���֤���
# �⤷��name �ǻ��ꤷ�� value ���ͤ� CORBA::string �Ǥʤ���С�
# ����ʸ�����string���֤���
#
# @param nv �����оݤ� NVList
# @param name ��������̾��
#
# @return name ���б������ͤ�string������
#
# @else
#
# @brief Get string value in NVList specified by name
#
# This operation returns string value in NVList specified by name.
# If the value in NVList specified by name is not CORBA::string type
# this operation returns empty string value.
#
# @param nv NVList to be searched
# @param name name to to serach
#
# @return string value named by name
#
# @endif
def toString(nv, name=None):
  if not name:
    str_ = [""]
    return dump_to_stream(str_, nv)

  str_value = ""
  try:
    ret_value = find(nv, name)
    val = any.from_any(ret_value, keep_structs=True)
    if type(val) == str:
      str_value = val
  except:
    print OpenRTM_aist.Logger.print_exception()
    pass
  
  return str_value


##
# @if jp
#
# @brief ���ꤵ�줿ʸ����� NVList �����Ǥ��ɲä��롣
#
# ���Υ��ڥ졼������ name �ǻ��ꤵ�줿���Ǥ� value �ǻ��ꤵ�줿ʸ�����
# �ɲä��롣
# name �ǻ��ꤷ�����Ǥ˴��� value ���ͤ����ꤵ��Ƥ�����ˤϲ��⤷�ʤ���
# name �ǻ��ꤷ�����Ǥ� value ���ͤ����ꤵ��Ƥ��ʤ����ϡ� ��,�����ڤ��
# value ���ͤ��ɲä��롣
# ���ꤵ�줿�ͤ����ꤹ�롣
# name �ǻ��ꤷ�����Ǥ�¸�ߤ��ʤ����ϡ� NVList �κǸ�˿��������Ǥ��ɲä���
# ���ꤵ�줿�ͤ����ꤹ�롣
#
# @param nv �����оݤ� NVList
# @param name �ɲ��о�����̾
# @param value �ɲä���ʸ����
#
# @return �ɲ������
#
# @else
#
# @endif
def appendStringValue(nv, name, value):
  index = find_index(nv, name)
  if index >= 0:
    tmp_str = nv[index].value.value()
    values = OpenRTM_aist.split(tmp_str,",")
    find_flag = False
    for val in values:
      if val == value:
        find_flag = True

    if not find_flag:
      tmp_str += ", "
      tmp_str += value
      nv[index].value = any.to_any(tmp_str)
  else:
    OpenRTM_aist.CORBA_SeqUtil.push_back(nv, newNV(name, value))

  return True


##
# @if jp
#
# @brief NVList �����Ǥ��ɲä��롣
#
# ���Υ��ڥ졼������ dest �ǻ��ꤵ�줿 NVList �� src �ǻ��ꤵ�줿���Ǥ�
# �ɲä��롣
#
# @param dest �ɲä���� NVList
# @param src �ɲä��� NVList
#
# @else
#
# @endif
def append(dest, src):
  for i in range(len(src)):
    OpenRTM_aist.CORBA_SeqUtil.push_back(dest, src[i])


##
# @if jp
# @brief NVList �����ꤵ��Ƥ������Ƥ�ʸ����Ȥ��ƽ��Ϥ��롣
# @else
# @brief Print information configured in NVList as a string type
# @endif
# std::ostream& dump_to_stream(std::ostream& out, const SDOPackage::NVList& nv)
def dump_to_stream(out, nv):
  for i in range(len(nv)):
    val = any.from_any(nv[i].value, keep_structs=True)
    if type(val) == str:
	    out[0] += (nv[i].name + ": " + str(nv[i].value) + "\n")
    else:
	    out[0] += (nv[i].name + ": not a string value \n")

  return out[0]


##
# @if jp
#
# @brief NVList �����ꤵ��Ƥ������Ƥ�ʸ����Ȥ��ƽ��Ϥ��롣
#
# ���ꤵ�줿 NVList �����ꤵ�줿���Ƥ�ʸ����Ȥ��ƽ��Ϥ��롣
# �ʤ������ꤵ��Ƥ������Ǥ�ʸ���󷿰ʳ��ξ��ˤϡ����λ�(ʸ����ǤϤʤ�)��
# ���Ϥ��롣
#
# @param nv �����о� NVList
#
# @else
#
# @endif
def dump(nv):
  out = [""]
  print dump_to_stream(out, nv)
