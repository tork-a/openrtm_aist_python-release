#!/usr/bin/env python
# -*- coding: euc-jp -*- 

##
# @file ConfigAdmin.py
# @brief Configuration Administration classes
# @date $Date: 2007/09/04$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
# Copyright (C) 2007-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.



import copy
import OpenRTM_aist


class OnUpdateCallback:
  def __init__(self):
    pass


  def __call__(self, config_set):
    pass



class OnUpdateParamCallback:
  def __init__(self):
    pass


  def __call__(self, config_set, config_param):
    pass



class OnSetConfigurationSetCallback:
  def __init__(self):
    pass


  def __call__(self, config_set):
    pass



class OnAddConfigurationAddCallback:
  def __init__(self):
    pass


  def __call__(self, config_set):
    pass



class OnRemoveConfigurationSetCallback:
  def __init__(self):
    pass


  def __call__(self, config_set):
    pass



class OnActivateSetCallback:
  def __init__(self):
    pass


  def __call__(self, config_id):
    pass



##
# @if jp
# @class Config
# @brief Config ���饹
# 
# ����ե�����졼�����ѥ�᡼���ξ�����ݻ����륯�饹��
#
# @since 0.4.0
#
# @else
# @class Config
# @brief Config class
# 
# Class to hold the configuration parameter information.
#
# @since 0.4.0
#
# @endif
class Config:
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
  # @param name ����ե�����졼�����ѥ�᡼��̾
  # @param var ����ե�����졼�����ѥ�᡼����Ǽ���ѿ�
  # @param def_val ʸ��������Υǥե������
  # @param trans ʸ��������Ѵ��ؿ�(�ǥե������:None)
  # 
  # @else
  #
  # @brief Constructor
  # 
  # Constructor
  #
  # @param self 
  # @param name Configuration parameter name
  # @param var Configuration parameter variable
  # @param def_val Default value in string format
  # @param trans Function to transform into string format
  #
  # @endif
  def __init__(self, name, var, def_val, trans=None):
    self.name = name
    self.default_value = def_val
    self._var = var
    if trans:
      self._trans = trans
    else:
      self._trans = OpenRTM_aist.stringTo


  ##
  # @if jp
  # 
  # @brief �Х���ɥѥ�᡼���ͤ򹹿�
  # 
  # ����ե�����졼����������ͤǥ���ե�����졼�����ѥ�᡼���򹹿�����
  # 
  # @param self 
  # @param val �ѥ�᡼���ͤ�ʸ����ɽ��
  # 
  # @return �����������(��������:true����������:false)
  # 
  # @else
  # 
  # @brief Update a bind parameter value
  # 
  # Update configuration paramater by the configuration value.
  #
  # @param self 
  # @param val The parameter values converted into character string format
  #
  # @return Update result (Successful:true, Failed:false)
  # 
  # @endif
  # virtual bool update(const char* val)
  def update(self, val):
    if self._trans(self._var, val):
      return True
    self._trans(self._var, self._default_value)
    return False



