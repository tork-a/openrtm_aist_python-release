#!/usr/bin/env python
# -*- coding: euc-jp -*-
  

##
# @file Properties.py
# @brief Property list class (derived from Java Properties)
# @date $Date: $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import sys
import string

import OpenRTM_aist


##
# @if jp
#
# @class Properties
# @brief �ץ�ѥƥ����åȤ�ɽ�����륯�饹
#
# Properties ���饹�ϡ����ѤΥץ�ѥƥ����åȤ�ɽ���� Properties �򥹥ȥ꡼��
# ���ݴɤ����ꡢ���ȥ꡼�फ����ɤ����ꤹ�뤳�Ȥ��Ǥ��롣
# �ץ�ѥƥ��ꥹ�Ȥγƥ���������Ӥ�����б������ͤ�ʸ����ȤʤäƤ��롣
#
# �ץ�ѥƥ��ꥹ�Ȥˤϡ����Ρ֥ǥե�����͡פȤ����̤Υץ�ѥƥ��ꥹ�Ȥ����
# ���Ȥ��Ǥ��롣���Υץ�ѥƥ��ꥹ�Ȥǥץ�ѥƥ����������Ĥ���ʤ��ȡ�����
# 2���ܤΥץ�ѥƥ��ꥹ�Ȥ���������롣 
#
# �ץ�ѥƥ��μ����ˤ� getProperty() ���ץ�ѥƥ��Υ��åȤˤ� setProperty() ��
# ���ä��᥽�åɤ���Ѥ��뤳�Ȥ��侩����롣
#
# �ץ�ѥƥ��򥹥ȥ꡼�����¸����Ȥ����ޤ��ϥ��ȥ꡼�फ����ɤ���Ȥ�
# �ˡ�ISO 8859-1 ʸ�����󥳡��ǥ��󥰤����Ѥ���롣���Υ��󥳡��ǥ��󥰤�
# ľ��ɽ���Ǥ��ʤ�ʸ���ϡ��������Ȥ��Ǥ��ʤ���
#
# ���Υ��饹�ϡ�Java �� Properties ���饹 (java.util.Properties) �Ȥۤ�Ʊ�ͤ�
# �᥽�åɤ���ġ��ޤ��������Ϥ����ե������ Java �� Properties ���饹��
# ���Ϥ����Τȸߴ��������뤬��Unicode ��ޤ��Τϰ������Ȥ��Ǥ��ʤ���
#
# @since 0.4.0
#
# @else
#
# @class Properties
#
# The Properties class represents a persistent set of properties. The
# Properties can be saved to a stream or loaded from a stream. Each key and
# its corresponding value in the property list is a string. 
#
# A property list can contain another property list as its "defaults"; this
# second property list is searched if the property key is not found in the
# original property list. 
#
# Because Properties inherits from Hashtable, the put and putAll methods can
# be applied to a Properties object. Their use is strongly discouraged as 
# they allow the caller to insert entries whose keys or values are not 
# Strings. The setProperty method should be used instead. If the store or 
# save method is called on a "compromised" Properties object that contains a 
# non-String key or value, the call will fail. 
#
# The load and store methods load and store properties in a simple
# line-oriented format specified below. This format uses the ISO 8859-1
# character encoding. Characters that cannot be directly represented in this
# encoding can be written using Unicode escapes ; only a single 'u' character
# is allowed in an escape sequence. The native2ascii tool can be used to
# convert property files to and from other character encodings. 
#
# This class has almost same methods of Java's Properties class. Input and 
# Output stream of this properties are compatible each other except Unicode
# encoded property file.
#
# @endif
class Properties:
  """
  """

  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # �ʲ��ν�˰���������å��������󥹥��󥹤�������Ԥ���
  #
  # ���� prop ���ͤ����ꤵ��Ƥ����硢
  # ������Ϳ����줿 Properties �Υ������ͤ���ӥǥե�����ͤ�
  # ���Ƥ��Τޤޥ��ԡ�����롣
  #
  # ���� key ���ͤ����ꤵ��Ƥ����硢
  # key �� value �Τߤ�Ϳ���� Property �Υ롼�ȥΡ��ɤ�������롣
  # �ͤ����ƥǥե�����ͤȤ������ꤵ��롣
  #
  # ���� defaults_map ���ͤ����ꤵ��Ƥ����硢
  # defaults_map �����ꤵ�줿���Ƥ�ǥե�����ͤˤ�� Properties ��������롣
  # �ͤ����ƥǥե�����ͤȤ������ꤵ��롣
  # 
  # ���� defaults_str ���ͤ����ꤵ��Ƥ����硢
  # ���ꤵ�줿�ǥե�����ͤ���Ķ��Υץ�ѥƥ��ꥹ�Ȥ�������롣
  # �ͤ����ƥǥե�����ͤȤ������ꤵ��롣
  # �ǥե�����ͤ� char* ������ˤ��Ϳ����졢key �� value ���Фˤʤä�
  # ���ꡢ�ꥹ�Ȥν�ü������ο���ɽ������ num ������ʸ���� key ��Ϳ������
  # �ʤ���Фʤ�ʤ���
  # �ʲ�����򼨤���
  #
  # <pre>
  # const char* defaults = {
  #     "key1", "value1",
  #     "key2", "value2",
  #     "key3", "value3",
  #     "key4", "value4",
  #     "key5", "value5",
  #     "" };
  # Properties p(defaults);
  # // �⤷����
  # Properties p(defaults, 10);
  # </pre>
  # 
  # @param self
  # @param key �ץ�ѥƥ��Υ���(�ǥե������:None)
  # @param value �ץ�ѥƥ�����(�ǥե������:None)
  # @param defaults_map �ǥե�����ͤȤ��ƻ��ꤵ���map(�ǥե������:None)
  # @param defaults_str �ǥե�����ͤ���ꤹ������(�ǥե������:None)
  # @param num �ǥե�����ͤ����ꤹ�����ǿ�(�ǥե������:None)
  # @param prop �ǥե�����ͤȤ��ƻ��ꤵ���property(�ǥե������:None)
  # 
  # @else
  #
  # @brief Constructor
  #
  # All of given Properties's keys, values and default values are copied to
  # new Properties.
  #
  # Creates a root node of Property with root's key and value.
  #
  # Creates an Properties with default value of std::string map.
  #
  # Creates an empty property list with the specified defaults.
  # The default values are given by array of char*, which should be pairs
  # of "key" and "value". The end of list is specified by argument "num",
  # which specifies number of array or null character of key.
  # The following is an example.
  #
  # const char* defaults = {
  #     "key1", "value1",
  #     "key2", "value2",
  #     "key3", "value3",
  #     "key4", "value4",
  #     "key5", "value5",
  #     "" };
  # Properties p(defaults);
  # // or
  # Properties p(defaults, 10);
  #
  # @endif
  def __init__(self, key=None, value=None, defaults_map=None, defaults_str=None, num=None, prop=None):
    self.default_value = ""
    self.root = None
    self.empty = ""
    self.leaf = []

    # Properties::Properties(const Properties& prop)
    if prop:
      self.name          = prop.name
      self.value         = prop.value
      self.default_value = prop.default_value

      keys = prop.propertyNames()
      for _key in keys:
        node = None
        node = prop.getNode(_key)
        if node:
          self.setDefault(_key, node.default_value)
          self.setProperty(_key, node.value)
          
      return

    # Properties::Properties(const char* key, const char* value)
    if key:
      self.name = key
      if value is None:
        self.value = ""
      else:
        self.value = value
      return

    self.name  = ""
    self.value = ""

    # Properties::Properties(std::map<std::string, std::string>& defaults)
    if defaults_map:
      #for i in range(len(defaults_map.items())):
      #  self.setDefault(defaults_map.keys()[i], defaults_map.values()[i])
      for key, value in defaults_map.items():
        self.setDefault(key, value)
      return

    if defaults_str:
      if num is None:
        _num = sys.maxint
      else:
        _num = num
      self.setDefaults(defaults_str, _num)
      return


  ##
  # @if jp
  # @brief �����黻��
  # 
  # �����ͤ� Properties �Υ������ͤ���ӥǥե�����ͤ����ƺ�����졢
  # �����ͤ� Properties �Υ������ͤ���ӥǥե�����ͤ����Ƥ��Τޤ�
  # ���ԡ�����롣
  # 
  # @param self
  # @param prop OpenRTM_aist.Properties
  # 
  # @else
  # @brief Assignment operator
  # @param self
  # @param prop OpenRTM_aist.Properties
  # @endif
  def assigmentOperator(self, prop):
    self.clear()
    self.name = prop.name
    self.value = prop.value
    self.default_value = prop.default_value

    keys = prop.propertyNames()

    for key in keys:
      node = None
      node = prop.getNode(key)
      if node:
        self.setDefault(key, node.default_value)
        self.setProperty(key, node.value)

    return self


  ##
  # @if jp
  #
  # @brief �ǥ��ȥ饯��
  #
  # @param self
  #
  # @else
  #
  # @brief Destructor
  #
  # @endif
  def __del__(self):
    self.clear()
    if self.root:
      self.root.removeNode(self.name)
    return

  #============================================================
  # public functions
  #============================================================


  ##
  # @if jp
  # @brief Name �μ���
  #
  # �ץ�ѥƥ���̾�Τ�������롣
  #
  # @param self
  #
  # @return �ץ�ѥƥ�̾
  #
  # @else
  #
  # @endif
  def getName(self):
    return self.name


  ##
  # @if jp
  # @brief �ͤμ���
  #
  # �ץ�ѥƥ����ͤ�������롣
  #
  # @param self
  #
  # @return �ץ�ѥƥ���
  #
  # @else
  #
  # @endif
  def getValue(self):
    return self.value


  ##
  # @if jp
  # @brief �ǥե�����ͤμ���
  #
  # �ץ�ѥƥ��Υǥե�����ͤ�������롣
  #
  # @param self
  #
  # @return �ץ�ѥƥ��ǥե������
  #
  # @else
  #
  # @endif
  def getDefaultValue(self):
    return self.default_value


  ##
  # @if jp
  # @brief �����Ǥμ���
  #
  # �ץ�ѥƥ��λ����Ǥ�������롣
  #
  # @param self
  #
  # @return ������
  #
  # @else
  #
  # @endif
  def getLeaf(self):
    return self.leaf


  ##
  # @if jp
  # @brief �롼�����Ǥμ���
  #
  # �ץ�ѥƥ��Υ롼�����Ǥ�������롣
  #
  # @param self
  #
  # @return �롼������
  #
  # @else
  #
  # @endif
  def getRoot(self):
    return self.root


  ##
  # @if jp
  #
  # @brief ���ꤵ�줿��������ĥץ�ѥƥ��򡢥ץ�ѥƥ��ꥹ�Ȥ���õ��
  #
  # ���ꤵ�줿��������ĥץ�ѥƥ��򡢥ץ�ѥƥ��ꥹ�Ȥ���õ����
  # ���Υ������ץ�ѥƥ��ꥹ�Ȥˤʤ����ϡ��ǥե�����ͤΰ������֤���롣 
  #
  # @param self
  # @param key �ץ�ѥƥ�����
  # @param default �ǥե������(�ǥե������:None)
  #
  # @return ���ꤵ�줿�����ͤ���Ĥ��Υץ�ѥƥ��ꥹ�Ȥ���
  #
  # @else
  #
  # @brief Searches for the property with the specified key in this property
  #
  # Searches for the property with the specified key in this property list.
  # The method returns the default value argument if the property is not 
  # found.
  #
  # @param key the property key
  # @param defaultValue a default value. 
  #
  # @return the value in this property list with the specified key value.
  #
  # @endif
  def getProperty(self, key, default=None):
    if default is None:
      keys = []
      #keys = string.split(key, ".")
      self.split(key, ".", keys)

      node = None
      node = self._getNode(keys, 0, self)
      if node:
        if node.value:
          return node.value
        else:
          return node.default_value
      return self.empty

    else:
      value = self.getProperty(key)
      if value:
        return value
      else:
        return default


  ##
  # @if jp
  # @brief ���ꤵ�줿�������Ф��ƥǥե�����ͤ��������
  #
  # ���ꤵ�줿��������ĥץ�ѥƥ��Υǥե�����ͤ��֤���
  # ���ꤵ�줿��������ĥץ�ѥƥ���¸�ߤ��ʤ����ˤ϶�ʸ�����֤���
  #
  # @param self
  # @param key �ץ�ѥƥ�����
  #
  # @return ���ꤵ�줿�����ͤ���ĥץ�ѥƥ��Υǥե������
  #
  # @else
  # @brief Set value as the default value to specified key's property
  # @endif
  def getDefault(self, key):
    keys = []
    #keys = string.split(key, ".")
    self.split(key, ".", keys)
    node = None
    node = self._getNode(keys, 0, self)
    if node:
      return node.default_value

    return self.empty


  ##
  # @if jp
  #
  # @brief Properties �� value �� key �ˤĤ�����Ͽ����
  #
  # Properties �� value �� key �ˤĤ�����Ͽ���롣
  # ���Ǥ� key ���Ф����ͤ���äƤ����硢����ͤ˸Ť��ͤ��֤���
  #
  # @param self
  # @param key �ץ�ѥƥ��ꥹ�Ȥ����֤���륭��
  # @param value key ���б�������(�ǥե������:None)
  #
  # @return �ץ�ѥƥ��ꥹ�Ȥλ��ꤵ�줿�����������͡����줬�ʤ����� null
  #
  # @else
  #
  # @brief Sets a value associated with key in the property list
  #
  # This method sets the "value" associated with "key" in the property list.
  # If the property list has a value of "key", old value is returned.
  #
  # @param key the key to be placed into this property list.
  # @param value the value corresponding to key. 
  #
  # @return the previous value of the specified key in this property list,
  #         or null if it did not have one.
  #
  #@endif
  def setProperty(self, key, value=None):
    if value is not None:
      keys = []
      #keys = string.split(key, ".")
      self.split(key, ".", keys)
      curr = self
      for _key in keys:
        next = curr.hasKey(_key)
        if next is None:
          next = OpenRTM_aist.Properties(key=_key)
          next.root = curr
          curr.leaf.append(next)
        curr = next
      retval = curr.value
      curr.value = value
      return retval

    else:
      self.setProperty(key, self.getProperty(key))
      prop = self.getNode(key)
      return prop.value


  ##
  # @if jp
  # @brief �ǥե�����ͤ���Ͽ����
  #
  # key �ǻ��ꤵ������Ǥ˥ǥե�����ͤ���Ͽ���롣
  #
  # @param self
  # @param key �ǥե�����ͤ���Ͽ����ץ�ѥƥ��Υ���
  # @param value ��Ͽ�����ǥե������
  #
  # @return ���ꤵ�줿�ǥե������
  #
  # @else
  # @brief Sets a default value associated with key in the property list
  # @endif
  def setDefault(self, key, value):
    keys = []
    self.split(key, ".", keys)
    #keys = string.split(key, ".")

    curr = self
    for _key in keys:
      next = curr.hasKey(_key)
      if next is None:
        next = OpenRTM_aist.Properties(key=_key)
        next.root = curr
        curr.leaf.append(next)
      curr = next
    if value != "" and value[-1] == "\n":
      value = value[0:len(value)-1]
    curr.default_value = value
    return value


  ##
  # @if jp
  # @brief Properties �˥ǥե�����ͤ�ޤȤ����Ͽ����
  #
  # ����ǻ��ꤵ�줿���Ǥ˥ǥե�����ͤ�ޤȤ����Ͽ���롣
  # �ǥե�����ͤ� char* ������ˤ��Ϳ����졢key �� value ���Фˤʤä�
  # ���ꡢ�ꥹ�Ȥν�ü������ο���ɽ������ num ������ʸ���� key ��Ϳ������
  # �ʤ���Фʤ�ʤ���
  # 
  # @param self
  # @param defaults �ǥե�����ͤ���ꤹ������
  # @param num �ǥե�����ͤ����ꤹ�����ǿ�(�ǥե������:None)
  # 
  # @else
  # @brief Sets a default value associated with key in the property list
  # @endif
  def setDefaults(self, defaults, num = None):
    if num is None:
      num = sys.maxint

    i = 0
    len_ = len(defaults)
    while 1:
      if i > num or i > (len_ - 1) or defaults[i] == "":
        break

      key = [defaults[i]]
      value = [defaults[i+1]]

      OpenRTM_aist.eraseHeadBlank(key)
      OpenRTM_aist.eraseTailBlank(key)

      OpenRTM_aist.eraseHeadBlank(value)
      OpenRTM_aist.eraseTailBlank(value)

      self.setDefault(key[0], value[0])

      i +=2



  #============================================================
  # load and save functions
  #============================================================

  ##
  # @if jp
  #
  # @brief ���ꤵ�줿���ϥ��ȥ꡼��ˡ��ץ�ѥƥ��ꥹ�Ȥ���Ϥ���
  #
  # ���ꤵ�줿���ϥ��ȥ꡼��ˡ��ץ�ѥƥ��ꥹ�Ȥ���Ϥ��롣
  # ���Υ᥽�åɤϼ�˥ǥХå����Ѥ����롣
  #
  # @param self
  # @param out ���ϥ��ȥ꡼��
  #
  # @else
  #
  # @brief Prints this property list out to the specified output stream
  #
  # Prints this property list out to the specified output stream.
  # This method is useful for debugging.
  #
  # @param out an output stream.
  #
  # @endif
  def list(self, out):
    self._store(out, "", self)
    return


  ##
  # @if jp
  #
  # @brief ���ϥ��ȥ꡼�फ�饭�������Ǥ��Фˤʤä��ץ�ѥƥ��ꥹ�Ȥ��ɤ߹���
  #
  # ���ϥ��ȥ꡼�फ�饭�������Ǥ��Фˤʤä��ץ�ѥƥ��ꥹ�Ȥ��ɤ߹��ࡣ
  # ���ȥ꡼��ϡ�ISO 8859-1 ʸ�����󥳡��ǥ��󥰤���Ѥ��Ƥ���Ȥߤʤ���롣
  # �ƥץ�ѥƥ��ϡ����ϥ��ȥ꡼��˹�ñ�̤���Ͽ����Ƥ����ΤȤߤʤ��졢
  # �ƹԤϹԶ��ڤ�ʸ�� (\\n��\\r���ޤ��� \\r\\n) �ǽ���롣
  # ���ϥ��ȥ꡼�फ���ɤ߹�����Ԥϡ����ϥ��ȥ꡼��ǥե�����ν�����
  # ã����ޤǽ�������롣
  #
  # ����ʸ�������ιԡ��ޤ��Ϻǽ�������ʸ���� ASCII ʸ�� # �ޤ��� ! �Ǥ���
  # �Ԥ�̵�뤵��롣�Ĥޤꡢ# �ޤ��� ! �ϥ����ȹԤ򼨤���
  #
  # ����Ԥޤ��ϥ����ȹ԰ʳ��Τ��٤ƤιԤϡ��ơ��֥���ɲä����ץ�ѥƥ�
  # �򵭽Ҥ��롣���������Ԥν���꤬ \ �ξ��ϡ����ιԤ�����з�³�ԤȤ���
  # ������ (�����򻲾�)�� �����ϡ��ǽ�������ʸ�����顢�ǽ�� ASCII ʸ��
  # =��:���ޤ��϶���ʸ����ľ���ޤǤΡ�����Τ��٤Ƥ�ʸ�����鹽������롣
  #
  # �����ν����򼨤�ʸ���ϡ����� \ ���դ��뤳�Ȥˤ�ꥭ���˴ޤ�뤳�Ȥ�
  # �Ǥ��롣�����θ��ζ���Ϥ��٤ƥ����åפ���롣
  # �����θ��κǽ�������ʸ���� = �ޤ��� : �Ǥ�����ϡ������Υ�����
  # ̵�뤵�졢���Τ��Ȥζ���ʸ���⤹�٤ƥ����åפ���롣
  # ����Τ���ʳ���ʸ���Ϥ��٤ơ���Ϣ��������ʸ����ΰ����Ȥʤ롣
  # ����ʸ������Ǥϡ�ASCII ���������ץ������� \\t��\\n��\\r��\\\\��\\"��
  # \\'��\\ (�ߵ���ȥ��ڡ���)������� \\uxxxx ��ǧ�����졢ñ�Ȥ�ʸ�����Ѵ�
  # ����롣
  # �ޤ����ԤκǸ��ʸ���� \ �Ǥ�����ϡ����ιԤϸ��ߤιԤη�³�Ȥ���
  # �����롣���ξ�硢\ �ȹԶ��ڤ�ʸ�����˴����졢��³�Ԥ���Ƭ�˶���
  # ����Ф���⤹�٤��˴����졢����ʸ����ΰ����ˤϤʤ�ʤ��� 
  #
  # ���Ȥ��С����� 4 �ԤϤ��줾�쥭�� Truth �ȴ�Ϣ���������� Beauty ��ɽ����
  # 
  # Truth = Beauty <BR>
  # Truth:Beauty <BR>
  # Truth\\t\\t\\t:Beauty <BR>
  #
  # �ޤ������� 3 �Ԥ� 1 �ĤΥץ�ѥƥ���ɽ���� 
  #
  # fruits\\t\\t\\t\\tapple, banana, pear, \ <BR>
  #                                  cantaloupe, watermelon, \ <BR>
  #                                  kiwi, mango <BR>
  # ������ fruits �ǡ��������Ǥ˴�Ϣ�դ�����롣 
  # "apple, banana, pear, cantaloupe, watermelon, kiwi, mango"
  # �ǽ�Ū�ʷ�̤ǥ���ޤΤ��Ȥ�ɬ�����ڡ�����ɽ�������褦�ˡ�
  # �� \ �����˥��ڡ��������롣�Ԥν����򼨤� \ �ȡ���³�Ԥ���Ƭ�ˤ���
  # ������˴����졢¾��ʸ�����ִ�����ʤ��� 
  # �ޤ������� 3 ���ܤ���Ǥϡ������� cheeses �ǡ���Ϣ�������Ǥ�����ʸ����
  # �Ǥ��뤳�Ȥ�ɽ���� 
  #
  # cheeses <BR>
  # �����ϡ�cheeses �ǡ���Ϣ���Ǥ϶���ʸ����Ǥ��뤳�Ȥ���ꤷ�Ƥ��롣 
  #
  # @param self
  # @param inStream ���ϥ��ȥ꡼�� 
  #
  # @else
  #
  # @brief Loads property list consists of key:value from input stream
  #
  # Reads a property list (key and element pairs) from the input stream.
  # The stream is assumed to be using the ISO 8859-1 character encoding; that
  # is each byte is one Latin1 character. Characters not in Latin1, and
  # certain special characters, can be represented in keys and elements using
  # escape sequences similar to those used for character and string literals
  # The differences from the character escape sequences used for characters
  # and strings are: 
  # - Octal escapes are not recognized. 
  # - The character sequence \b does not represent a backspace character. 
  # - The method does not treat a backslash character, \, before a non-valid
  #   escape character as an error; the backslash is silently dropped. For
  #   example, in a Java string the sequence "\z" would cause a compile time
  #   error. In contrast, this method silently drops the backslash. 
  #   Therefore, this method treats the two character sequence "\b" as 
  #   equivalent to the single character 'b'. 
  # - Escapes are not necessary for single and double quotes; however, by the
  #   rule above, single and double quote characters preceded by a backslash
  #   still yield single and double quote characters, respectively. 
  # An IllegalArgumentException is thrown if a malformed Unicode escape
  # appears in the input. 
  #
  # This method processes input in terms of lines. A natural line of input is
  # terminated either by a set of line terminator characters
  # (\n or \r or \r\n) or by the end of the file. A natural line may be 
  # either a blank line, a comment line, or hold some part of a key-element 
  # pair. The logical line holding all the data for a key-element pair may 
  # be spread out across several adjacent natural lines by escaping the line 
  # terminator sequence with a backslash character, \. Note that a comment 
  # line cannot be extended in this manner; every natural line that is a 
  # comment must have its own comment indicator, as described below. If a 
  # logical line is continued over several natural lines, the continuation 
  # lines receive further processing, also described below. Lines are read 
  # from the input stream until end of file is reached. 
  #
  # A natural line that contains only white space characters is considered
  # blank and is ignored. A comment line has an ASCII '#' or '!' as its first
  # non-white space character; comment lines are also ignored and do not
  # encode key-element information. In addition to line terminators, this
  # method considers the characters space (' ', '\u0020'), tab 
  # ('\t', '\u0009'), and form feed ('\f', '\u000C') to be white space. 
  #
  # If a logical line is spread across several natural lines, the backslash
  # escaping the line terminator sequence, the line terminator sequence, and
  # any white space at the start the following line have no affect on the key
  # or element values. The remainder of the discussion of key and element
  # parsing will assume all the characters constituting the key and element
  # appear on a single natural line after line continuation characters have
  # been removed. Note that it is not sufficient to only examine the 
  # character preceding a line terminator sequence to see if the line 
  # terminator is escaped; there must be an odd number of contiguous 
  # backslashes for the line terminator to be escaped. Since the input is 
  # processed from left to right, a non-zero even number of 2n contiguous 
  # backslashes before a line terminator (or elsewhere) encodes n 
  # backslashes after escape processing. 
  #
  # The key contains all of the characters in the line starting with the 
  # first non-white space character and up to, but not including, the first
  # unescaped '=', ':', or white space character other than a line 
  # terminator. All of these key termination characters may be included in 
  # the key by escaping them with a preceding backslash character; 
  # for example,
  #
  # \:\=
  #
  # would be the two-character key ":=". Line terminator characters can be
  # included using \r and \n escape sequences. Any white space after the key
  # is skipped; if the first non-white space character after the key is '=' 
  # or ':', then it is ignored and any white space characters after it are 
  # also skipped. All remaining characters on the line become part of the
  # associated element string; if there are no remaining characters, the
  # element is the empty string "". Once the raw character sequences
  # constituting the key and element are identified, escape processing is
  # performed as described above. 
  #
  # As an example, each of the following three lines specifies the key 
  # "Truth" and the associated element value "Beauty": 
  #
  # Truth = Beauty <BR>
  #        Truth:Beauty <BR>
  # Truth                  :Beauty <BR>
  #  As another example, the following three lines specify a single 
  # property: 
  #
  # fruits                           apple, banana, pear, \ <BR>
  #                                  cantaloupe, watermelon, \ <BR>
  #                                  kiwi, mango <BR>
  # The key is "fruits" and the associated element is: 
  # "apple, banana, pear, cantaloupe, watermelon, kiwi, mango"Note that a
  # space appears before each \ so that a space will appear after each comma
  # in the final result; the \, line terminator, and leading white space on
  # the continuation line are merely discarded and are not replaced by one or
  # more other characters. 
  # As a third example, the line: 
  #
  # cheeses <BR>
  # specifies that the key is "cheeses" and the associated element is the
  # empty string "".
  #
  # @param inStream the input stream.
  #
  # @endif
  def load(self, inStream):
    pline = ""
    for readStr in inStream:
      if not readStr:
        continue
      
      tmp = [readStr]
      OpenRTM_aist.eraseHeadBlank(tmp)
      _str = tmp[0]
      
      if _str[0] == "#" or _str[0] == "!" or _str[0] == "\n":
        continue

      _str = _str.rstrip('\r\n')

      if _str[len(_str)-1] == "\\" and not OpenRTM_aist.isEscaped(_str, len(_str)-1):
        #_str = _str[0:len(_str)-1]
        tmp = [_str[0:len(_str)-1]]
        OpenRTM_aist.eraseTailBlank(tmp)
        #pline += _str
        pline += tmp[0]
        continue
      pline += _str
      if pline == "":
        continue

      key = []
      value = []
      self.splitKeyValue(pline, key, value)
      key[0] = OpenRTM_aist.unescape(key)
      OpenRTM_aist.eraseHeadBlank(key)
      OpenRTM_aist.eraseTailBlank(key)

      value[0] = OpenRTM_aist.unescape(value)
      OpenRTM_aist.eraseHeadBlank(value)
      OpenRTM_aist.eraseTailBlank(value)

      self.setProperty(key[0], value[0])
      pline = ""


  ##
  # @if jp
  #
  # @brief �ץ�ѥƥ��ꥹ�Ȥ���ꤵ�줿���ȥ꡼�����¸����
  #
  # �ץ�ѥƥ��ꥹ�Ȥ���ꤵ�줿���ȥ꡼�����¸���롣
  # ���Υ᥽�åɤ� Java Properties �Ȥθߴ����Τ�����������Ƥ��롣
  # (����Ū�ˤ� store �᥽�åɤ����Ѥ��Ƥ��롣)
  #
  # @param self
  # @param out ���ϥ��ȥ꡼��
  # @param header �ץ�ѥƥ��ꥹ�Ȥε��� 
  #
  # @else
  #
  # @brief Save the properties list to the stream
  #
  # Deprecated. 
  #
  # @param out The output stream
  # @param header A description of the property list
  #
  # @endif
  def save(self, out, header):
    self.store(out, header)
    return


  ##
  # @if jp
  #
  # @brief �ץ�ѥƥ��ꥹ�Ȥ���ϥ��ȥ꡼�����¸����
  #
  # Properties �ơ��֥���Υץ�ѥƥ��ꥹ�� (���������ǤΥڥ�) ��load
  # �᥽�åɤ�Ȥä� Properties �ơ��֥�˥��ɤ���Τ�Ŭ�ڤʥե����ޥåȤ�
  # ���ϥ��ȥ꡼��˽񤭹��ࡣ 
  #
  # Properties �ơ��֥���Υץ�ѥƥ��ꥹ�� (���������ǤΥڥ�) ��load
  # �᥽�åɤ�Ȥä� Properties �ơ��֥�˥��ɤ���Τ�Ŭ�ڤʥե����ޥåȤ�
  # ���ϥ��ȥ꡼��˽񤭹��ࡣ���ȥ꡼��ϡ�ISO 8859-1 ʸ��
  # ���󥳡��ǥ��󥰤���Ѥ��ƽ񤭹��ޤ�롣 
  # Properties �ơ��֥� (¸�ߤ�����) �Υǥե���ȥơ��֥뤫���
  # �ץ�ѥƥ��ϡ����Υ᥽�åɤˤ�äƤϽ񤭹��ޤ�ʤ��� 
  #
  # header ������ null �Ǥʤ����ϡ�ASCII ʸ���� #��header ��ʸ����
  # ����ӹԶ��ڤ�ʸ�����ǽ�˽��ϥ��ȥ꡼��˽񤭹��ޤ�ޤ������Τ��ᡢ
  # header �ϼ��̥����ȤȤ��ƻȤ����Ȥ��Ǥ��롣 
  #
  # ���ˡ�ASCII ʸ���� #�����ߤ����� (Date �� toString �᥽�åɤˤ�ä�
  # ���߻��郎���������Τ�Ʊ��)������� Writer �ˤ�ä����������Զ��ڤ�
  # ����ʤ륳���ȹԤ��񤭹��ޤ�롣 
  #
  # ³���ơ� Properties �ơ��֥���Τ��٤ƤΥ���ȥ꤬ 1 �Ԥ��Ľ񤭽Ф���롣
  # �ƥ���ȥ�Υ���ʸ����ASCII ʸ����=����Ϣ��������ʸ���󤬽񤭹��ޤ�롣
  # ����ʸ����γ�ʸ���ϡ����������ץ������󥹤Ȥ������褹��ɬ�פ����뤫
  # �ɤ�����ǧ����롣ASCII ʸ���� \�����֡����ԡ�����������Ϥ��줾�� \\\\��
  # \\t��\\n������� \\r �Ȥ��ƽ񤭹��ޤ�롣\\u0020 ��꾮����ʸ�������
  # \\u007E ����礭��ʸ���ϡ��б����� 16 ���� xxxx ��Ȥä� \\uxxxx �Ȥ���
  # �񤭹��ޤ�롣�����߶���ʸ���Ǥ��񤭶���ʸ���Ǥ�ʤ���Զ���ʸ���ϡ�
  # ���� \ ���դ��ƽ񤭹��ޤ�롣�������ͤ�ʸ�� #��!��=������� : �ϡ�
  # ɬ�����������ɤ����褦�ˡ����˥���å�����դ��ƽ񤭹��ޤ�롣 
  #
  # ����ȥ꤬�񤭹��ޤ줿���Ȥǡ����ϥ��ȥ꡼�ब�ե�å��夵��롣
  # ���ϥ��ȥ꡼��Ϥ��Υ᥽�åɤ��������������ȤⳫ�����ޤޤȤʤ롣 
  #
  # @param self
  # @param out ���ϥ��ȥ꡼��
  # @param header �ץ�ѥƥ��ꥹ�Ȥε��� 
  #
  # @else
  #
  # @brief Stores property list to the output stream
  #
  # Writes this property list (key and element pairs) in this Properties 
  # table to the output stream in a format suitable for loading into a 
  # Properties table using the load method. The stream is written using the 
  # ISO 8859-1 character encoding. 
  #
  # Properties from the defaults table of this Properties table (if any) are
  # not written out by this method. 
  #
  # If the comments argument is not null, then an ASCII # character, the
  # comments string, and a line separator are first written to the output
  # stream. Thus, the comments can serve as an identifying comment. 
  #
  # Next, a comment line is always written, consisting of an ASCII #
  # character, the current date and time (as if produced by the toString
  # method of Date for the current time), and a line separator as generated
  # by the Writer. 
  #
  # Then every entry in this Properties table is written out, one per line.
  # For each entry the key string is written, then an ASCII =, then the
  # associated element string. Each character of the key and element strings
  # is examined to see whether it should be rendered as an escape sequence.
  # The ASCII characters \, tab, form feed, newline, and carriage return are
  # written as \\, \t, \f \n, and \r, respectively. Characters less than
  # \u0020 and characters greater than \u007E are written as \uxxxx for the
  # appropriate hexadecimal value xxxx. For the key, all space characters are
  # written with a preceding \ character. For the element, leading space
  # characters, but not embedded or trailing space characters, are written
  # with a preceding \ character. The key and element characters #, !, =, and
  # : are written with a preceding backslash to ensure that they are properly
  # loaded. 
  #
  # After the entries have been written, the output stream is flushed. The
  # output stream remains open after this method returns. 
  #
  # @param out an output stream.
  # @param header a description of the property list.
  #
  # @endif
  def store(self, out, header):
    out.write("#"+header+"\n")
    self._store(out, "", self)


  #============================================================
  # other util functions
  #============================================================

  ##
  # @if jp
  #
  # @brief �ץ�ѥƥ��Υ����Υꥹ�Ȥ� vector ���֤�
  #
  # �ᥤ��ץ�ѥƥ��ꥹ�Ȥ�Ʊ��̾���Υ��������Ĥ���ʤ����ϡ��ǥե���Ȥ�
  # �ץ�ѥƥ��ꥹ�Ȥˤ�����̤Υ�����ޤࡢ���Υץ�ѥƥ��ꥹ�Ȥˤ��뤹�٤�
  # �Υ����Υꥹ�Ȥ��֤��� 
  #
  # @param self
  #
  # @return �ץ�ѥƥ��ꥹ�Ȥˤ��뤹�٤ƤΥ����Υꥹ�ȡ�
  #         �ǥե���ȤΥץ�ѥƥ��ꥹ�Ȥˤ��륭����ޤ�
  #
  # @else
  #
  # @brief Returns an vector of all the keys in this property
  #
  # Returns an enumeration of all the keys in this property list, including
  # distinct keys in the default property list if a key of the same name has
  # not already been found from the main properties list.
  #
  # @return an vector of all the keys in this property list, including the
  #         keys in the default property list.
  #
  # @endif
  def propertyNames(self):
    names = []
    for leaf in self.leaf:
      self._propertyNames(names, leaf.name, leaf)
    return names


  ##
  # @if jp
  # @brief �ץ�ѥƥ��ο����������
  #
  # ����ѤߤΥץ�ѥƥ�����������롣
  #
  # @param self
  #
  # @return �ץ�ѥƥ���
  #
  # @else
  # @brief Get number of Properties
  # @endif
  def size(self):
    return len(self.propertyNames())


  ##
  # @if jp
  # @brief �Ρ��ɤ򸡺�����
  # @else
  # @brief Find node of properties
  # @endif
  # Properties* const Properties::findNode(const std::string& key) const
  def findNode(self, key):
    if not key:
      return None

    keys = []
    self.split(key, '.', keys)
    return self._getNode(keys, 0, self)


  ##
  # @if jp
  # @brief �Ρ��ɤ��������
  #
  # ���ꤷ����������ĥΡ��ɤ�������롣
  #
  # @param self
  # @param key �����оݥΡ��ɤΥ���
  #
  # @return �оݥΡ���
  #
  # @else
  # @brief Get node of Properties
  # @endif
  def getNode(self, key):
    if not key:
      return self

    leaf = self.findNode(key)
    if leaf:
      return leaf

    self.createNode(key)
    return self.findNode(key)


  ##
  # @if jp
  # @brief �����Ρ��ɤ���������
  #
  # ���ꤷ����������Ŀ����Ρ��ɤ��������롣
  # ����Ʊ�쥭������ĥΡ��ɤ���Ͽ�Ѥߤξ��ˤϥ��顼���֤���
  #
  # @param self
  # @param key �����Ρ��ɤΥ���
  #
  # @return �����Ρ����������
  #         ���ꤷ����������ĥΡ��ɤ�����¸�ߤ�����ˤ�false
  #
  # @else
  #
  # @endif
  def createNode(self, key):
    if not key:
      return False

    if self.findNode(key):
      return False
    
    self.setProperty(key,"")
    return True


  ##
  # @if jp
  # @brief �Ρ��ɤ�������
  #
  # ���ꤷ��̾�Τ���ĥץ�ѥƥ��������롣
  # ��������ץ�ѥƥ����֤���
  #
  # @param self
  # @param leaf_name ����оݥץ�ѥƥ�̾��
  #
  # @return ��������ץ�ѥƥ�
  #
  # @else
  # @brief Get node of Properties
  # @endif
  def removeNode(self, leaf_name):
    len_ = len(self.leaf)
    for i in range(len_):
      idx = (len_ - 1) - i
      if self.leaf[idx].name == leaf_name:
        prop = self.leaf[idx]
        del self.leaf[idx]
        return prop
    return None


  ##
  # @if jp
  # @brief �ҥΡ��ɤ�key�����뤫�ɤ���
  #
  # ���ꤷ����������ĻҥΡ��ɤ�¸�ߤ��뤫�ɤ�����ǧ���롣
  # ¸�ߤ����硢�ҥΡ��ɤ��֤���
  #
  # @param self
  # @param key ��ǧ�оݤΥ���
  #
  # @return �ҥΡ���
  #
  # @else
  # @brief If key exists in the children
  # @endif
  def hasKey(self, key):
    for leaf in self.leaf:
      if leaf.name == key:
        return leaf

    return None


  ##
  # @if jp
  # @brief �ҥΡ��ɤ����ƺ������
  #
  # @param self
  #
  # @else
  # @brief If key exists in the children
  # @endif
  def clear(self):
    len_ = len(self.leaf)
    for i in range(len_):
      if self.leaf[-1]:
        del self.leaf[-1]

    return


  ##
  # @if jp
  # @brief Property��ޡ�������
  #
  # ���ߤΥץ�ѥƥ������ꤷ���ץ�ѥƥ���ޡ������롣
  #
  # @param self
  # @param prop �ޡ�������ץ�ѥƥ�
  #
  # @return �ץ�ѥƥ��ޡ������
  #
  # @else
  # @brief Merge properties
  # @endif
  def mergeProperties(self, prop):
    keys = prop.propertyNames()

    for i in range(prop.size()):
      self.setProperty(keys[i], prop.getProperty(keys[i]))

    return self


  ##
  # @if jp
  # @brief ʸ����򥭡����ͤΥڥ���ʬ�䤹��
  #
  # Ϳ����줿ʸ��������ꤵ�줿�ǥ�ߥ��ǥ������ͤΥڥ���ʬ�䤹�롣
  # �ޤ��ǽ��Ϳ����줿ʸ�����':'�⤷����'='���ޤޤ�뤫�򸡺�����
  # �ɤ��餫��ʸ�����ޤޤ�Ƥ�����ˤϤ����ǥ�ߥ��Ȥ��ƻ��Ѥ��롣
  # ξ���Ȥ�ޤޤ�Ƥ��ʤ����ˤϡ�' '(���ڡ���)���Ѥ���ʬ����ߤ롣
  # ���ƤΥǥ�ߥ����䤬�ޤޤ�Ƥ��ʤ����ˤϡ�Ϳ����줿ʸ����򥭡��Ȥ���
  # ���ꤷ���ͤ˶���ʸ��������ꤹ�롣
  # �ɤΥǥ�ߥ�����ˤĤ��Ƥ⥨�������פ���Ƥ���(ľ����'\'�����ꤵ��Ƥ���)
  # ���ˤϡ��ǥ�ߥ��Ȥ��ƻ��Ѥ��ʤ���
  #
  # @param self
  # @param _str ʬ���о�ʸ����
  # @param key ʬ���̥���
  # @param value ʬ������
  #
  # @else
  #
  # @endif
  def splitKeyValue(self, _str, key, value):
    i = 0
    length = len(_str)

    while i < length:
      if (_str[i] == ":" or _str[i] == "=") and not OpenRTM_aist.isEscaped(_str, i):
        key.append(_str[0:i])
        value.append(_str[i+1:])
        return
      i += 1

    # If no ':' or '=' exist, ' ' would be delimiter.
    i = 0
    while i < length:
      if (_str[i] == " ") and not OpenRTM_aist.isEscaped(_str, i):
        key.append(_str[0:i])
        value.append(_str[i+1:])
        return
      i += 1

    key.append(_str)
    value.append("")
    return


  ##
  # @if jp
  # @brief ʸ�����ʬ�䤹��
  #
  # Ϳ����줿ʸ�����Ϳ����줿�ǥ�ߥ���ʬ�䤹�롣
  # Ϳ����줿ʸ���󤬶��ξ��ϡ����顼���֤���
  # Ϳ����줿�ǥ�ߥ������������פ���Ƥ���(ľ����'\'�����ꤵ��Ƥ���)���
  # �ˤϡ��ǥ�ߥ��Ȥ��ƻ��Ѥ��ʤ���
  #
  # @param self
  # @param _str ʬ���о�ʸ����
  # @param delim �ǥ�ߥ�
  # @param value ʬ�����ͥꥹ��
  #
  # @return ʬ��������
  #
  # @else
  #
  # @endif
  def split(self, _str, delim, value):
    if _str == "":
      return False

    begin_it = end_it = 0

    length = len(_str)

    while end_it < length:
      if _str[end_it] == delim and not OpenRTM_aist.isEscaped(_str, end_it):
        value.append(_str[begin_it:end_it])
        begin_it = end_it + 1
      end_it += 1

    value.append(_str[begin_it:end_it])
    return True


  ##
  # @if jp
  # @brief �ץ�ѥƥ����������
  #
  # �����ꥹ�Ȥǻ��ꤵ�줿�ץ�ѥƥ���������롣
  # �����ꥹ�ȤǤϡ����ꤹ�륭���Υץ�ѥƥ��Ǥγ��شط���ꥹ�ȷ�����ɽ��
  # ���롣
  # ���ꤷ�������ꥹ�Ȥ˳�������ץ�ѥƥ���¸�ߤ��ʤ�����None���֤���
  #
  # @param self
  # @param keys �����оݥץ�ѥƥ��Υ����Υꥹ��ɽ��
  # @param index �����ꥹ�Ȥγ��ؿ�
  # @param curr �����оݥץ�ѥƥ�
  #
  # @return �����оݥץ�ѥƥ�
  #
  # @else
  #
  # @endif
  def _getNode(self, keys, index, curr):
    next = curr.hasKey(keys[index])
    if next is None:
      return None

    if index < (len(keys) - 1):
      index+=1
      return next._getNode(keys, index, next)
    else:
      return next

    return None


  ##
  # @if jp
  # @brief �ץ�ѥƥ���̾�Υꥹ�Ȥ��������
  #
  # �ץ�ѥƥ���̾�Τ�'.'���ڤ��ɽ�������ꥹ�Ȥ�������롣
  #
  # @param self
  # @param names �ץ�ѥƥ���̾�Υꥹ��
  # @param curr_name ���ߤΥץ�ѥƥ�̾
  # @param curr �оݥץ�ѥƥ�
  #
  # @else
  #
  # @endif
  def _propertyNames(self, names, curr_name, curr):
    if len(curr.leaf) > 0:
      for i in range(len(curr.leaf)):
        next_name = curr_name+"."+curr.leaf[i].name
        self._propertyNames(names, next_name, curr.leaf[i])
    else:
      names.append(curr_name)

    return


  ##
  # @if jp
  # @brief �ץ�ѥƥ���̾�Υꥹ�Ȥ���¸����
  #
  # �ץ�ѥƥ���̾�Τ�'.'���ڤ��ɽ�������ꥹ�Ȥ���¸���롣
  #
  # @param self
  # @param out �ץ�ѥƥ���̾�Υꥹ����¸��ν��ϥ��ȥ꡼��
  # @param curr_name ���ߤΥץ�ѥƥ�̾
  # @param curr �оݥץ�ѥƥ�
  #
  # @else
  #
  # @endif
  def _store(self, out, curr_name, curr):
    if len(curr.leaf) > 0:
      for i in range(len(curr.leaf)):
        if curr_name == "":
          next_name = curr.leaf[i].name
        else:
          next_name = curr_name+"."+curr.leaf[i].name
        self._store(out, next_name, curr.leaf[i])
        
    else:
      val = curr.value
      if val == "":
        val = curr.default_value
      out.write(curr_name+": "+val+"\n")

    return


  ##
  # @if jp
  # @brief ����ǥ�Ȥ���������
  #
  # ���ꤵ�줿�����˽��ä�������������ǥ�Ȥ��֤���
  # �֤���륤��ǥ�Ȥϡ����������2�Ĥζ���
  #
  # @param self
  # @param index ����ǥ�ȿ��λ���
  #
  # @return �������줿����ǥ��
  #
  # @else
  #
  # @endif
  def indent(self, index):
    space = ""

    for i in range(index-1):
      space += "  "

    return space


  ##
  # @if jp
  # @brief �ץ�ѥƥ������Ƥ���¸����
  #
  # �ץ�ѥƥ������ꤵ�줿���Ƥ���¸���롣
  # ��¸���ˤϥץ�ѥƥ����ؤο�����ɽ���������ղä���롣
  # �ͤ����ꤵ��Ƥ��ʤ��ץ�ѥƥ��ˤĤ��Ƥϡ��ǥե�����ͤ����Ϥ���롣
  #
  # @param self
  # @param out �ץ�ѥƥ�������¸��ν��ϥ��ȥ꡼��
  # @param curr �оݥץ�ѥƥ�
  # @param index ���ߤΥץ�ѥƥ�����
  #
  # @else
  #
  # @endif
  def _dump(self, out, curr, index):
    if index != 0:
      #ut.write(self.indent(index)+"- "+curr.name)
      out[0]+=self.indent(index)+"- "+curr.name

    if curr.leaf == []:
      if curr.value == "":
        #out.write(": "+curr.default_value+"\n")
        out[0]+=": "+curr.default_value+"\n"
      else:
        #out.write(": "+curr.value+"\n")
        out[0]+=": "+str(curr.value)+"\n"
      return out[0]

    if index != 0:
      #out.write("\n")
      out[0]+="\n"

    for i in range(len(curr.leaf)):
      self._dump(out, curr.leaf[i], index + 1)

    return out[0]


  ##
  # @if jp
  # @brief �ץ�ѥƥ������Ƥ���Ϥ���
  #
  # �ץ�ѥƥ������ꤵ�줿���Ƥ���Ϥ��롣<br>
  # friend std::ostream& operator<<(std::ostream& lhs, const Properties& rhs);
  # ������ˡ�print obj�ˤƸƤӽФ���ǽ�Ȥ��뤿��Υ᥽�åɡ�
  #
  # @param self
  #
  # @return ����ץ�ѥƥ�ʸ����ɽ��
  #
  # @else
  #
  # @endif
  def __str__(self): 
    string=[""]
    return self._dump(string, self, 0)

  
