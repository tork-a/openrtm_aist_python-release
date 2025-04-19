#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# \file CorbaNaming.py
# \brief CORBA naming service helper class
# \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import omniORB.CORBA as CORBA
import CosNaming
import string
import sys
import traceback

##
# @if jp
# @class CorbaNaming
# @brief CORBA Naming Service �إ�ѡ����饹
#
# ���Υ��饹�ϡ�CosNaming::NamingContext ���Ф����åѡ����饹�Ǥ��롣
# CosNaming::NamingContext �����ĥ��ڥ졼�����Ȥۤ�Ʊ����ǽ��
# ���ڥ졼�������󶡤���ȤȤ�ˡ��͡��ॳ��ݡ��ͥ�� CosNaming::Name
# �������ʸ����ˤ��̾��ɽ��������դ��륪�ڥ졼�������󶡤��롣
#
# ���֥������Ȥ������������뤤������ľ��� CORBA �͡��ॵ���Ф���³��
# �ʸ塢���Υ͡��ॵ���ФΥ롼�ȥ���ƥ����Ȥ��Ф��Ƽ�Υ��ڥ졼�����
# ��������롣
# �������ؤΥ͡��ߥ󥰥���ƥ����Ȥκ����䥪�֥������ȤΥХ���ɤˤ����ơ�
# ����Υ���ƥ����Ȥ�¸�ߤ��ʤ����Ǥ⡢����Ū�˥���ƥ����Ȥ�Х����
# ����Ū�Υ���ƥ����Ȥ䥪�֥������ȤΥХ���ɤ�Ԥ����Ȥ�Ǥ��롣
#
# @since 0.4.0
#
# @else
# @class CorbaNaming
# @brief CORBA Naming Service helper class
#
# This class is a wrapper class of CosNaming::NamingContext.
# Almost the same operations which CosNaming::NamingContext has are
# provided, and some operation allows string naming representation of
# context and object instead of CosNaming::Name.
#
# The object of the class would connect to a CORBA naming server at
# the instantiation or immediately after instantiation.
# After that the object invokes operations to the root context of it.
# This class realizes forced binding to deep NamingContext, without binding
# intermediate NamingContexts explicitly.
#
# @since 0.4.0
#
# @endif
class CorbaNaming:
  """
  """



  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # @param self
  # @param orb ORB
  # @param name_server �͡��ॵ���Ф�̾��(�ǥե������:None)
  #
  # @else
  #
  # @brief Consructor
  #
  # @endif
  def __init__(self, orb, name_server=None):
    self._orb = orb
    self._nameServer = ""
    self._rootContext = CosNaming.NamingContext._nil
    self._blLength = 100

    if name_server:
      self._nameServer = "corbaloc::" + name_server + "/NameService"
      try:
        obj = orb.string_to_object(self._nameServer)
        self._rootContext = obj._narrow(CosNaming.NamingContext)
        if CORBA.is_nil(self._rootContext):
          print "CorbaNaming: Failed to narrow the root naming context."

      except CORBA.ORB.InvalidName:
        self.__print_exception()
        print "Service required is invalid [does not exist]."

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


  ##
  # @if jp
  #
  # @brief �͡��ߥ󥰥����ӥ��ν����
  # 
  # ���ꤵ�줿�͡��ॵ���о�Υ͡��ߥ󥰥����ӥ����������ޤ���
  # 
  # @param self
  # @param name_server �͡��ॵ���Ф�̾��
  # 
  # @else
  # 
  # @endif
  def init(self, name_server):
    self._nameServer = "corbaloc::" + name_server + "/NameService"
    obj = self._orb.string_to_object(self._nameServer)
    self._rootContext = obj._narrow(CosNaming.NamingContext)
    if CORBA.is_nil(self._rootContext):
      raise MemoryError

    return


  ##
  # @if jp
  #
  # @brief �롼�ȥ���ƥ����Ȥ���¸���Ƥ��뤫���֤���
  # 
  # �롼�ȥ���ƥ����Ȥ���¸���Ƥ��뤫�Υ����å���Ԥ���
  # 
  # @param self
  # @else
  # @brief Check on whether the root context is alive.
  # Check on whether the root context is alive.
  # @param self
  # @endif
  # bool CorbaNaming::isAlive()
  def isAlive(self):
    try:
      if self._rootContext._non_existent():
        return False
      return True
    except:
      self.__print_exception()
      return False

    return False


  ##
  # @if jp
  #
  # @brief Object �� bind ����
  #
  # CosNaming::bind() �Ȥۤ�Ʊ����Ư���򤹤뤬�����Ϳ����줿�͡��ॵ���Ф�
  # �롼�ȥ���ƥ����Ȥ��Ф���bind()���ƤӽФ���������ۤʤ롣
  #
  # Name <name> �� Object <obj> ������ NamingContext ��˥Х���ɤ��롣
  # c_n �� n ���ܤ� NameComponent �򤢤�魯�Ȥ���ȡ�
  # name �� n �Ĥ� NameComponent ��������Ȥ����ʲ��Τ褦�˰����롣
  #
  # cxt->bind(<c_1, c_2, ... c_n>, obj) �ϰʲ�������Ʊ���Ǥ��롣
  # cxt->resolve(<c_1, ... c_(n-1)>)->bind(<c_n>, obj)
  #
  # ���ʤ����1���ܤ���n-1���ܤΥ���ƥ����Ȥ��褷��n-1���ܤΥ���ƥ�����
  # ��� name <n> �Ȥ��ơ�obj �� bind ���롣
  # ̾�����˻��ä��� <c_1, ... c_(n-1)> �� NemingContext �ϡ�
  # bindContext() �� rebindContext() �Ǵ��˥Х���ɺѤߤǤʤ���Фʤ�ʤ���
  # �⤷ <c_1, ... c_(n-1)> �� NamingContext ��¸�ߤ��ʤ����ˤϡ�
  # NotFound �㳰��ȯ�����롣
  #
  # �������������Х���ɥե饰 force �� true �λ��ϡ�<c_1, ... c_(n-1)>
  # ��¸�ߤ��ʤ����ˤ⡢�Ƶ�Ū�˥���ƥ����Ȥ�Х���ɤ��ʤ��顢
  # �ǽ�Ū�� obj ��̾�� name <c_n> �˥Х���ɤ��롣
  #
  # ������ξ��Ǥ⡢n-1���ܤΥ���ƥ����Ⱦ�� name<n> �Υ��֥�������
  # (Object ���뤤�� ����ƥ�����) ���Х���ɤ���Ƥ����
  # AlreadyBound �㳰��ȯ�����롣
  #
  # @param self
  # @param name_list ���֥������Ȥ��դ���̾���� NameComponent
  # @param obj ��Ϣ�դ����� Object
  # @param force true�ξ�硢����Υ���ƥ����Ȥ���Ū�˥Х���ɤ���
  #              (�ǥե������:None)
  #
  # @exception NotFound ����� <c_1, c_2, ..., c_(n-1)> ��¸�ߤ��ʤ���
  # @exception CannotProceed ���餫����ͳ�ǽ������³�Ǥ��ʤ���
  # @exception InvalidName ���� name_list ��̾����������
  # @exception AlreadyBound name <c_n> �� Object �����Ǥ˥Х���ɤ���Ƥ��롣
  #
  # @else
  #
  # @brief
  #
  # @endif
  def bind(self, name_list, obj, force=None):
    if force is None :
      force = True

    try:
      self._rootContext.bind(name_list, obj)
    except CosNaming.NamingContext.NotFound:
      if force:
        self.bindRecursive(self._rootContext, name_list, obj)
      else:
        raise
    except CosNaming.NamingContext.CannotProceed, err:
      if force:
        self.bindRecursive(err.cxt, err.rest_of_name, obj)
      else:
        raise
    except CosNaming.NamingContext.AlreadyBound:
      self._rootContext.rebind(name_list, obj)


  ##
  # @if jp
  #
  # @brief Object �� bind ����
  #
  # Object �� bind ����ݤ�Ϳ����̾����ʸ����ɽ���Ǥ��뤳�Ȱʳ��ϡ�bind()
  # ��Ʊ���Ǥ��롣bind(toName(string_name), obj) ��������
  #
  # @param self
  # @param string_name ���֥������Ȥ��դ���̾����ʸ����ɽ��
  # @param obj ��Ϣ�դ����륪�֥�������
  # @param force true�ξ�硢����Υ���ƥ����Ȥ���Ū�˥Х���ɤ���
  #              (�ǥե������:true)
  #
  # @exception NotFound ����� <c_1, c_2, ..., c_(n-1)> ��¸�ߤ��ʤ���
  # @exception CannotProceed ���餫����ͳ�ǽ������³�Ǥ��ʤ���
  # @exception InvalidName ���� string_name ��̾����������
  # @exception AlreadyBound name <n> �� Object �����Ǥ˥Х���ɤ���Ƥ��롣
  #
  # @else
  #
  # @brief
  #
  # @endif
  def bindByString(self, string_name, obj, force=True):
    self.bind(self.toName(string_name), obj, force)


  ##
  # @if jp
  #
  # @brief ����Υ���ƥ����Ȥ� bind ���ʤ��� Object �� bind ����
  #
  # context ��Ϳ����줿 NamingContext ���Ф��ơ�name �ǻ��ꤵ�줿
  # �͡��ॳ��ݡ��ͥ�� <c_1, ... c_(n-1)> �� NamingContext �Ȥ���
  # ��褷�ʤ��顢̾�� <c_n> ���Ф��� obj �� bind ���롣
  # �⤷��<c_1, ... c_(n-1)> ���б����� NamingContext ���ʤ����ˤ�
  # ������ NamingContext ��Х���ɤ��롣
  #
  # �ǽ�Ū�� <c_1, c_2, ..., c_(n-1)> ���б����� NamingContext ������
  # �ޤ��ϲ�褵�줿��ǡ�CosNaming::bind(<c_n>, object) ���ƤӽФ���롣
  # ���ΤȤ������Ǥ˥Х���ǥ��󥰤�¸�ߤ���� AlreadyBound�㳰��ȯ�����롣
  #
  # ����Υ���ƥ����Ȥ��褹������ǡ���褷�褦�Ȥ��륳��ƥ����Ȥ�
  # Ʊ��̾���� NamingContext �ǤϤʤ� Binding ��¸�ߤ����硢
  # CannotProceed �㳰��ȯ������������ߤ��롣
  #
  # @param self
  # @param context bind �򳫻Ϥ��롡NamingContext
  # @param name_list ���֥������Ȥ��դ���̾���Υ͡��ॳ��ݡ��ͥ��
  # @param obj ��Ϣ�դ����륪�֥�������
  #
  # @exception CannotProceed <c_1, ..., c_(n-1)> ���б����� NamingContext 
  #            �Τ����ҤȤĤ������Ǥ� NamingContext �ʳ��� object �˥Х����
  #            ����Ƥ��ꡢ�������³�Ǥ��ʤ���
  # @exception InvalidName ̾�� name_list ������
  # @exception AlreadyBound name <c_n> �ˤ��Ǥ˲��餫�� object ���Х����
  #            ����Ƥ��롣
  # @else
  #
  # @brief
  #
  # @endif
  def bindRecursive(self, context, name_list, obj):
    length = len(name_list)
    cxt = context
    for i in range(length):
      if i == length -1:
        try:
          cxt.bind(self.subName(name_list, i, i), obj)
        except CosNaming.NamingContext.AlreadyBound:
          cxt.rebind(self.subName(name_list, i, i), obj)
        return
      else:
        if self.objIsNamingContext(cxt):
          cxt = self.bindOrResolveContext(cxt,self.subName(name_list, i, i))
        else:
          raise CosNaming.NamingContext.CannotProceed(cxt, self.subName(name_list, i))
    return


  ##
  # @if jp
  #
  # @brief Object �� rebind ����
  #
  # name_list �ǻ��ꤵ�줿 Binding �����Ǥ�¸�ߤ����������� bind() ��Ʊ��
  # �Ǥ��롣�Х���ǥ��󥰤����Ǥ�¸�ߤ�����ˤϡ��������Х���ǥ��󥰤�
  # �֤��������롣
  #
  # @param self
  # @param name_list ���֥������Ȥ��դ���̾���� NameComponent
  # @param obj ��Ϣ�դ����륪�֥�������
  # @param force true�ξ�硢����Υ���ƥ����Ȥ���Ū�˥Х���ɤ���
  #              (�ǥե������:true)
  #
  # @exception NotFound ����� <c_1, c_2, ..., c_(n-1)> ��¸�ߤ��ʤ���
  # @exception CannotProceed ���餫����ͳ�ǽ������³�Ǥ��ʤ���
  # @exception InvalidName ̾�� name_list ������
  #
  # @else
  #
  # @brief
  #
  # @endif
  def rebind(self, name_list, obj, force=True):
    if force is None:
      force = True
      
    try:
      self._rootContext.rebind(name_list, obj)

    except CosNaming.NamingContext.NotFound:
      if force:
        self.rebindRecursive(self._rootContext, name_list, obj)
      else:
        self.__print_exception()
        raise

    except CosNaming.NamingContext.CannotProceed, err:
      if force:
        self.rebindRecursive(err.cxt, err,rest_of_name, obj)
      else:
        self.__print_exception()
        raise
      
    return


  ##
  # @if jp
  #
  # @brief Object �� rebind ����
  #
  # Object �� rebind ����ݤ�Ϳ����̾����ʸ����ɽ���Ǥ��뤳�Ȱʳ��� rebind()
  # ��Ʊ���Ǥ��롣rebind(toName(string_name), obj) ��������
  #
  # @param self
  # @param string_name ���֥������Ȥ��դ���̾����ʸ����ɽ��
  # @param obj ��Ϣ�դ����륪�֥�������
  # @param force true�ξ�硢����Υ���ƥ����Ȥ���Ū�˥Х���ɤ���
  #              (�ǥե������:true)
  #
  # @exception NotFound ����� <c_1, c_2, ..., c_(n-1)> ��¸�ߤ��ʤ���
  # @exception CannotProceed ���餫����ͳ�ǽ������³�Ǥ��ʤ���
  # @exception InvalidName ���� string_name ��̾����������
  #
  # @else
  #
  # @brief
  #
  # @endif
  def rebindByString(self, string_name, obj, force=True):
    self.rebind(self.toName(string_name), obj, force)

    return


  ##
  # @if jp
  #
  # @brief ����Υ���ƥ����Ȥ� bind ���ʤ��� Object �� rebind ����
  #
  # name_list <c_n> �ǻ��ꤵ�줿 NamingContext �⤷���� Object �����Ǥ�¸�ߤ���
  # ��������� bindRecursive() ��Ʊ���Ǥ��롣
  #
  # name_list <c_n> �ǻ��ꤵ�줿�Х���ǥ��󥰤����Ǥ�¸�ߤ�����ˤϡ�
  # �������Х���ǥ��󥰤��֤��������롣
  #
  # @param self
  # @param context bind �򳫻Ϥ��롡NamingContext
  # @param name_list ���֥������Ȥ��դ���̾���� NameComponent
  # @param obj ��Ϣ�դ����륪�֥�������
  #
  # @exception CannotProceed ����Υ���ƥ����Ȥ����Ǥ��ʤ���
  # @exception InvalidName Ϳ����줿 name_list ��������
  #
  # @else
  #
  # @brief
  #
  # @endif
  def rebindRecursive(self, context, name_list, obj):
    length = len(name_list)
    for i in range(length):
      if i == length - 1:
        context.rebind(self.subName(name_list, i, i), obj)
        return
      else:
        if self.objIsNamingContext(context):
          try:
            context = context.bind_new_context(self.subName(name_list, i, i))
          except CosNaming.NamingContext.AlreadyBound:
            obj_ = context.resolve(self.subName(name_list, i, i))
            context = obj_._narrow(CosNaming.NamingContext)
        else:
          raise CosNaming.NamingContext.CannotProceed(context, self.subName(name_list, i))
    return


  ##
  # @if jp
  #
  # @brief NamingContext �� bind ����
  #
  # bind �оݤȤ��ƻ��ꤵ�줿���� name ��ʸ����ξ��� bindByString() �ȡ�
  # ����ʳ��ξ��� bind() ��Ʊ���Ǥ��롣
  #
  # @param self
  # @param name ���֥������Ȥ��դ���̾��
  # @param name_cxt ��Ϣ�դ����� NamingContext
  # @param force true�ξ�硢����Υ���ƥ����Ȥ���Ū�˥Х���ɤ���
  #              (�ǥե������:True)
  #
  # @exception NotFound ����� <c_1, c_2, ..., c_(n-1)> ��¸�ߤ��ʤ���
  # @exception CannotProceed ���餫����ͳ�ǽ������³�Ǥ��ʤ���
  # @exception InvalidName ���� name ��̾����������
  # @exception AlreadyBound name <c_n> �� Object �����Ǥ˥Х���ɤ���Ƥ��롣
  #
  # @else
  #
  # @brief
  #
  # @endif
  def bindContext(self, name, name_cxt, force=True):
    if isinstance(name, basestring):
      self.bind(self.toName(name), name_cxt, force)
    else:
      self.bind(name, name_cxt, force)
    return


  ##
  # @if jp
  #
  # @brief NamingContext �� bind ����
  #
  # bind ����륪�֥������Ȥ� NamingContext �Ǥ��뤳�Ȥ������
  # bindRecursive() ��Ʊ���Ǥ��롣
  #
  # @param self
  # @param context bind �򳫻Ϥ��롡NamingContext
  # @param name_list ���֥������Ȥ��դ���̾���Υ͡��ॳ��ݡ��ͥ��
  # @param name_cxt ��Ϣ�դ����� NamingContext
  #
  # @else
  #
  # @brief
  #
  # @endif
  def bindContextRecursive(self, context, name_list, name_cxt):
    self.bindRecursive(context, name_list, name_cxt)
    return


  ##
  # @if jp
  #
  # @brief NamingContext �� rebind ����
  #
  # bind �оݤȤ��ƻ��ꤵ�줿���� name ��ʸ����ξ��� rebindByString() �ȡ�
  # ����ʳ��ξ��� rebind() ��Ʊ���Ǥ��롣
  # �ɤ���ξ���Х���ǥ��󥰤����Ǥ�¸�ߤ�����ˤϡ�
  # �������Х���ǥ��󥰤��֤��������롣
  #
  # @param self
  # @param name ���֥������Ȥ��դ���̾���Υ͡��ॳ��ݡ��ͥ��
  # @param name_cxt ��Ϣ�դ����� NamingContext
  # @param force true�ξ�硢����Υ���ƥ����Ȥ���Ū�˥Х���ɤ���
  #              (�ǥե������:true)
  #
  # @exception NotFound ����� <c_1, c_2, ..., c_(n-1)> ��¸�ߤ��ʤ���
  # @exception CannotProceed ���餫����ͳ�ǽ������³�Ǥ��ʤ���
  # @exception InvalidName ���� name ��̾����������
  #
  # @else
  #
  # @endif
  def rebindContext(self, name, name_cxt, force=True):
    if isinstance(name, basestring):
      self.rebind(self.toName(name), name_cxt, force)
    else:
      self.rebind(name, name_cxt, force)
    return


  ##
  # @if jp
  #
  # @brief ����Υ���ƥ����Ȥ�Ƶ�Ū�� rebind �� NamingContext �� rebind ����    #
  # bind ����륪�֥������Ȥ� NamingContext �Ǥ��뤳�Ȥ������
  # rebindRecursive() ��Ʊ���Ǥ��롣
  #
  # @param self
  # @param context bind �򳫻Ϥ��롡NamingContext
  # @param name_list ���֥������Ȥ��դ���̾���� NameComponent
  # @param name_cxt ��Ϣ�դ����� NamingContext
  #
  # @else
  #
  # @brief
  #
  # @endif
  def rebindContextRecursive(self, context, name_list, name_cxt):
    self.rebindRecursive(context, name_list, name_cxt)
    return


  ##
  # @if jp
  #
  # @brief Object �� name �����褹��
  #
  # name �� bind ����Ƥ��륪�֥������Ȼ��Ȥ��֤���
  # �͡��ॳ��ݡ��ͥ�� <c_1, c_2, ... c_n> �ϺƵ�Ū�˲�褵��롣
  # 
  # ���� name ��Ϳ����줿�ͤ�ʸ����ξ��ˤϤޤ��ǽ�� toName() �ˤ�ä�
  # NameComponent ���Ѵ�����롣
  # 
  # CosNaming::resolve() �Ȥۤ�Ʊ����Ư���򤹤뤬�����Ϳ����줿
  # �͡��ॵ���ФΥ롼�ȥ���ƥ����Ȥ��Ф��� resolve() ���ƤӽФ��������
  # �ۤʤ롣
  #
  # @param self
  # @param name ��褹�٤����֥������Ȥ�̾���Υ͡��ॳ��ݡ��ͥ��
  #
  # @return ��褵�줿���֥������Ȼ���
  #
  # @exception NotFound ����� <c_1, c_2, ..., c_(n-1)> ��¸�ߤ��ʤ���
  # @exception CannotProceed ���餫����ͳ�ǽ������³�Ǥ��ʤ���
  # @exception InvalidName ���� name ��̾����������
  #
  # @else
  #
  # @endif
  def resolve(self, name):
    if isinstance(name, basestring):
      name_ = self.toName(name)
    else:
      name_ = name
      
    try:
      obj = self._rootContext.resolve(name_)
      return obj
    except CosNaming.NamingContext.NotFound, ex:
      self.__print_exception()
      return None


  ##
  # @if jp
  #
  # @brief ���ꤵ�줿̾���Υ��֥������Ȥ� bind ��������
  #
  # name �� bind ����Ƥ��륪�֥������Ȼ��Ȥ������롣
  # �͡��ॳ��ݡ��ͥ�� <c_1, c_2, ... c_n> �ϺƵ�Ū�˲�褵��롣
  # 
  # ���� name ��Ϳ����줿�ͤ�ʸ����ξ��ˤϤޤ��ǽ�� toName() �ˤ�ä�
  # NameComponent ���Ѵ�����롣
  # 
  # CosNaming::unbind() �Ȥۤ�Ʊ����Ư���򤹤뤬�����Ϳ����줿
  # �͡��ॵ���ФΥ롼�ȥ���ƥ����Ȥ��Ф��� unbind() ���ƤӽФ��������
  # �ۤʤ롣
  #
  # @param self
  # @param name ������륪�֥������ȤΥ͡��ॳ��ݡ��ͥ��
  #
  # @exception NotFound ����� <c_1, c_2, ..., c_(n-1)> ��¸�ߤ��ʤ���
  # @exception CannotProceed ���餫����ͳ�ǽ������³�Ǥ��ʤ���
  # @exception InvalidName ���� name ��̾����������
  #
  # @else
  #
  # @endif
  # void unbind(const CosNaming::Name& name)
  #   throw(NotFound, CannotProceed, InvalidName);
  def unbind(self, name):
    if isinstance(name, basestring):
      name_ = self.toName(name)
    else:
      name_ = name

    try:
      self._rootContext.unbind(name_)
    except:
      self.__print_exception()

    return


  ##
  # @if jp
  #
  # @brief ����������ƥ����Ȥ���������
  #
  # Ϳ����줿�͡��ॵ���о���������줿 NamingContext ���֤���
  # �֤��줿 NamingContext �� bind ����Ƥ��ʤ���
  # 
  # @param self
  # 
  # @return �������줿������ NamingContext
  #
  # @else
  #
  # @endif
  def newContext(self):
    return self._rootContext.new_context()


  ##
  # @if jp
  #
  # @brief ����������ƥ����Ȥ� bind ����
  #
  # Ϳ����줿 name ���Ф��ƿ���������ƥ����Ȥ�Х���ɤ��롣
  # �������줿��NamingContext �ϥ͡��ॵ���о���������줿��ΤǤ��롣
  # 
  # ���� name ��Ϳ����줿�ͤ�ʸ����ξ��ˤϤޤ��ǽ�� toName() �ˤ�ä�
  # NameComponent ���Ѵ�����롣
  # 
  # @param self
  # @param name NamingContext���դ���̾���Υ͡��ॳ��ݡ��ͥ��
  # @param force true�ξ�硢����Υ���ƥ����Ȥ���Ū�˥Х���ɤ���
  #              (�ǥե������:true)
  #
  # @return �������줿������ NamingContext
  #
  # @exception NotFound ����� <c_1, c_2, ..., c_(n-1)> ��¸�ߤ��ʤ���
  # @exception CannotProceed ���餫����ͳ�ǽ������³�Ǥ��ʤ���
  # @exception InvalidName ���� name ��̾����������
  # @exception AlreadyBound name <n> �� Object �����Ǥ˥Х���ɤ���Ƥ��롣
  #
  # @else
  #
  # @endif
  def bindNewContext(self, name, force=True):
    if force is None:
      force = True
      
    if isinstance(name, basestring):
      name_ = self.toName(name)
    else:
      name_ = name

    try:
      return self._rootContext.bind_new_context(name_)
    except CosNaming.NamingContext.NotFound:
      if force:
        self.bindRecursive(self._rootContext, name_, self.newContext())
      else:
        self.__print_exception()
        raise
    except CosNaming.NamingContext.CannotProceed, err:
      if force:
        self.bindRecursive(err.cxt, err.rest_of_name, self.newContext())
      else:
        self.__print_exception()
        raise
    return None


  ##
  # @if jp
  #
  # @brief NamingContext ���󥢥��ƥ��ֲ�����
  #
  # context �ǻ��ꤵ�줿 NamingContext ���󥢥��ƥ��ֲ����롣
  # context ��¾�Υ���ƥ����Ȥ��Х���ɤ���Ƥ������ NotEmpty �㳰��
  # ȯ�����롣
  # 
  # @param self
  # @param context �󥢥��ƥ��ֲ����� NamingContext
  #
  # @exception NotEmpty �о�context ��¾�Υ���ƥ����Ȥ��Х���ɤ���Ƥ��롣
  #
  # @else
  #
  # @else
  #
  # @brief Destroy the naming context
  #
  # Delete the specified naming context.
  # any bindings should be <unbind> in which the given context is bound to
  # some names before invoking <destroy> operation on it. 
  #
  # @param context NamingContext which is destroied.
  #     
  # @exception NotEmpty 
  #
  # @else
  #
  # @endif
  def destroy(self, context):
    context.destroy()


  ##
  # @if jp
  # @brief NamingContext ��Ƶ�Ū�˲��ä��󥢥��ƥ��ֲ�����
  #
  # context ��Ϳ����줿 NamingContext ���Ф��ơ�name �ǻ��ꤵ�줿
  # �͡��ॳ��ݡ��ͥ�� <c_1, ... c_(n-1)> �� NamingContext �Ȥ���
  # ��褷�ʤ��顢̾�� <c_n> ���Ф��� �󥢥��ƥ��ֲ���Ԥ���
  #
  # @param self
  # @param context �󥢥��ƥ��ֲ����� NamingContext
  #
  # @exception NotEmpty �о�context ��¾�Υ���ƥ����Ȥ��Х���ɤ���Ƥ��롣
  # @exception NotFound ����� <c_1, c_2, ..., c_(n-1)> ��¸�ߤ��ʤ���
  # @exception CannotProceed ���餫����ͳ�ǽ������³�Ǥ��ʤ���
  # @exception InvalidName ���� name ��̾����������
  #
  # @else
  # @brief Destroy the naming context recursively
  # @endif
  def destroyRecursive(self, context):
    cont = True
    bl = []
    bi = 0
    bl, bi = context.list(self._blLength)
    while cont:
      for i in range(len(bl)):
        if bl[i].binding_type == CosNaming.ncontext:
          obj = context.resolve(bl[i].binding_name)
          next_context = obj._narrow(CosNaming.NamingContext)

          self.destroyRecursive(next_context)
          context.unbind(bl[i].binding_name)
          next_context.destroy()
        elif bl[i].binding_type == CosNaming.nobject:
          context.unbind(bl[i].binding_name)
        else:
          assert(0)
      if CORBA.is_nil(bi):
        cont = False
      else:
        bi.next_n(self._blLength, bl)

    if not (CORBA.is_nil(bi)):
      bi.destroy()
    return


  ##
  # @if jp
  # @brief ���٤Ƥ� Binding ��������
  #
  # ��Ͽ����Ƥ������Ƥ�Binding �������롣
  #
  # @param self
  #
  # @else
  # @brief Destroy all binding
  # @endif
  def clearAll(self):
    self.destroyRecursive(self._rootContext)
    return


  ##
  # @if jp
  # @brief Ϳ����줿 NamingContext �� Binding ���������
  #
  # ���ꤵ�줿 NamingContext �� Binding ��������롣
  #
  # @param self
  # @param name_cxt Binding �����о� NamingContext
  # @param how_many Binding ��������볬�ؤο���
  # @param rbl �������� Binding ���ݻ�����ۥ��
  # @param rbi �������� Binding �򤿤ɤ뤿��Υ��ƥ졼��
  #
  # @else
  # @endif
  def list(self, name_cxt, how_many, rbl, rbi):
    bl, bi = name_cxt.list(how_many)

    for i in bl:
      rbl.append(bl)

    rbi.append(bi)
  

  #============================================================
  # interface of NamingContext
  #============================================================

  ##
  # @if jp
  # @brief Ϳ����줿 NameComponent ��ʸ����ɽ�����֤�
  #
  # ���ꤵ�줿 NameComponent ��ʸ�����Ѵ����롣
  #
  # @param self
  # @param name_list �Ѵ��о� NameComponent
  #
  # @return ʸ�����Ѵ����
  #
  # @exception InvalidName ���� name_list ��̾����������
  #
  # @else
  # @brief Get string representation of given NameComponent
  # @endif
  def toString(self, name_list):
    if len(name_list) == 0:
      raise CosNaming.NamingContext.InvalidName

    slen = self.getNameLength(name_list)
    string_name = [""]
    self.nameToString(name_list, string_name, slen)

    return string_name[0]


  ##
  # @if jp
  # @brief Ϳ����줿ʸ����ɽ���� NameComponent ��ʬ�򤹤�
  #
  # ���ꤵ�줿ʸ����� NameComponent ���Ѵ����롣
  #
  # @param self
  # @param sname �Ѵ��о�ʸ����
  #
  # @return NameComponent �Ѵ����
  #
  # @exception InvalidName ���� sname ��������
  #
  # @else
  # @brief Get NameComponent from gien string name representation
  # @endif
  def toName(self, sname):
    if not sname:
      raise CosNaming.NamingContext.InvalidName

    string_name = sname
    name_comps = []

    nc_length = 0
    nc_length = self.split(string_name, "/", name_comps)

    if not (nc_length > 0):
      raise CosNaming.NamingContext.InvalidName

    name_list = [CosNaming.NameComponent("","") for i in range(nc_length)]

    for i in range(nc_length):
      pos = string.rfind(name_comps[i][0:],".")
      if pos == -1:
        name_list[i].id   = name_comps[i]
        name_list[i].kind = ""
      else:
        name_list[i].id   = name_comps[i][0:pos]
        name_list[i].kind = name_comps[i][(pos+1):]

    return name_list


  ##
  # @if jp
  # @brief Ϳ����줿 addr �� string_name ���� URLɽ�����������
  #
  # ���ꤵ�줿���ɥ쥹��̾�Τ�URL���Ѵ����롣
  #
  # @param self
  # @param addr �Ѵ��оݥ��ɥ쥹
  # @param string_name �Ѵ��о�̾��
  #
  # @return URL �Ѵ����
  #
  # @exception InvalidAddress ���� addr ��������
  # @exception InvalidName ���� string_name ��������
  #
  # @else
  # @brief Get URL representation from given addr and string_name
  # @endif
  def toUrl(self, addr, string_name):
    return self._rootContext.to_url(addr, string_name)


  ##
  # @if jp
  # @brief Ϳ����줿ʸ����ɽ���� resolve �����֥������Ȥ��֤�
  #
  # ���ꤵ�줿ʸ����ɽ����resolve�������֥������Ȥ�������롣
  #
  # @param self
  # @param string_name �����оݥ��֥�������ʸ����ɽ��
  #
  # @return ��褵�줿���֥�������
  #
  # @exception NotFound ����� <c_1, c_2, ..., c_(n-1)> ��¸�ߤ��ʤ���
  # @exception CannotProceed ���餫����ͳ�ǽ������³�Ǥ��ʤ���
  # @exception InvalidName ���� name ��̾����������
  # @exception AlreadyBound name <n> �� Object �����Ǥ˥Х���ɤ���Ƥ��롣
  #
  # @else
  # @brief Resolve from name of string representation and get object 
  # @endif
  def resolveStr(self, string_name):
    return self.resolve(self.toName(string_name))


  #============================================================
  # Find functions
  #============================================================

  ##
  # @if jp
  #
  # @brief ���֥������Ȥ�̾����Х���ɤޤ��ϲ�褹��
  #
  # ���ꤵ�줿����ƥ����Ȥ��Ф��ƥ��֥������Ȥ� NameComponent �ǻ��ꤵ�줿
  # ���֤˥Х���ɤ��롣
  # Ʊ��ս�˴���¾�����Ǥ��Х���ɺѤߤξ��ϡ���¸�ΥХ���ɺѤ����Ǥ�
  # �������롣
  #
  # @param self
  # @param context bind �⤷���� resole �оݥ���ƥ�����
  # @param name_list ���֥������Ȥ��դ���̾���� NameComponent
  # @param obj ��Ϣ�դ����� Object
  #
  # @return NameComponent �ǻ��ꤵ�줿���֤˥Х���ɤ���Ƥ��륪�֥�������
  #
  # @else
  # @brief Bind of resolve the given name component
  # @endif
  def bindOrResolve(self, context, name_list, obj):
    try:
      context.bind_context(name_list, obj)
      return obj
    except CosNaming.NamingContext.AlreadyBound:
      obj = context.resolve(name_list)
      return obj
    return CORBA.Object._nil


  ##
  # @if jp
  #
  # @brief ����ƥ����Ȥ�̾����Х���ɤޤ��ϲ�褹��
  #
  # ���ꤵ�줿����ƥ����Ȥ��Ф��� Context�� NameComponent �ǻ��ꤵ�줿���֤�
  # �Х���ɤ��롣
  # Context �����ξ��Ͽ�������ƥ����Ȥ��������ƥХ���ɤ��롣
  # Ʊ��ս�˴���¾�����Ǥ��Х���ɺѤߤξ��ϡ���¸�ΥХ���ɺѤ����Ǥ�
  # �������롣
  #
  # @param self
  # @param context bind �⤷���� resole �оݥ���ƥ�����
  # @param name_list ����ƥ����Ȥ��դ���̾���� NameComponent
  # @param new_context ��Ϣ�դ����� Context(�ǥե������:None)
  #
  # @return NameComponent �ǻ��ꤵ�줿���֤˥Х���ɤ���Ƥ���Context
  #
  # @else
  # @brief Bind of resolve the given name component
  # @endif
  def bindOrResolveContext(self, context, name_list, new_context=None):
    if new_context is None:
      new_cxt = self.newContext()
    else:
      new_cxt = new_context

    obj = self.bindOrResolve(context, name_list, new_cxt)
    return obj._narrow(CosNaming.NamingContext)


  ##
  # @if jp
  # @brief �͡��ॵ���Ф�̾�����������
  #
  # ���ꤷ���͡��ॵ���Ф�̾����������롣
  #
  # @param self
  #
  # @return �͡��ॵ���Ф�̾��
  #
  # @else
  # @brief Get the name of naming server
  # @endif
  def getNameServer(self):
    return self._nameServer


  ##
  # @if jp
  # @brief �롼�ȥ���ƥ����Ȥ��������
  #
  # ���ꤷ���͡��ॵ���ФΥ롼�ȥ���ƥ����Ȥ�������롣
  #
  # @param self
  #
  # @return �͡��ॵ���ФΥ롼�ȥ���ƥ�����
  #
  # @else
  # @brief Get the root context
  # @endif
  def getRootContext(self):
    return self._rootContext


  ##
  # @if jp
  # @brief ���֥������Ȥ��͡��ߥ󥰥���ƥ����Ȥ�Ƚ�̤���
  #
  # ���ꤷ�����Ǥ��͡��ߥ󥰥���ƥ����Ȥ�Ƚ�̤���
  #
  # @param self
  # @param obj Ƚ���о�����
  #
  # @return Ƚ�̷��(�͡��ߥ󥰥���ƥ�����:true������ʳ�:false)
  #
  # @else
  # @brief Whether the object is NamingContext
  # @endif
  def objIsNamingContext(self, obj):
    nc = obj._narrow(CosNaming.NamingContext)
    if CORBA.is_nil(nc):
      return False
    else:
      return True


  ##
  # @if jp
  # @brief Ϳ����줿̾�����͡��ߥ󥰥���ƥ����Ȥ��ɤ���Ƚ�̤���
  #
  # NameComponent �⤷����ʸ����ǻ��ꤷ�����Ǥ��͡��ߥ󥰥���ƥ����Ȥ�
  # Ƚ�̤���
  #
  # @param self
  # @param name_list Ƚ���о�
  #
  # @return Ƚ�̷��(�͡��ߥ󥰥���ƥ�����:true������ʳ�:false)
  #
  # @else
  # @brief Whether the given name component is NamingContext
  # @endif
  def nameIsNamingContext(self, name_list):
    return self.objIsNamingContext(self.resolve(name_list))


  ##
  # @if jp
  # @brief �͡��ॳ��ݡ��ͥ�Ȥ���ʬ���֤�
  #
  # ���ꤵ�줿�ϰϤΥ͡��ॳ��ݡ��ͥ�Ȥ�������롣
  # ��λ���֤����ꤵ��Ƥ��ʤ����ϡ��Ǹ�����Ǥ�������͡��ॳ��ݡ��ͥ��
  # ���֤���
  #
  # @param self
  # @param name_list �����о�NameComponent
  # @param begin �����ϰϳ��ϰ���
  # @param end �����ϰϽ�λ����(�ǥե������:None)
  #
  # @return NameComponent �������
  #
  # @else
  # @brief Get subset of given name component
  # @endif
  def subName(self, name_list, begin, end = None):
    if end is None or end < 0:
      end = len(name_list) - 1

    sub_len = end - (begin -1)
    objId = ""
    kind  = ""
    
    sub_name = []
    for i in range(sub_len):
      sub_name.append(name_list[begin + i])

    return sub_name


  ##
  # @if jp
  # @brief �͡��ॳ��ݡ��ͥ�Ȥ�ʸ����ɽ�����������
  #
  # ���ꤷ���ϰϤΥ͡��ॳ��ݡ��ͥ�Ȥ�ʸ����ɽ����������롣
  # ʸ����ɽ���ϡ�NameComponent�ι�����{Nc[0],Nc[1],Nc[2]������}�ξ�硢
  #   Nc[0]id.Nc[0].kind/Nc[1]id.Nc[1].kind/Nc[2].id/Nc[2].kind������
  # �Ȥ��������Ǽ����Ǥ��롣
  # ��������ʸ�����Ĺ�������ꤷ��Ĺ���ʾ�ξ��ϡ�
  # ���ꤷ��Ĺ�����ڤ�ΤƤ��롣
  #
  # @param self
  # @param name_list �����о�NameComponent
  # @param string_name �������ʸ����
  # @param slen �����о�ʸ���������
  #
  # @else
  # @brief Get string representation of name component
  # @endif
  def nameToString(self, name_list, string_name, slen):
    for i in range(len(name_list)):
      for id_ in name_list[i].id:
        if id_ == "/" or id_ == "." or id_ == "\\":
          string_name[0] += "\\"
        string_name[0] += id_

      if name_list[i].id == "" or name_list[i].kind != "":
        string_name[0] += "."

      for kind_ in name_list[i].kind:
        if kind_ == "/" or kind_ == "." or kind_ == "\\":
          string_name[0] += "\\"
        string_name[0] += kind_

      string_name[0] += "/"


  ##
  # @if jp
  # @brief �͡��ॳ��ݡ��ͥ�Ȥ�ʸ����ɽ������ʸ��Ĺ���������
  #
  # ���ꤷ���͡��ॳ��ݡ��ͥ�Ȥ�ʸ�����ɽ����������Ĺ����������롣
  # ʸ����ɽ���ϡ�NameComponent�ι�����{Nc[0],Nc[1],Nc[2]������}�ξ�硢
  #   Nc[0]id.Nc[0].kind/Nc[1]id.Nc[1].kind/Nc[2].id/Nc[2].kind������
  # �Ȥ��������Ǽ����Ǥ��롣
  #
  # @param self
  # @param name_list �����о�NameComponent
  #
  # @return ���ꤷ���͡��ॳ��ݡ��ͥ�Ȥ�ʸ����Ĺ��
  #
  # @else
  # @brief Get string length of the name component's string representation
  # @endif
  def getNameLength(self, name_list):
    slen = 0

    for i in range(len(name_list)):
      for id_ in name_list[i].id:
        if id_ == "/" or id_ == "." or id_ == "\\":
          slen += 1
        slen += 1
      if name_list[i].id == "" or name_list[i].kind == "":
        slen += 1

      for kind_ in name_list[i].kind:
        if kind_ == "/" or kind_ == "." or kind_ == "\\":
          slen += 1
        slen += 1

      slen += 1

    return slen


  ##
  # @if jp
  # @brief ʸ�����ʬ��
  #
  # ʸ�������ꤷ���ǥ�ߥ���ʬ�䤹�롣
  #
  # @param self
  # @param input ʬ���о�ʸ����
  # @param delimiter ʬ���ѥǥ�ߥ�
  # @param results ʬ����
  #
  # @return ʬ�䤷��ʸ��������ǿ�
  #
  # @else
  # @brief Split of string
  # @endif
  def split(self, input, delimiter, results):
    delim_size = len(delimiter)
    found_pos = 0
    begin_pos = 0
    pre_pos = 0
    substr_size = 0

    if input[0:delim_size] == delimiter:
      begin_pos = delim_size
      pre_pos = delim_size

    while 1:
      found_pos = string.find(input[begin_pos:],delimiter)
      if found_pos == -1:
        results.append(input[pre_pos:])
        break

      if found_pos > 0 and input[found_pos + begin_pos - 1] == "\\":
        begin_pos += found_pos + delim_size
      else:
        substr_size = found_pos + (begin_pos - pre_pos)
        if substr_size > 0:
          results.append(input[pre_pos:(pre_pos+substr_size)])
        begin_pos += found_pos + delim_size
        pre_pos   = begin_pos

    return len(results)


  ##
  # @if jp
  #
  # @brief �㳰�������
  #  �㳰�������Ϥ��롣
  #
  # @else
  #
  # @brief Print exception information 
  #  Print exception information 
  # @endif
  def __print_exception(self):
    if sys.version_info[0:3] >= (2, 4, 0):
      print traceback.format_exc()
    else:
      _exc_list = traceback.format_exception(*sys.exc_info())
      _exc_str = "".join(_exc_list)
      print _exc_str

    return
