#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file StringUtil.py
# @brief String operation utility
# @date $Date: $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2003-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.



import string

##
# @if jp
# @brief ʸ���󤬥��������פ���Ƥ��뤫Ƚ�Ǥ���
#
# ���ꤵ�줿ʸ�������������פ���Ƥ��뤫�ɤ�����Ƚ�Ǥ��롣
#
# @param _str ���������פ���Ƥ��뤫�ɤ���Ƚ�Ǥ���ʸ����ޤ�ʸ����
# @param pos ���������פ���Ƥ��뤫�ɤ���Ƚ�Ǥ���ʸ���ΰ���
#
# @return ���ꤷ��ʸ�������������פ���Ƥ���� true, ����ʳ��� false
#
# @else
# @brief Whether the character is escaped or not
#
# This operation returns true if the specified character is escaped, and
# if the specified character is not escaped, it returns false
#
# @param str The string thath includes the character to be investigated.
# @param pos The position of the character to be investigated.
#
# @return true: the character is escaped, false: the character is not escaped.
#
# @endif
def isEscaped(_str, pos):
  pos -= 1

  i = 0
  while pos >= 0 and _str[pos] == "\\":
    i += 1
    pos -= 1

  return i % 2 == 1


##
# @if jp
# @class escape_functor
# @brief  ʸ���󥨥������׽�����functor
# @else
#
# @endif
class escape_functor:
  def __init__(self):
    self._str = ""

  def __call__(self,c):
    if   c == '\t':
      self._str += "\\t"
    elif c == '\n':
      self._str += "\\n"
    elif c == '\f':
      self._str += "\\f"
    elif c == '\r':
      self._str += "\\r"
    elif c == '\\':
      self._str += "\\\\"
    else:
      self._str += c


##
# @if jp
# @class unescape_functor
# @brief  ʸ���󥢥󥨥������׽�����functor
# @else
#
# @endif
class unescape_functor:
  def __init__(self):
    self.count = 0
    self._str = ""

  def __call__(self,c):
    if c == "\\":
      self.count += 1
      if not (self.count % 2):
        self._str += c
    else:
      if self.count > 0 and (self.count % 2):
        self.count = 0
        if c == 't':
          self._str+='\t'
        elif c == 'n':
          self._str+='\n'
        elif c == 'f':
          self._str+='\f'
        elif c == 'r':
          self._str+='\r'
        elif c == '\"':
          self._str+='\"'
        elif c == '\'':
          self._str+='\''
        else:
          self._str+=c
      else:
        self.count = 0
        self._str+=c


##
# @if jp
# @class unique_strvec
# @brief  ��ʣʸ�����������functor
# @else
#
# @endif
class unique_strvec:
  def __init__(self):
    self._str = []

  def __call__(self,s):
    if self._str.count(s) == 0:
      return self._str.append(s)


##
# @if jp
# @brief  ���󥹥���������functor
# @else
#
# @endif
def for_each(_str, instance):
  for i in _str:
    instance(i)

  return instance


##
# @if jp
# @brief ʸ����򥨥������פ���
# 
# ����ʸ���򥨥������ץ������󥹤��Ѵ����롣<br>
# HT -> "\t" <br>
# LF -> "\n" <br>
# CR -> "\r" <br>
# FF -> "\f" <br>
# ���󥰥륯�����ȡ����֥륯�����ȤˤĤ��ƤϤȤ��˽����Ϥ��ʤ���
# 
# @else
# 
# @brief Escape string
# 
# The following characters are converted. <br>
# HT -> "\t" <br>
# LF -> "\n" <br>
# CR -> "\r" <br>
# FF -> "\f" <br>
# Single quote and dobule quote are not processed.
# 
# @endif
def escape(_str):
  return for_each(_str, escape_functor())._str


##
# @if jp
# @brief ʸ����Υ��������פ��᤹
# 
# ���Υ��������ץ������󥹤�ʸ�����Ѵ����롣<br>
# "\t" -> HT <br>
# "\n" -> LF <br>
# "\r" -> CR <br>
# "\f" -> FF <br>
# "\"" -> "  <br>
# "\'" -> '  <br>
# 
# @else
# 
# @brief Unescape string
# 
# The following characters are converted. <br>
# "\t" -> HT <br>
# "\n" -> LF <br>
# "\r" -> CR <br>
# "\f" -> FF <br>
# "\'" -> '  <br>
# "\"" -> "  <br>
# @endif
def unescape(_str):
  return for_each(_str, unescape_functor())._str