##
# @if jp
# @class ConfigAdmin
# @brief ConfigAdmin ���饹
# 
# �Ƽ拾��ե�����졼���������������륯�饹��
# �Ѹ��ʲ��Τ褦��������롣
#
# - ����ե�����졼�����: ����ݡ��ͥ�Ȥ��������
#
# - (����ե�����졼�����)�ѥ�᡼���� key-value ����ʤ��������
#   coil::Properties �ѿ��Ȥ��ư���졢key��value ����ʸ����Ȥ�����
#   ������롣key �򥳥�ե�����졼�����ѥ�᡼��̾��value �򥳥�
#   �ե�����졼�����ѥ�᡼���ͤȸƤ֡�
#
# - ����ե�����졼����󥻥åȡ� ����ե�����졼�����ѥ�᡼��
#   �Υꥹ�Ȥǡ�̾�� (ID) �ˤ�äƶ��̤���롣ID�򥳥�ե�����졼����
#   �󥻥å�ID�ȸƤ֡�
#
# - (����ե�����졼�����)�ѥ�᡼���ѿ�������ե�����졼������
#   ��᡼����RTC�Υ����ƥ��ӥƥ���Ǽºݤ����Ѥ���ݤ˻��Ȥ������
#   �����ѥ�᡼�����Ȥ˸�ͭ�η�����ġ�
#
# - �����ƥ���(����ե�����졼�����)���åȡ�����ͭ���ʥ���ե�����
#   �졼����󥻥åȤΤ��ȤǤ��ꡢͣ���¸�ߤ��롣��§�Ȥ��ơ������ƥ�
#   �֥���ե�����졼����󥻥åȤΥѥ�᡼��������ե�����졼����
#   ��ѥ�᡼���ѿ���ȿ�Ǥ���롣
#
# ���Υ��饹�Ǥϡ�����ե�����졼�����Τ���ΰʲ���2�Ĥξ������
# �����Ƥ��롣
#
# -# ����ե�����졼����󥻥åȤΥꥹ��
# -# �ѥ�᡼���ѿ��Υꥹ��
#
# ����Ū�ˤϡ�(1) �Υ���ե�����졼����󥻥åȤΥꥹ�ȤΤ�����Ĥ�
# (2) �Υѥ�᡼���ѿ���ȿ�Ǥ����롢�Τ��ܥ��饹����Ū�Ǥ��롣�̾
# �ѥ�᡼���ѿ����ѹ����ϡ�����ե�����졼����󥻥åȤ��ѹ��ȥ�
# ��᡼���ѿ��ؤ�ȿ�Ǥ�2�ʳ��ǹԤ��롣
#
# ����ե�����졼����󥻥åȤΥꥹ�Ȥ����ˤϡ��ʲ��δؿ����Ѥ��롣
#
# - getConfigurationSets()
# - getConfigurationSet()
# - setConfigurationSetValues()
# - getActiveConfigurationSet()
# - addConfigurationSet()
# - removeConfigurationSet()
# - activateConfigurationSet()
#
# �����δؿ��ˤ�ꡢ����ե�����졼����󥻥åȤ��ѹ����ɲá������
# �����������ƥ��ֲ���Ԥ������������ˤ���ѹ����줿����ե�����
# �졼����󥻥åȤ�RTC�Υ����ƥ��ӥƥ�������Ѥ���ѥ�᡼���ѿ�
# ��ȿ�Ǥ�����ˤϡ��ʲ��� update() �ؿ����Ѥ��롣
#
# - update(void)
# - update(const char* config_set)
# - update(const char* config_set, const char* config_param)
#
# ����ե�����졼���������եå����뤿��˥�����Хå��ե��󥯥�
# ��Ϳ���뤳�Ȥ��Ǥ��롣�եå��Ǥ������ϰʲ����̤ꡣ
#
# - ON_UPDATE                   : update() �������
# - ON_UPDATE_PARAM             : update(param) �������
# - ON_SET_CONFIGURATIONSET     : setConfigurationSet() �������
# - ON_ADD_CONFIGURATIONSET     : addConfigurationSet() �������
# - ON_REMOVE_CONFIGURATIONSET  : removeConfigurationSet() �������
# - ON_ACTIVATE_CONFIGURATIONSET: activateConfigurationSet() �������
#
# @since 0.4.0
#
# @else
# @class ConfigAdmin
# @brief ConfigAdmin class
# 
# Class to manage various configuration information.
# Now terms for this class are defined as follows.
#
# - Configurations: The configuration information for the RTCs.
#
# - (Configuration) parameters: Configuration information that
#   consists of a key-value pair. The "key" and the "value" are
#   both stored as character string values in a coil::Properties
#   variable in this class. The "key" is called the "configuration
#   parameter name", and the "value" is called the "configuration
#   parameter value".
#
# - Configuration-sets: This is a list of configuration parameters,
#   and it is distinguished by name (ID). The ID is called
#   configuration-set ID.
#
# - (Configuration) parameter variables: The variables to be
#   referred when configuration parameters are actually used within
#   the activity of an RTC. Each variable has each type.
#
# - Active (configuration) set: This is the only configuration-set
#   that is currently active. The parameter values of the active
#    configuration-set are substituted into configuration variables
#   in principle.
#
# The following two configuration informations are stored in this class.
#
# -# A list of configuration-set
# -# A list of configuration parameter variables
#
# Basically, the purpose of this class is to set one of the
# configuration-set in the list of (1) into parameter variables of
# (2). Usually, configuration parameter variables manipulation is
# performed with two-phases of configuration-set setting and
# parameter variables setting.
#
# The configuration-set manipulations are performed by the
# following functions.
#
# - getConfigurationSets()
# - getConfigurationSet()
# - setConfigurationSetValues()
# - getActiveConfigurationSet()
# - addConfigurationSet()
# - removeConfigurationSet()
# - activateConfigurationSet()
#
# Modification, addition, deletion, acquisition and activation of
# configuration-set are performed by these functions. In order to
# reflect configuration-set, which is manipulated by these
# functions, on parameter variables that are used from RTC
# activities, the following update() functions are used .
#
# - update(void)
# - update(const char* config_set)
# - update(const char* config_set, const char* config_param)
#
# Callback functors can be given to hook configuration
# operation. Operations to be hooked are as follows.
#
# - ON_UPDATE                   : when update() is called
# - ON_UPDATE_PARAM             : when update(param) is called
# - ON_SET_CONFIGURATIONSET     : when setConfigurationSet() is called
# - ON_ADD_CONFIGURATIONSET     : when addConfigurationSet() is called
# - ON_REMOVE_CONFIGURATIONSET  : when removeConfigurationSet() is called
# - ON_ACTIVATE_CONFIGURATIONSET: when activateConfigurationSet() is called
#
# @since 0.4.0
#
# @endif
class ConfigAdmin:
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
  # @param configsets �����оݥץ�ѥƥ�̾
  # 
  # @else
  # 
  # Constructor
  #
  # @param self 
  # @param prop The target property name for setup
  # 
  # @endif
  # ConfigAdmin(coil::Properties& prop);
  def __init__(self, configsets):
    self._configsets = configsets
    self._activeId   = "default"
    self._active     = True
    self._changed    = False
    self._params     = []
    self._emptyconf  = OpenRTM_aist.Properties()
    self._newConfig  = []
    self._listeners  = OpenRTM_aist.ConfigurationListeners()

  ##
  # @if jp
  # 
  # @brief �ǥ��ȥ饯��
  # 
  # �ǥ��ȥ饯����
  # ���ꤵ��Ƥ���ѥ�᡼���������롣
  # 
  # @param self 
  # 
  # @else
  # 
  # @brief Destructor
  # 
  # @param self 
  # 
  # @endif
  def __del__(self):
    del self._params


  ##
  # @if jp
  # 
  # @brief ����ե�����졼�����ѥ�᡼��������
  # 
  # ����ե�����졼�����ѥ�᡼�����ѿ���Х���ɤ���
  # ���ꤷ��̾�ΤΥ���ե�����졼�����ѥ�᡼��������¸�ߤ������
  # false���֤���
  # 
  # @param self 
  # @param param_name ����ե�����졼�����ѥ�᡼��̾
  # @param var ����ե�����졼�����ѥ�᡼����Ǽ���ѿ�
  # @param def_val ����ե�����졼�����ѥ�᡼���ǥե������
  # @param trans ����ե�����졼�����ѥ�᡼��ʸ�����Ѵ��Ѵؿ�
  #             (�ǥե������:None)
  # 
  # @return ������(��������:true�����꼺��:false)
  # 
  # @else
  # 
  # @brief Setup for configuration parameters
  # 
  # Bind configuration parameter to its variable.
  # Return false, if configuration parameter of specified name has already 
  # existed.
  #
  # @param self 
  # @param param_name Configuration parameter name
  # @param var Configuration parameter variable
  # @param def_val Default value of configuration parameter
  # @param trans Function to transform configuration parameter type into 
  #        string format
  #
  # @return Setup result (Successful:true, Failed:false)
  #
  # 
  # @endif
  #template <typename VarType>
  # bool bindParameter(const char* param_name, VarType& var,
  #                    const char* def_val,
  #                    bool (*trans)(VarType&, const char*) = coil::stringTo)
  def bindParameter(self, param_name, var, def_val, trans=None):
    if trans is None:
      trans = OpenRTM_aist.stringTo
    
    if self.isExist(param_name):
      return False

    if not trans(var, def_val):
      return False
    
    self._params.append(Config(param_name, var, def_val, trans))
    return True


  ##
  # void update(void);
  #
  # @if jp
  #
  # @brief ����ե�����졼�����ѥ�᡼���ι���
  #        (�����ƥ��֥���ե�����졼����󥻥å�)
  # 
  # ����ե�����졼����󥻥åȤ���������Ƥ�����ˡ����ߥ����ƥ�
  # �֤ˤʤäƤ��륳��ե�����졼���������ꤷ���ͤǡ�����ե�����
  # �졼�����ѥ�᡼�����ͤ򹹿����롣���ν����Ǥι����ϡ������ƥ�
  # �֤ȤʤäƤ��륳��ե�����졼����󥻥åȤ�¸�ߤ��Ƥ����硢��
  # ��ι������饳��ե�����졼����󥻥åȤ����Ƥ���������Ƥ����
  # ��Τ߼¹Ԥ���롣
  #
  # @else
  #
  # @brief Update the values of configuration parameters
  #        (Active configuration set)
  # 
  # When configuration set is updated, update the configuration
  # parameter value to the value that is set to the current active
  # configuration.  This update will be executed, only when an
  # active configuration set exists and the content of the
  # configuration set has been updated from the last update.
  #
  # @endif
  #
  # void update(const char* config_set);
  #
  # @if jp
  #
  # @brief ����ե�����졼�����ѥ�᡼���ι���(ID����)
  # 
  # ����ե�����졼������ѿ����ͤ򡢻��ꤷ��ID����ĥ���ե�����졼
  # ����󥻥åȤ��ͤǹ������롣����ˤ�ꡢ�����ƥ��֤ʥ���ե�����
  # �졼����󥻥åȤ��ѹ�����ʤ����������äơ������ƥ��֥���ե�����
  # �졼����󥻥åȤȥѥ�᡼���ѿ��δ֤�̷�⤬ȯ�������ǽ��������
  # �Τ���դ�ɬ�פǤ��롣
  #
  # ���ꤷ��ID�Υ���ե�����졼����󥻥åȤ�¸�ߤ��ʤ����ϡ�����
  # �����˽�λ���롣
  #
  # @param config_set �����оݤΥ���ե�����졼����󥻥å�ID
  # 
  # @else
  #
  # @brief Update configuration parameter (By ID)
  # 
  # This operation updates configuration variables by the
  # configuration-set with specified ID. This operation does not
  # change current active configuration-set. Since this operation
  # causes inconsistency between current active configuration set
  # and actual values of configuration variables, user should
  # carefully use it.
  #
  # This operation ends without doing anything, if the
  # configuration-set does not exist.
  #
  # @param config_set The target configuration set's ID to setup
  #
  # @endif
  #
  # void update(const char* config_set, const char* config_param);
  #
  # @if jp
  #
  # @brief ����ե�����졼�����ѥ�᡼���ι���(̾�λ���)
  # 
  # ����Υ���ե�����졼������ѿ����ͤ򡢻��ꤷ��ID����ĥ���ե�
  # ����졼����󥻥åȤ��ͤǹ������롣����ˤ�ꡢ�����ƥ��֤ʥ���
  # �ե�����졼����󥻥åȤ��ѹ�����ʤ����������äơ������ƥ��֥�
  # ��ե�����졼����󥻥åȤȥѥ�᡼���ѿ��δ֤�̷�⤬ȯ�������
  # ǽ��������Τ���դ�ɬ�פǤ��롣
  #
  # ���ꤷ��ID�Υ���ե�����졼����󥻥åȤ䡢���ꤷ��̾�ΤΥѥ�᡼
  # ����¸�ߤ��ʤ����ϡ����⤻���˽�λ���롣
  #
  # @param config_set ����ե�����졼�����ID
  # @param config_param ����ե�����졼�����ѥ�᡼��̾
  # 
  # @else
  #
  # @brief Update the values of configuration parameters (By name)
  # 
  # This operation updates a configuration variable by the
  # specified configuration parameter in the
  # configuration-set. This operation does not change current
  # active configuration-set. Since this operation causes
  # inconsistency between current active configuration set and
  # actual values of configuration variables, user should carefully
  # use it.
  #
  # This operation ends without doing anything, if the
  # configuration-set or the configuration parameter do not exist.
  #
  # @param config_set configuration-set ID.
  # @param config_param configuration parameter name.
  #
  # @endif
  #
  def update(self, config_set=None, config_param=None):
    # update(const char* config_set)
    if config_set and config_param is None:
      if self._configsets.hasKey(config_set) is None:
        return
      prop = self._configsets.getNode(config_set)
      for i in range(len(self._params)):
        if prop.hasKey(self._params[i].name):
          self._params[i].update(prop.getProperty(self._params[i].name))
          self.onUpdate(config_set)

    # update(const char* config_set, const char* config_param)
    if config_set and config_param:
      key = config_set
      key = key+"."+config_param
      for conf in self._params:
        if conf.name == config_param:
          conf.update(self._configsets.getProperty(key))
          self.onUpdateParam(config_set, config_param)
          return

    # update()
    if config_set is None and config_param is None:
      if self._changed and self._active:
        self.update(self._activeId)
        self._changed = False
      return


  ##
  # @if jp
  # 
  # @brief ����ե�����졼�����ѥ�᡼����¸�߳�ǧ
  # 
  # ���ꤷ��̾�Τ���ĥ���ե�����졼�����ѥ�᡼����¸�ߤ��뤫��ǧ���롣
  # 
  # @param self 
  # @param param_name ����ե�����졼�����ѥ�᡼��̾�Ρ�
  # 
  # @return ¸�߳�ǧ���(�ѥ�᡼������:true���ѥ�᡼���ʤ�:false)
  # 
  # @else
  # 
  # @brief Check the existence of configuration parameters
  # 
  # Check the existence of configuration parameters of specified name.
  #
  # @param self 
  # @param name Configuration parameter name
  #
  # @return Result of existance confirmation 
  #         (Parameters exist:true, else:false)
  # 
  # @endif
  # bool isExist(const char* name);
  def isExist(self, param_name):
    if not self._params:
      return False
    
    for conf in self._params:
      if conf.name == param_name:
        return True

    return False


  ##
  # @if jp
  # 
  # @brief ����ե�����졼�����ѥ�᡼�����ѹ���ǧ
  # 
  # ����ե�����졼�����ѥ�᡼�����ѹ����줿����ǧ���롣
  # 
  # @param self 
  # 
  # @return �ѹ���ǧ���(�ѹ�����:true���ѹ��ʤ�:false)
  # 
  # @else
  # 
  # @brief Confirm to change configuration parameters
  # 
  # Confirm that configuration parameters have changed.
  #
  # @param self 
  #
  # @return Result of change confirmation
  #         (There is a change:true��No change:false)
  # 
  # @endif
  # bool isChanged(void) {return m_changed;}
  def isChanged(self):
    return self._changed


  ##
  # @if jp
  # 
  # @brief �����ƥ��֡�����ե�����졼����󥻥å�ID�μ���
  # 
  # ���ߥ����ƥ��֤ʥ���ե�����졼����󥻥åȤ�ID��������롣
  # 
  # @param self 
  # 
  # @return �����ƥ��֡�����ե�����졼����󥻥å�ID
  # 
  # @else
  # 
  # @brief Get ID of active configuration set
  # 
  # Get ID of the current active configuration set.
  #
  # @param self 
  #
  # @return The active configuration set ID
  # 
  # @endif
  # const char* getActiveId(void);
  def getActiveId(self):
    return self._activeId


  ##
  # @if jp
  # 
  # @brief ����ե�����졼����󥻥åȤ�¸�߳�ǧ
  # 
  # ���ꤷ������ե�����졼����󥻥åȤ�¸�ߤ��뤫��ǧ���롣
  # 
  # @param self 
  # @param config_id ��ǧ�оݥ���ե�����졼����󥻥å�ID
  # 
  # @return ¸�߳�ǧ���(���ꤷ��ConfigSet����:true���ʤ�:false)
  # 
  # @else
  # 
  # @brief Check the existence of configuration set
  # 
  # Check the existence of specified configuration set.
  #
  # @param self 
  # @param config_id ID of target configuration set for confirmation
  # @return Result of existence confirmation 
  #         (Specified ConfigSet exists:true, else:false)
  # @endif
  # bool haveConfig(const char* config_id);
  def haveConfig(self, config_id):
    if self._configsets.hasKey(config_id) is None:
      return False
    else:
      return True


  ##
  # @if jp
  # 
  # @brief ����ե�����졼����󥻥åȤΥ����ƥ��ֲ���ǧ
  # 
  # ����ե�����졼����󥻥åȤ������ƥ��ֲ�����Ƥ��뤫��ǧ���롣
  # 
  # @param self 
  # 
  # @return ���ֳ�ǧ���(�����ƥ��־���:true���󥢥��ƥ��־���:false)
  # 
  # @else
  # 
  # @brief Confirm to activate configuration set
  # 
  # Confirm that configuration set has been activated.
  #
  # @param self 
  #
  # @return Result of state confirmation
  #         (Active state:true, Inactive state:false)
  # 
  # @endif
  # bool isActive(void);
  def isActive(self):
    return self._active


  ##
  # @if jp
  # 
  # @brief ������ե�����졼����󥻥åȤμ���
  # 
  # ���ꤵ��Ƥ���������ե�����졼����󥻥åȤ�������롣
  # 
  # @param self 
  # 
  # @return ������ե�����졼����󥻥å�
  # 
  # @else
  # 
  # @brief Get all configuration sets
  # 
  # Get all specified configuration sets
  #
  # @param self 
  #
  # @return All configuration sets
  # 
  # @endif
  # const std::vector<coil::Properties*>& getConfigurationSets(void);
  def getConfigurationSets(self):
    return self._configsets.getLeaf()


  ##
  # @if jp
  # 
  # @brief ���ꤷ��ID�Υ���ե�����졼����󥻥åȤμ���
  # 
  # ID�ǻ��ꤷ������ե�����졼����󥻥åȤ�������롣
  # ���ꤷ������ե�����졼����󥻥åȤ�¸�ߤ��ʤ����ϡ�
  # ���Υ���ե�����졼����󥻥åȤ��֤���
  # 
  # @param self 
  # @param config_id �����оݥ���ե�����졼����󥻥åȤ�ID
  # 
  # @return ����ե�����졼����󥻥å�
  # 
  # @else
  # 
  # @brief Get a configuration set by specified ID
  # 
  # Get a configuration set that was specified by ID
  # Return empty configuration set, if a configuration set of
  # specified ID doesn't exist.
  #
  # @param self 
  # @param config_id ID of the target configuration set for getting
  #
  # @return The configuration set
  # 
  # @endif
  # const coil::Properties& getConfigurationSet(const char* config_id);
  def getConfigurationSet(self, config_id):
    prop = self._configsets.getNode(config_id)
    if prop is None:
      return self._emptyconf
    return prop


  ##
  # @if jp
  # 
  # @brief ���ꤷ���ץ�ѥƥ��Υ���ե�����졼����󥻥åȤؤ��ɲ�
  # 
  # ���ꤷ���ץ�ѥƥ��򥳥�ե�����졼����󥻥åȤ��ɲä��롣
  # 
  # @param self 
  # @param config_set �ɲä���ץ�ѥƥ�
  # 
  # @return �ɲý����¹Է��(�ɲ�����:true���ɲü���:false)
  # 
  # @else
  # 
  # @brief Add to configuration set from specified property
  # 
  # Add specified property to configuration set.
  #
  # @param self 
  # @param configuration_set Property to add
  #
  # @return Add result (Successful:true, Failed:false)
  # 
  # @endif
  # bool setConfigurationSetValues(const coil::Properties& config_set)
  def setConfigurationSetValues(self, config_set):
    if config_set.getName() == "" or config_set.getName() is None:
      return False

    if not self._configsets.hasKey(config_set.getName()):
      return False

    p = self._configsets.getNode(config_set.getName())
    if p is None:
      return False

    p.mergeProperties(config_set)
    self._changed = True
    self._active  = False
    self.onSetConfigurationSet(config_set)
    return True


  ##
  # @if jp
  # 
  # @brief �����ƥ��֡�����ե�����졼����󥻥åȤ����
  # 
  # ���ߥ����ƥ��֤ȤʤäƤ��륳��ե�����졼����󥻥åȤ�������롣
  # �����ƥ��֤ȤʤäƤ��륳��ե�����졼����󥻥åȤ�¸�ߤ��ʤ����ϡ�
  # ���Υ���ե�����졼����󥻥å� ���֤���
  # 
  # @param self 
  # 
  # @return �����ƥ��֡�����ե�����졼����󥻥å�
  # 
  # @else
  # 
  # @brief Get the active configuration set
  # 
  # Get the current active configuration set.
  # Return empty configuration set, if an active configuration set 
  # doesn't exist.
  #
  # @param self 
  # @return The active configuration set
  # 
  # @endif
  # const coil::Properties& getActiveConfigurationSet(void);
  def getActiveConfigurationSet(self):
    p = self._configsets.getNode(self._activeId)
    if p is None:
      return self._emptyconf

    return p


  ##
  # @if jp
  # 
  # @brief ����ե�����졼����󥻥åȤ������ͤ��ɲ�
  # 
  # ����ե�����졼����󥻥åȤ������ͤ��ɲä��롣
  # 
  # @param self 
  # @param configset �ɲä���ץ�ѥƥ�
  # 
  # @return �ɲý������(�ɲ�����:true���ɲü���:false)
  # 
  # @else
  # 
  # @brief Add the configuration value to configuration set
  # 
  # Add the configuration value to configuration set
  #
  # @param self 
  # @param configuration_set Property to add
  #
  # @return Add Result (Successful:true, Failed:false)
  # 
  # @endif
  # bool addConfigurationSet(const coil::Properties& configuration_set);
  def addConfigurationSet(self, configset):
    if self._configsets.hasKey(configset.getName()):
      return False
    node = configset.getName()

    # Create node
    self._configsets.createNode(node)

    p = self._configsets.getNode(node)
    if p is None:
      return False

    p.mergeProperties(configset)
    self._newConfig.append(node)

    self._changed = True
    self._active  = False
    self.onAddConfigurationSet(configset)
    return True


  ##
  # @if jp
  #
  # @brief ����ե�����졼����󥻥åȤκ��
  # 
  # ���ꤷ��ID�Υ���ե�����졼����󥻥åȤ������롣
  #
  # ���ꤷ��ID�Υ���ե�����졼����󥻥åȤ�¸�ߤ��ʤ����ϡ�
  # false���֤��������ǽ�ʥ���ե�����졼����󥻥åȤϡ�
  # addConfigruationSet() �ˤ�ä��ɲä�������ե�����졼����󥻥�
  # �ȤΤߤǤ��ꡢ�ǥե���ȥ���ե�����졼����󥻥åȡ�����ݡ���
  # ��ȵ�ư���˥ե����뤫���ɤ߹��ޤ�륳��ե�����졼����󥻥å�
  # �Ϻ�����뤳�Ȥ��Ǥ��ʤ���
  #
  # �ޤ������ꤷ������ե�����졼����󥻥åȤ����ߥ����ƥ��֤Ǥ���
  # ���ˤϡ������ʤ륳��ե�����졼����󥻥åȤǤ����Ǥ��ʤ���
  #
  # ���δؿ��ˤ��ºݤ˥���ե�����졼����󥻥åȤ�������줿��硢
  # setOnRemoveConfigurationSet() �ǥ��åȤ��줿������Хå��ؿ�����
  # �ӽФ���롣
  #
  # @param self 
  # @param config_id ����оݥ���ե�����졼����󥻥åȤ�ID
  #
  # @return ����������(�������:true���������:false)
  #
  # @else
  #
  # @brief Remove the configuration set
  # 
  # Remove the configuration set of specified ID Return empty
  # configuration set, if a configuration set of specified ID
  # doesn't exist.
  #
  # The configuration-sets that can be removed by this function are
  # only configuration-sets newly added by the
  # addConfigurationSet() function. The configuration that can be
  # removed by this function is only newly added configuration-set
  # by addConfigurationSet() function.  The "default"
  # configuration-set and configurationi-sets that is loaded from
  # configuration file cannot be removed.
  #
  # If the specified configuration is active currently, any
  # configurations are not deleted.
  #
  # Callback functions that are set by
  # addOnRemovedConfigurationSet() will be called if a
  # configuration-set is deleted actually by this function.
  #
  # @param self 
  # @param config_id ID of the target configuration set for remove
  #
  # @return Remove result (Successful:true, Failed:false)
  #
  # @endif
  #
  # bool removeConfigurationSet(const char* config_id);
  def removeConfigurationSet(self, config_id):
    if config_id == "default":
      return False
    if self._activeId == config_id:
      return False

    find_flg = False
    # removeable config-set is only config-sets newly added
    for (idx,conf) in enumerate(self._newConfig):
      if conf == config_id:
        find_flg = True
        break


    if not find_flg:
      return False

    p = self._configsets.getNode(config_id)
    if p:
      p.getRoot().removeNode(config_id)
      del p

    del self._newConfig[idx]

    self._changed = True
    self._active  = False
    self.onRemoveConfigurationSet(config_id)
    return True


  ##
  # @if jp
  # 
  # @brief ����ե�����졼����󥻥åȤΥ����ƥ��ֲ�
  # 
  # ���ꤷ��ID�Υ���ե�����졼����󥻥åȤ򥢥��ƥ��ֲ����롣
  # ���ꤷ��ID�Υ���ե�����졼����󥻥åȤ�¸�ߤ��ʤ����ϡ�
  # false���֤���
  # 
  # @param self 
  # @param config_id ����оݥ���ե�����졼����󥻥åȤ�ID
  # 
  # @return �����ƥ��ֽ������(����:true������:false)
  # 
  # @else
  # 
  # @brief Activate the configuration set
  # 
  # Activate the configuration set of specified ID
  # Return empty configuration set, if a configuration set of
  # specified ID doesn't exist.
  #
  # @param self 
  # @param config_id ID of the target configuration set for remove
  #
  # @return Activate result (Remove success:true��Remove failure:false)
  # 
  # @endif
  # bool activateConfigurationSet(const char* config_id);
  def activateConfigurationSet(self, config_id):
    if config_id is None:
      return False

    # '_<conf_name>' is special configuration set name
    if config_id[0] == '_':
      return False

    if not self._configsets.hasKey(config_id):
      return False
    self._activeId = config_id
    self._active   = True
    self._changed  = True
    self.onActivateSet(config_id)
    return True


  #------------------------------------------------------------
  # obsolete functions
  #

  ##
  # @if jp
  #
  # @brief OnUpdate �Υ�����Хå�������
  #
  # OnUpdate �ǸƤФ�륳����Хå��Υ��֥������Ȥ����ꤹ�롣
  # 
  # @param self 
  # @param cb OnUpdateCallback���Υ��֥�������
  #
  # @else
  #
  # @brief Set callback that is called by OnUpdate. 
  # 
  # @param self 
  # @param cb OnUpdateCallback type object
  #
  # @endif
  #
  # void setOnUpdate(OnUpdateCallback* cb);
  def setOnUpdate(self, cb):
    print "setOnUpdate function is obsolete."
    print "Use addConfigurationSetNameListener instead."
    self._listeners.configsetname_[OpenRTM_aist.ConfigurationSetNameListenerType.ON_UPDATE_CONFIG_SET].addListener(cb, False)
    return


  ##
  # @if jp
  #
  # @brief OnUpdateParam �Υ�����Хå�������
  #
  # OnUpdateParam �ǸƤФ�륳����Хå��Υ��֥������Ȥ����ꤹ�롣
  # 
  # @param self 
  # @param cb OnUpdateParamCallback���Υ��֥�������
  #
  # @else
  #
  # @brief Set callback that is called by OnUpdateParam. 
  # 
  # @param self 
  # @param cb OnUpdateParamCallback type object
  #
  # @endif
  #
  # void setOnUpdateParam(OnUpdateParamCallback* cb);
  def setOnUpdateParam(self, cb):
    print "setOnUpdateParam function is obsolete."
    print "Use addConfigurationParamListener instead."
    self._listeners.configparam_[OpenRTM_aist.ConfigurationParamListenerType.ON_UPDATE_CONFIG_PARAM].addListener(cb, False)
    return


  ##
  # @if jp
  #
  # @brief OnSetConfigurationSet �Υ�����Хå�������
  #
  # OnSetConfigurationSet �ǸƤФ�륳����Хå��Υ��֥������Ȥ����ꤹ�롣
  # 
  # @param self 
  # @param cb OnSetConfigurationSetCallback���Υ��֥�������
  #
  # @else
  #
  # @brief Set callback that is called by OnSetConfiguration. 
  # 
  # @param self 
  # @param cb OnSetConfigurationSetCallback type object
  #
  # @endif
  #
  # void setOnSetConfigurationSet(OnSetConfigurationSetCallback* cb);
  def setOnSetConfigurationSet(self, cb):
    print "setOnSetConfigurationSet function is obsolete."
    print "Use addConfigurationSetListener instead."
    self._listeners.configset_[OpenRTM_aist.ConfigurationSetListenerType.ON_SET_CONFIG_SET].addListener(cb, False)
    return


  ##
  # @if jp
  #
  # @brief OnAddConfigurationSet �Υ�����Хå�������
  #
  # OnAddConfigurationSet �ǸƤФ�륳����Хå��Υ��֥������Ȥ����ꤹ�롣
  # 
  # @param self 
  # @param cb OnAddConfigurationAddCallback���Υ��֥�������
  #
  # @else
  #
  # @brief Set callback that is called by OnSetConfiguration. 
  # 
  # @param self 
  # @param cb OnSetConfigurationSetCallback type object
  #
  # @endif
  #
  # void setOnAddConfigurationSet(OnAddConfigurationAddCallback* cb);
  def setOnAddConfigurationSet(self, cb):
    print "setOnAddConfigurationSet function is obsolete."
    print "Use addConfigurationSetListener instead."
    self._listeners.configset_[OpenRTM_aist.ConfigurationSetListenerType.ON_ADD_CONFIG_SET].addListener(cb, False)
    return


  ##
  # @if jp
  #
  # @brief OnRemoveConfigurationSet �Υ�����Хå�������
  #
  # OnRemoveConfiguration �ǸƤФ�륳����Хå��Υ��֥������Ȥ����ꤹ�롣
  # 
  # @param self 
  # @param cb OnRemoveConfigurationSetCallback���Υ��֥�������
  #
  # @else
  #
  # @brief Set callback that is called by OnRemoveConfigurationSet. 
  # 
  # @param self 
  # @param cb OnRemoveConfigurationSetCallback type object
  #
  # @endif
  #
  # void setOnRemoveConfigurationSet(OnRemoveConfigurationSetCallback* cb);
  def setOnRemoveConfigurationSet(self, cb):
    print "setOnRemoveConfigurationSet function is obsolete."
    print "Use addConfigurationSetNameListener instead."
    self._listeners.configsetname_[OpenRTM_aist.ConfigurationSetNameListenerType.ON_REMOVE_CONFIG_SET].addListener(cb, False)
    return


  ##
  # @if jp
  #
  # @brief OnActivateSet �Υ�����Хå�������
  #
  # OnActivateSet �ǸƤФ�륳����Хå��Υ��֥������Ȥ����ꤹ�롣
  # 
  # @param self 
  # @param cb OnActivateSetCallback���Υ��֥�������
  #
  # @else
  #
  # @brief Set callback that is called by OnActivateSet. 
  # 
  # @param self 
  # @param cb OnActivateSetCallback type object
  #
  # @endif
  #
  # void setOnActivateSet(OnActivateSetCallback* cb);
  def setOnActivateSet(self, cb):
    print "setOnActivateSet function is obsolete."
    print "Use addConfigurationSetNameListener instead."
    self._listeners.configsetname_[OpenRTM_aist.ConfigurationSetNameListenerType.ON_ACTIVATE_CONFIG_SET].addListener(cb, False)
    return

  #
  # end of obsolete functions
  #------------------------------------------------------------

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
  # @param listener ConfigurationParamListener ���Υꥹ�ʥ��֥������ȡ�
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
  # @param listener ConfigurationParamListener listener object.
  # @param autoclean a flag whether if the listener object autocleaned.
  #
  # @endif
  #
  # void addConfigurationParamListener(ConfigurationParamListenerType type,
  #                                    ConfigurationParamListener* listener,
  #                                    bool autoclean = true);
  def addConfigurationParamListener(self, type, listener, autoclean = True):
    self._listeners.configparam_[type].addListener(listener, autoclean)
    return


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
    self._listeners.configparam_[type].removeListener(listener)
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
  # @param listener ConfigurationSetListener ���Υꥹ�ʥ��֥������ȡ�
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
  # @param listener ConfigurationSetListener listener object.
  # @param autoclean a flag whether if the listener object autocleaned.
  #
  # @endif
  #
  # void addConfigurationSetListener(ConfigurationSetListenerType type,
  #                                  ConfigurationSetListener* listener,
  #                                  bool autoclean = true);
  def addConfigurationSetListener(self, type, listener, autoclean = True):
    self._listeners.configset_[type].addListener(listener, autoclean)
    return


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
  # void removeConfigurationSetListener(ConfigurationSetListenerType type,
  #                                     ConfigurationSetListener* listener);
  def removeConfigurationSetListener(self, type, listener):
    self._listeners.configset_[type].removeListener(listener)
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
  # @param listener ConfigurationSetNameListener ���Υꥹ�ʥ��֥������ȡ�
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
  # @param listener ConfigurationSetNameListener listener object.
  # @param autoclean a flag whether if the listener object autocleaned.
  #
  # @endif
  # void 
  # addConfigurationSetNameListener(ConfigurationSetNameListenerType type,
  #                                 ConfigurationSetNameListener* listener,
  #                                 bool autoclean = true);
  def addConfigurationSetNameListener(self, type, listener, autoclean = True):
    self._listeners.configsetname_[type].addListener(listener, autoclean)
    return


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
    self._listeners.configsetname_[type].removeListener(listener)
    return
    

  ##
  # @if jp
  #
  # @brief ����ե�����졼�����ѥ�᡼���ι���(ID����)���˥����뤵���
  #
  # ���ꤵ��Ƥ륳����Хå����֥������Ȥ�ƤӽФ���
  #
  # @param self 
  # @param config_set �����оݤΥ���ե�����졼����󥻥å�ID
  #
  # @else
  #
  # @brief When the configuration parameter is updated, it is called. 
  #
  # Call the set callback object.
  # 
  # @param self 
  # @param config_set The target configuration set's ID to setup
  #
  # @endif
  #
  # void onUpdate(const char* config_set);
  def onUpdate(self, config_set):
    self._listeners.configsetname_[OpenRTM_aist.ConfigurationSetNameListenerType.ON_UPDATE_CONFIG_SET].notify(config_set)
    return


  ##
  # @if jp
  #
  # @brief ����ե�����졼�����ѥ�᡼���ι���(̾�λ���)���˥����뤵���
  #
  # ���ꤵ��Ƥ륳����Хå����֥������Ȥ�ƤӽФ���
  #
  # @param self 
  # @param config_set ����ե�����졼�����ID
  # @param config_param ����ե�����졼�����ѥ�᡼��̾
  #
  # @else
  #
  # @brief When the configuration parameter is updated, it is called. 
  #
  # Call the set callback object.
  # 
  # @param self 
  # @param config_set configuration-set ID.
  # @param config_param configuration parameter name.
  #
  # @endif
  #
  # void onUpdateParam(const char* config_set, const char* config_param);
  def onUpdateParam(self, config_set, config_param):
    self._listeners.configparam_[OpenRTM_aist.ConfigurationParamListenerType.ON_UPDATE_CONFIG_PARAM].notify(config_set,
                                                                                                            config_param)
    return


  ##
  # @if jp
  #
  # @brief ����ե�����졼����󥻥åȤؤ��ɲû��˥����뤵���
  #
  # ���ꤵ��Ƥ륳����Хå����֥������Ȥ�ƤӽФ���
  #
  # @param self 
  # @param configuration_set �ץ�ѥƥ�
  #
  # @else
  #
  # @brief Called when the property is added to the configuration set
  #
  # Call the set callback object.
  # 
  # @param self 
  # @param configuration_set property
  #
  # @endif
  #
  # void onSetConfigurationSet(const coil::Properties& config_set);
  def onSetConfigurationSet(self, config_set):
    self._listeners.configset_[OpenRTM_aist.ConfigurationSetListenerType.ON_SET_CONFIG_SET].notify(config_set)
    return


  ##
  # @if jp
  #
  # @brief �����ͤ��ɲä��줿�Ȥ��˥����뤵��롣
  #
  # ���ꤵ��Ƥ륳����Хå����֥������Ȥ�ƤӽФ���
  #
  # @param self 
  # @param configuration_set �ץ�ѥƥ�
  #
  # @else
  #
  # @brief Called when a set value is added to the configuration set
  #
  # Call the set callback object.
  # 
  # @param self 
  # @param configuration_set property
  #
  # @endif
  #
  # void onAddConfigurationSet(const coil::Properties& config_set);
  def onAddConfigurationSet(self, config_set):
    self._listeners.configset_[OpenRTM_aist.ConfigurationSetListenerType.ON_ADD_CONFIG_SET].notify(config_set)
    return


  ##
  # @if jp
  #
  # @brief ���åȤ��������Ƥ�Ȥ��˥����뤵��롣
  #
  # ���ꤵ��Ƥ륳����Хå����֥������Ȥ�ƤӽФ���
  #
  # @param self 
  # @param config_id �ץ�ѥƥ�
  #
  # @else
  #
  # @brief Called when the configuration set has been deleted
  #
  # Call the set callback object.
  # 
  # @param self 
  # @param config_id property
  #
  # @endif
  #
  # void onRemoveConfigurationSet(const char* config_id);
  def onRemoveConfigurationSet(self, config_id):
    self._listeners.configsetname_[OpenRTM_aist.ConfigurationSetNameListenerType.ON_REMOVE_CONFIG_SET].notify(config_id)
    return


  ##
  # @if jp
  #
  # @brief ���åȤ������ƥ��ֲ����줿�Ȥ��˥����뤵��롣
  #
  # ���ꤵ��Ƥ륳����Хå����֥������Ȥ�ƤӽФ���
  #
  # @param self 
  # @param config_id �ץ�ѥƥ�
  #
  # @else
  #
  # @brief Called when the configuration set is made active
  #
  # Call the set callback object.
  # 
  # @param self 
  # @param config_id property
  #
  # @endif
  #
  # void onActivateSet(const char* config_id);
  def onActivateSet(self, config_id):
    self._listeners.configsetname_[OpenRTM_aist.ConfigurationSetNameListenerType.ON_ACTIVATE_CONFIG_SET].notify(config_id)
    return


  class find_conf:
    def __init__(self, name):
      self._name = name
      return

    def __call__(self, conf):
      if conf is None or conf is 0:
        return False

      return self._name == conf.name
