#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ModuleManager.py
# @brief Loadable modules manager class
# @date $Date: 2007/08/24$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import string
import sys,os
import glob

import OpenRTM_aist


CONFIG_EXT    = "manager.modules.config_ext"
CONFIG_PATH   = "manager.modules.config_path"
DETECT_MOD    = "manager.modules.detect_loadable"
MOD_LOADPTH   = "manager.modules.load_path"
INITFUNC_SFX  = "manager.modules.init_func_suffix"
INITFUNC_PFX  = "manager.modules.init_func_prefix"
ALLOW_ABSPATH = "manager.modules.abs_path_allowed"
ALLOW_URL     = "manager.modules.download_allowed"
MOD_DWNDIR    = "manager.modules.download_dir"
MOD_DELMOD    = "manager.modules.download_cleanup"
MOD_PRELOAD   = "manager.modules.preload"



##
# @if jp
#
# @brief �⥸�塼��ޥ͡����㥯�饹
# @class ModuleManager
#
# �⥸�塼��Υ��ɡ�������ɤʤɤ�������륯�饹
#
# @since 0.4.0
#
# @else
#
# @biref ModuleManager class
#
# @endif
class ModuleManager:
  """
  """



  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯����
  # ���ꤵ�줿 Property ���֥���������ξ�����˽������¹Ԥ��롣
  #
  # @param self
  # @param prop ������ѥץ�ѥƥ�
  #
  # @else
  #
  # @brief constructor
  #
  # @endif
  def __init__(self, prop):
    self._properties = prop

    self._configPath = prop.getProperty(CONFIG_PATH).split(",")
    for i in range(len(self._configPath)):
      tmp = [self._configPath[i]]
      OpenRTM_aist.eraseHeadBlank(tmp)
      self._configPath[i] = tmp[0]
    self._loadPath = prop.getProperty(MOD_LOADPTH,"./").split(",")
    for i in range(len(self._loadPath)):
      tmp = [self._loadPath[i]]
      OpenRTM_aist.eraseHeadBlank(tmp)
      self._loadPath[i] = tmp[0]

    self._absoluteAllowed = OpenRTM_aist.toBool(prop.getProperty(ALLOW_ABSPATH),
                                                "yes", "no", False)

    self._downloadAllowed = OpenRTM_aist.toBool(prop.getProperty(ALLOW_URL),
                                                "yes", "no", False)

    self._initFuncSuffix = prop.getProperty(INITFUNC_SFX)
    self._initFuncPrefix = prop.getProperty(INITFUNC_PFX)
    self._modules = OpenRTM_aist.ObjectManager(self.DLLPred)
    self._rtcout = None
    self._mgr = OpenRTM_aist.Manager.instance()

  ##
  # @if jp
  #
  # @brief �ǥ��ȥ饯��(̤����)
  #
  # @param self
  #
  # @else
  #
  # @brief destructor
  #
  # @endif
  def __del__(self):
    self.unloadAll()


  ##
  # @if jp
  # @class Error
  # @brief �ե����롦�����ץ����㳰�������������饹
  # @else
  #
  # @endif
  class Error:
    def __init__(self, reason_):
      self.reason = reason_



  ##
  # @if jp
  # @class NotFound
  # @brief ̤������������⥸�塼�������㳰�������������饹
  # @else
  #
  # @endif
  class NotFound:
    def __init__(self, name_):
      self.name = name_



  ##
  # @if jp
  # @class FileNotFound
  # @brief ����ե����������㳰�������������饹
  # @else
  #
  # @endif
  class FileNotFound(NotFound):
    def __init__(self, name_):
      ModuleManager.NotFound.__init__(self, name_)



  ##
  # @if jp
  # @class ModuleNotFound
  # @brief ����⥸�塼�������㳰�������������饹
  # @else
  #
  # @endif
  class ModuleNotFound(NotFound):
    def __init__(self, name_):
      ModuleManager.NotFound.__init__(self, name_)



  ##
  # @if jp
  # @class SymbolNotFound
  # @brief ���ꥷ��ܥ������㳰�������������饹
  # @else
  #
  # @endif
  class SymbolNotFound(NotFound):
    def __init__(self, name_):
      ModuleManager.NotFound.__init__(self, name_)



  ##
  # @if jp
  # @class NotAllowedOperation
  # @brief �������ػ߻��㳰�������������饹
  # @else
  #
  # @endif
  class NotAllowedOperation(Error):
    def __init__(self, reason_):
      ModuleManager.Error.__init__(self, reason_)
      ModuleManager.Error.__init__(self, reason_)



  ##
  # @if jp
  # @class InvalidArguments
  # @brief ��������������㳰�������������饹
  # @else
  #
  # @endif
  class InvalidArguments(Error):
    def __init__(self, reason_):
      ModuleManager.Error.__init__(self, reason_)



  ##
  # @if jp
  # @class InvalidOperation
  # @brief ��������������㳰�������������饹
  # @else
  #
  # @endif
  class InvalidOperation(Error):
    def __init__(self, reason_):
      ModuleManager.Error.__init__(self, reason_)



  ##
  # @if jp
  #
  # @brief �⥸�塼��Υ��ɡ������
  #
  # ���ꤷ���ե������ͭ�饤�֥��Ȥ��ƥ��ɤ���ȤȤ�ˡ�
  # ���ꤷ��������ѥ��ڥ졼������¹Ԥ��롣
  # 
  # @param self
  # @param file_name �����оݥ⥸�塼��̾ (.py��������ե�����̾)
  # @param init_func ����������ѥ��ڥ졼�����(�ǥե������:None)
  #
  # @return ���ꤷ�������оݥ⥸�塼��̾
  #
  # @else
  #
  # @brief Load module
  #
  #
  # @endif
  # std::string ModuleManager::load(const std::string& file_name,
  #                                 const std::string& init_func)
  def load(self, file_name, init_func=None):
    if not self._rtcout:
      self._rtcout = self._mgr.getLogbuf("ModuleManager")

    self._rtcout.RTC_TRACE("load(fname = %s)", file_name)
    if file_name == "":
      raise ModuleManager.InvalidArguments, "Invalid file name."

    if OpenRTM_aist.isURL(file_name):
      if not self._downloadAllowed:
        raise ModuleManager.NotAllowedOperation, "Downloading module is not allowed."
      else:
        raise ModuleManager.NotFound, "Not implemented."

    import_name = os.path.split(file_name)[-1]
    pathChanged=False
    file_path = None
    if OpenRTM_aist.isAbsolutePath(file_name):
      if not self._absoluteAllowed:
        raise ModuleManager.NotAllowedOperation, "Absolute path is not allowed"
      else:
        splitted_name = os.path.split(file_name)
        save_path = sys.path[:]
        sys.path.append(splitted_name[0])
        pathChanged = True
        import_name = splitted_name[-1]
        file_path = file_name

    else:
      file_path = self.findFile(file_name, self._loadPath)
      if not file_path:
        raise ModuleManager.InvalidArguments, "Invalid file name."

    if not self.fileExist(file_path):
      raise ModuleManager.FileNotFound, file_name

    if not pathChanged:
      splitted_name = os.path.split(file_path)
      sys.path.append(splitted_name[0])

    ext_pos = import_name.find(".py")
    if ext_pos > 0:
      import_name = import_name[:ext_pos]
    mo = __import__(str(import_name))

    if pathChanged:
      sys.path = save_path

    dll = self.DLLEntity(mo,OpenRTM_aist.Properties())
    dll.properties.setProperty("file_path",file_path)
    self._modules.registerObject(dll)


    if init_func is None:
      return file_name

    self.symbol(file_path,init_func)(self._mgr)

    return file_name


  ##
  # @if jp
  # @brief �⥸�塼��Υ������
  #
  # ���ꤷ�����ɺѤߥ⥸�塼��򥯥�������������ɤ��롣
  #
  # @param self
  # @param file_name ��������оݥ⥸�塼��̾
  #
  # @else
  # @brief Unload module
  # @endif
  def unload(self, file_name):
    dll = self._modules.find(file_name)
    if not dll:
      raise ModuleManager.NotFound, file_name

    self._modules.unregisterObject(file_name)
    return


  ##
  # @if jp
  # @brief ���⥸�塼��Υ������
  #
  # ���ƤΥ��ɺѤߥ⥸�塼��򥢥���ɤ��롣
  #
  # @param self
  #
  # @else
  # @brief Unload all modules
  # @endif
  def unloadAll(self):
    dlls = self._modules.getObjects()
    
    for dll in dlls:
      ident = dll.properties.getProperty("file_path")
      self._modules.unregisterObject(ident)
    return


  ##
  # @if jp
  # @brief �⥸�塼��Υ���ܥ�λ���
  #
  # �⥸�塼��Υ���ܥ���������
  #
  # @param self
  # @param file_name �����оݥե�����̾
  # @param func_name �����оݴؿ�̾
  #
  # @else
  # @brief Look up a named symbol in the module
  # @endif
  def symbol(self, file_name, func_name):
    dll = self._modules.find(file_name)
    if not dll:
      raise ModuleManager.ModuleNotFound, file_name

    func = getattr(dll.dll,func_name,None)

    if not func:
      raise ModuleManager.SymbolNotFound, func_name
    
    return func


  ##
  # @if jp
  # @brief �⥸�塼����ɥѥ�����ꤹ��
  # 
  # �⥸�塼����ɻ����оݥ⥸�塼��򸡺�����ѥ�����ꤹ�롣
  #
  # @param self
  # @param load_path_list �⥸�塼�븡���оݥѥ��ꥹ��
  #
  # @else
  # @brief Set default module load path
  # @endif
  def setLoadpath(self, load_path_list):
    self._loadPath = load_path_list
    return


  ##
  # @if jp
  # @brief �⥸�塼����ɥѥ����������
  # 
  # ���ꤵ��Ƥ���⥸�塼��򸡺��оݥѥ��ꥹ�Ȥ�������롣
  #
  # @param self
  # 
  # @return load_path �⥸�塼�븡���оݥѥ��ꥹ��
  #
  # @else
  # @brief Get default module load path
  # @endif
  def getLoadPath(self):
    return self._loadPath


  ##
  # @if jp
  # @brief �⥸�塼����ɥѥ����ɲä���
  # 
  # ���ꤵ�줿�ѥ��ꥹ�Ȥ򸡺��оݥѥ��ꥹ�Ȥ��ɲä��롣
  #
  # @param self
  # @param load_path �ɲå⥸�塼�븡���оݥѥ��ꥹ��
  #
  # @else
  # @brief Add module load path
  # @endif
  def addLoadpath(self, load_path):
    for path in load_path:
      self._loadPath.append(path)
    return


  ##
  # @if jp
  # @brief ���ɺѤߤΥ⥸�塼��ꥹ�Ȥ��������
  #
  # ���˥��ɺѤߤΥ⥸�塼��ꥹ�Ȥ�������롣
  #
  # @param self
  #
  # @return ���ɺѤߥ⥸�塼��ꥹ��
  #
  # @else
  # @brief Get loaded module names
  # @endif
  # std::vector<coil::Properties> getLoadedModules();
  def getLoadedModules(self):
    dlls = self._modules.getObjects()
    modules = []
    for dll in dlls:
      modules.append(dll.properties)

    return modules


  def __getRtcProfile(self, fname):
    # file name with full path
    fullname  = fname
    # directory name
    dirname   = os.path.dirname(fname)
    sys.path.append(dirname)
    # basename
    basename  = os.path.basename(fname)
    # classname
    classname  = basename.split(".")[0].lower()

    # loaded profile = old profiles - new profiles
    # for old
    oldp = self._mgr.getFactoryProfiles()

    # for new
    comp_spec_name = classname+"_spec"

    try:
      imp_file = __import__(basename.split(".")[0])
    except:
      return None
    comp_spec = getattr(imp_file,comp_spec_name,None)
    if not comp_spec:
      return None
    newp = OpenRTM_aist.Properties(defaults_str=comp_spec)

    profs = []
    
    exists = False
    for i in range(len(oldp)):
      if    oldp[i].getProperty("implementation_id") == newp.getProperty("implementation_id") and \
            oldp[i].getProperty("type_name") == newp.getProperty("type_name") and \
            oldp[i].getProperty("description") == newp.getProperty("description") and \
            oldp[i].getProperty("version") == newp.getProperty("version"):
        exists = True
    if not exists:
      profs.append(newp)

        
    # loaded component profile have to be one
    if len(profs) == 0:
      return OpenRTM_aist.Properties()

    if len(profs) > 1:
      return None

    return profs[0]


  ##
  # @if jp
  # @brief ���ɲ�ǽ�⥸�塼��ꥹ�Ȥ��������(̤����)
  #
  # ���ɲ�ǽ�ʥ⥸�塼��Υꥹ�Ȥ�������롣
  #
  # @param self
  #
  # @return ���ɲ�ǽ�⥸�塼��ꥹ��
  #
  # @else
  # @brief Get loadable module names
  # @endif
  def getLoadableModules(self):
    # getting loadable module file path list.
    modules_ = []
    for path in self._loadPath:
      if path == "":
        continue

      flist = glob.glob(path + os.sep + '*.py')
      for file in flist:
        if file.find("__init__.py") == -1:
          modules_.append(file)
    
    props = []
    # getting module properties from loadable modules
    for mod_ in modules_:
      prop = self.__getRtcProfile(mod_)
      if prop:
        prop.setProperty("module_file_name",os.path.basename(mod_))
        prop.setProperty("module_file_path", mod_)
        props.append(prop)

    return props



  ##
  # @if jp
  # @brief �⥸�塼������Хѥ��������
  #
  # �����оݥ⥸�塼������Хѥ��������Ĥ���褦�����ꤹ�롣
  #
  # @param self
  #
  # @else
  # @brief Allow absolute load path
  # @endif
  def allowAbsolutePath(self):
    self._absoluteAllowed = True


  ##
  # @if jp
  # @brief �⥸�塼������Хѥ�����ػ�
  #
  # �����оݥ⥸�塼������Хѥ������ػߤ���褦�����ꤹ�롣
  #
  # @param self
  #
  # @else
  # @brief Forbid absolute load path
  # @endif
  def disallowAbsolutePath(self):
    self._absoluteAllowed = False


  ##
  # @if jp
  # @brief �⥸�塼���URL�������
  #
  # �����оݥ⥸�塼���URL�������Ĥ��롣
  # �����꤬���Ĥ���Ƥ����硢�⥸�塼����������ɤ��ƥ��ɤ��뤳�Ȥ�
  # ���Ĥ���롣
  #
  # @param self
  #
  # @else
  # @brief Allow module download
  # @endif
  def allowModuleDownload(self):
    self._downloadAllowed = True


  ##
  # @if jp
  # @brief �⥸�塼���URL����ػ�
  #
  # �����оݥ⥸�塼���URL�����ػߤ��롣
  #
  # @param self
  #
  # @else
  # @brief Forbid module download
  # @endif
  def disallowModuleDownload(self):
    self._downloadAllowed = False


  ##
  # @if jp
  # @brief LoadPath ����Υե�����θ���
  # 
  # ���ꤵ�줿�ѥ���ˡ����ꤵ�줿�ե����뤬¸�ߤ��뤫��ǧ���롣
  #
  # @param self
  # @param fname �����оݥե�����̾
  # @param load_path ������ѥ��ꥹ��
  #
  # @return �������줿�ե�����̾
  #
  # @else
  # @brief Search file from load path
  # @endif
  def findFile(self, fname, load_path):
    file_name = fname
    for path in load_path:
      if fname.find(".py") == -1:
        f = str(path) + os.sep + str(file_name)+".py"
      else:
        f = str(path)+ os.sep + str(file_name)
      if self.fileExist(f):
        return f
    return ""


  ##
  # @if jp
  # @brief �ե����뤬¸�ߤ��뤫�ɤ����Υ����å�
  #
  # ���ꤵ�줿�ե����뤬¸�ߤ��뤫��ǧ���롣
  #
  # @param self
  # @param filename ¸�߳�ǧ�оݥե�����̾
  #
  # @return �ե�����¸�߳�ǧ���(�ե����뤢��:true���ʤ�:false)
  #
  # @else
  # @brief Check file existance
  # @endif
  def fileExist(self, filename):
    fname = filename
    if fname.find(".py") == -1:
      fname = str(filename)+".py"

    if os.path.isfile(fname):
      return True

    return False



  ##
  # @if jp
  # @brief ������ؿ�����ܥ����������
  #
  # ������ؿ���̾�Τ��Ȥ�Ω�Ƥ롣
  #
  # @param self
  # @param file_path ������оݥ⥸�塼��̾��
  #
  # @return ������ؿ�̾���Ȥ�Ω�Ʒ��
  #
  # @else
  # @brief Create initialize function symbol
  # @endif
  def getInitFuncName(self, file_path):
    base_name = os.path.basename(file_path)
    return str(self._initFuncPrefix)+str(base_name)+str(self._initFuncSuffix)



  ##
  # @if jp
  # @class DLL
  # @brief �⥸�塼���ݻ����������饹
  # @else
  #
  # @endif
  class DLL:
    def __init__(self, dll):
      self.dll = dll
      return


  class DLLEntity:
    def __init__(self,dll,prop):
      self.dll = dll
      self.properties = prop


  class DLLPred:
    def __init__(self, name=None, factory=None):
      self._filepath = name or factory

    def __call__(self, dll):
      return self._filepath == dll.properties.getProperty("file_path")