##
# @if jp
# @brief ʸ����ζ���ʸ����������
#
# Ϳ����줿ʸ����ζ���ʸ���������롣
# ����ʸ���Ȥ��ư����Τ�' '(���ڡ���)��'\\t'(����)��
#
# @param str(list) ����ʸ���������ʸ����Υꥹ��
#
# @else
# @brief Erase blank characters of string
#
# Erase blank characters that exist at the head of the given string.
# Space ' 'and tab '\\t' are supported as the blank character.
#
# @param str The target blank characters of string for the erase
#
# @endif
#
def eraseBlank(str):
    if len(str) == 0:
        return
    str[0] = str[0].strip(" ")
    l_str = str[0].split(" ")
    tmp_str = ""
    for s in l_str:
        if s:
            tmp_str+=s.strip(" ")

    tmp_str = tmp_str.strip('\t')
    l_str = tmp_str.split('\t')
    tmp_str = ""
    for s in l_str:
        if s:
            tmp_str+=s.strip('\t')

    str[0] = tmp_str


##
# @if jp
# @brief ʸ�������Ƭ�ζ���ʸ����������
#
# Ϳ����줿ʸ�������Ƭ��¸�ߤ������ʸ���������롣
# ����ʸ���Ȥ��ư����Τ�' '(���ڡ���)��'\\t'(����)��
#
# @param _str ��Ƭ����ʸ���������ʸ����
#
# @else
# @brief Erase the head blank characters of string
# @endif
def eraseHeadBlank(_str):
  _str[0] = _str[0].lstrip('\t ')


##
# @if jp
# @brief ʸ����������ζ���ʸ����������
#
# Ϳ����줿ʸ�����������¸�ߤ������ʸ���������롣
# ����ʸ���Ȥ��ư����Τ�' '(���ڡ���)��'\\t'(����)��
#
# @param _str ��������ʸ���������ʸ����
#
# @else
# @brief Erase the tail blank characters of string
# @endif
def eraseTailBlank(_str):
  #_str[0] = _str[0].rstrip('\t ')
  if _str[0] == "":
    return

  while (_str[0][-1] == " " or _str[0][-1] == '\t') and not isEscaped(_str[0], len(_str[0]) - 1):
    _str[0] = _str[0][:-1]


#
# @if jp
# @brief ʸ���������������
# @else
# @brief Erase the head/tail blank and replace upper case to lower case
# @endif
#
def normalize(_str):
  _str[0] = _str[0].strip().lower()
  return _str[0]


##
# @if jp
# @brief ʸ������֤�������
#
# Ϳ����줿ʸ������Ф��ơ����ꤷ��ʸ�����֤�������Ԥ���
#
# @param str �֤����������о�ʸ����
# @param _from �ִ���ʸ��
# @param _to �ִ���ʸ��
#
# @else
# @brief Replace string
# @endif
def replaceString(str, _from, _to):
  str[0] = str[0].replace(_from, _to)


##
# @if jp
# @brief ʸ�����ʬ��ʸ����ʬ�䤹��
# 
# ���ꤵ�줿ʸ�����Ϳ����줿�ǥ�ߥ���ʬ�䤹�롣
#
# @param input ʬ���о�ʸ����
# @param delimiter ʬ��ʸ����(�ǥ�ߥ�)
#
# @return ʸ����ʬ���̥ꥹ��
#
# @else
# @brief Split string by delimiter
# @endif
def split(input, delimiter):
  if not input:
    return []

  del_result = input.split(delimiter)

  len_ = len(del_result)

  result = []
  for i in range(len_):
    if del_result[i] == "" or del_result[i] == " ":
      continue
      
    str_ = [del_result[i]]
    eraseHeadBlank(str_)
    eraseTailBlank(str_)
    result.append(str_[0])
    
  return result


##
# @if jp
# @brief Ϳ����줿ʸ�����bool�ͤ��Ѵ�����
# 
# ���ꤵ�줿ʸ�����trueɽ��ʸ����falseɽ��ʸ�������Ӥ������η�̤�
# bool�ͤȤ����֤���
# ��Ӥη�̡�trueɽ��ʸ����falseɽ��ʸ����Τɤ���Ȥ���פ��ʤ����ϡ�
# Ϳ����줿�ǥե�����ͤ��֤���
#
# @param _str Ƚ���о�ʸ����
# @param yes trueɽ��ʸ����
# @param no falseɽ��ʸ����
# @param default_value �ǥե������(�ǥե������:None)
# @else
# @brief Convert given string to bool value
# @endif
def toBool(_str, yes, no, default_value=None):
  if default_value is None:
    default_value = True

  _str = _str.upper()
  yes  = yes.upper()
  no   = no.upper()

  if _str.find(yes) != -1:
    return True
  elif (_str.find(no)) != -1:
    return False
  else:
    return default_value

##
# @if jp
# @brief ʸ����ꥹ����ˤ���ʸ���󤬴ޤޤ�뤫�ɤ���
# 
# ��1�����˥���޶��ڤ�Υꥹ�Ȥ���2������õ���о�ʸ�������ꤷ��
# ����ʸ������1��������˴ޤޤ�뤫��Ƚ�Ǥ��롣
#
# @param list �оݥꥹ��
# @param value õ��ʸ����
# @return true: �ޤޤ�롢false: �ޤޤ�ʤ�
#
# @else
# @brief Include if a string is included in string list
# 
# if the second argument is included in the comma separated string
# list of the first argument, This operation returns "true value".
#
# @param list The target comma separated string
# @param value The searched string
# @return true: included, false: not included
#
# @endif
#
#  bool includes(const vstring& list, std::string value,
#                bool ignore_case = true);
def includes(_list, value, ignore_case = True):
  if not (type(_list) == list or type(_list) == str):
    return False

  if type(_list) == str:
    _list = _list.split(",")

  tmp_list = _list
  if ignore_case:
    value = value.lower()
    tmp_list = map((lambda x: x.lower()),_list)
    
  if tmp_list.count(value) > 0:
    return True

  return False
    


##
# @if jp
# @brief Ϳ����줿ʸ�������Хѥ����ɤ�����Ƚ�Ǥ���
#
# Ϳ����줿ʸ�������Хѥ�ɽ���Ǥ��뤫�ɤ�����Ƚ�Ǥ��롣
# ʸ���󤬰ʲ��ξ��ˤ����Хѥ��Ȥ���Ƚ�Ǥ��롣
#  - ��Ƭʸ����'/' (UNIX�ξ��)
#  - ��Ƭ��ʸ��������ե��٥åȡ�'/'��'\\' (Windows�ξ��)
#  - ��Ƭ��ʸ����'\\\\' (Windows�ͥåȥ���ѥ��ξ��)
#
# @param str Ƚ���о�ʸ����
#
# @return ���Хѥ�Ƚ����
#
# @else
# @brief Investigate whether the given string is absolute path or not
# @endif
def isAbsolutePath(str):
  if str[0] == "/":
    return True
  if str[0].isalpha() and str[1] == ":" and str[2] == "\\":
    return True
  if str[0] == "\\" and str[1] == "\\":
    return True

  return False


##
# @if jp
# @brief Ϳ����줿ʸ����URL���ɤ�����Ƚ�Ǥ���
#
# Ϳ����줿ʸ����URLɽ�����ɤ�����Ƚ�Ǥ��롣
# Ϳ����줿ʸ������ˡ�'://'�Ȥ���ʸ���󤬴ޤޤ�Ƥ�����ˤ�
# URLɽ���Ȥ���Ƚ�Ǥ��롣
#
# @param str Ƚ���о�ʸ����
#
# @return URLȽ����
#
# @else
# @brief Investigate whether the given string is URL or not
# @endif
def isURL(str):
  pos = 0
  if str == "":
    return False

  pos = str.find(":")
  if pos != 0 and pos != -1 and str[pos+1] == "/" and str[pos+2] == "/":
    return True

  return False


##
# @if jp
# @brief Ϳ����줿���֥������Ȥ�ʸ������Ѵ�
#
# �����ǻ��ꤵ�줿���֥������Ȥ�ʸ������Ѵ����롣
#
# @param n �Ѵ��оݥ��֥�������
#
# @return ʸ�����Ѵ����
#
# @else
# @brief Convert the given object to st::string.
# @endif
def otos(n):
  if type(n) == int or type(n) == str or type(n) == long or type(n) == float:
    return str(n)



##
# @if jp
# @brief Ϳ����줿ʸ�����ꥹ�Ȥ��Ѵ�
#
# �����ǻ��ꤵ�줿ʸ�����,����ʬ�䤷���ꥹ�Ȥ��Ѵ����롣
#
# @param _type �Ѵ���̥ꥹ��
# @param _str �Ѵ���ʸ����
#
# @return �ꥹ���Ѵ��������
#
# @else
# 
# @endif
def _stringToList(_type, _str):
  list_ = split(_str,",")
  len_ = len(list_)

  if len(_type[0]) < len(list_):
    sub = len(list_) - len(_type[0])
    for i in range(sub):
      _type[0].append(_type[0][0])
  elif len(_type[0]) > len(list_):
    sub = len(_type[0]) - len(list_)
    for i in range(sub):
      del _type[0][-1]

  for i in range(len_):
    str_ = [list_[i]]
    eraseHeadBlank(str_)
    eraseTailBlank(str_)
    list_[i] = str_[0]

  for i in range(len(list_)):
    if type(_type[0][i]) == int:
      _type[0][i] = int(list_[i])
    elif type(_type[0][i]) == long:
      _type[0][i] = long(list_[i])
    elif type(_type[0][i]) == float:
      _type[0][i] = float(list_[i])
    elif type(_type[0][i]) == str:
      _type[0][i] = str(list_[i])
    else:
      return False

  return True


##
# @if jp
# @brief Ϳ����줿ʸ����򥪥֥������Ȥ��Ѵ�
#
# ������Ϳ����줿ʸ�������ꤵ�줿���֥������Ȥ��Ѵ����롣
#
# @param _type �Ѵ��襪�֥�������
# @param _str �Ѵ���ʸ����
#
# @return �Ѵ������¹Է��
#
# @else
# @brief Convert the given object to st::string.
# @endif
def stringTo(_type, _str):
  if not _str:
    return False

  if type(_type[0]) == int:
    _type[0] = int(_str)
    return True
  elif type(_type[0]) == long:
    _type[0] = long(_str)
    return True
  elif type(_type[0]) == float:
    _type[0] = float(_str)
    return True
  elif type(_type[0]) == list:
    return _stringToList(_type, _str)
  elif type(_type[0]) == str:
    _type[0] = str(_str)
    return True
  
  return False


##
# @if jp
# @brief Ϳ����줿ʸ����ꥹ�Ȥ����ʣ����
#
# ������Ϳ����줿ʸ����ꥹ�Ȥ����ʣ���������ꥹ�Ȥ�������롣
#
# @param sv ��ǧ��ʸ����ꥹ��
#
# @return ��ʣ���������̥ꥹ��
#
# @else
#
# @endif
def unique_sv(sv):
  return for_each(sv, unique_strvec())._str


##
# @if jp
# @brief Ϳ����줿ʸ����ꥹ�Ȥ���CSV������
#
# ������Ϳ����줿ʸ����ꥹ�Ȥγ����Ǥ��¤٤�CSV���������롣
# ʸ����ꥹ�Ȥ����ξ��ˤ϶���ʸ�����֤���
#
# @param sv CSV�Ѵ��о�ʸ����ꥹ��
#
# @return CSV�Ѵ����ʸ����
#
# @else
#
# @endif
def flatten(sv):
  if len(sv) == 0:
    return ""

  _str = ", ".join(sv)

  return _str


##
# @if jp
# @brief Ϳ����줿ʸ����ꥹ�Ȥ�����ꥹ�Ȥ��Ѵ�
#
# ������Ϳ����줿ʸ����ꥹ�Ȥγ�����������'\\0'��ä���
# �����ꥹ�Ȥ��Ѵ����롣<br>
# ���ܥ⥸�塼��Ǥϰ����򤽤Τޤ��֤�
#
# @param args �Ѵ��о�ʸ����ꥹ��
#
# @return �����Ѵ����ʸ����
#
# @else
#
# @endif
def toArgv(args):
  return args
