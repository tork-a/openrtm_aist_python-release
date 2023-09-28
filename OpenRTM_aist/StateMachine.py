#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file StateMachine.py
# @brief State machine template class
# @date $Date: 2007/08/30$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import threading

import OpenRTM_aist
import RTC


##
# @if jp
# @class StateHolder
# @brief �����ݻ��ѥ��饹
# 
# ���֤��ݻ����뤿��Υۥ�������饹��
# ���ߤξ��֤ȡ��������ξ��֡�����ͽ��ξ��֤��ݻ����롣
#
# @param State �ݻ�������֤η�
#
# @since 0.4.0
#
# @else
#
# @endif
class StateHolder:
  def __init__(self):
    self.curr = None
    self.prev = None
    self.next = None


##
# @if jp
#
# @class StateMachine
#
# @brief ���֥ޥ��󥯥饹
#
# StateMachine ���饹�Ͼ��֥ޥ����¸����륯�饹�Ǥ��롣
#
# ��: ActiveObject�Ͼ��֥ޥ������ĥ����ƥ��֥��֥������ȤǤ���Ȥ��롣
# ���֤�3���� INACTIVE, ACTIVE, ERROR �����ꡢ�ƾ��֤Ǥ�Entry��Exitư���
# ����������Ȥ���ȡ��ʲ��Τ褦�˼¸�����롣
# <pre>
# class ActiveObject:
#   class MyState:
#     INACTIVE, ACTIVE, ERROR = range(3)
# 
#   def __init__(self):
#     m_sm = StateMachine(3)
#     m_sm.setNOP(nullAction)
#     m_sm.setListener(self)
# 
#     m_sm.setExitAction(MyState.INACTIVE, self.inactiveExit)
#       : 
#     m_sm.setPostDoAction(MyState.ERROR, self.errorPostDo)
#     m_sm.setTransitionAction(self.transition); 
# 
#   def nullAction(myStates):
#     pass
#   def inactiveExit(myStates):
#     pass
#     : 
#   def errorPostDo(myStates):
#     pass
#   def transition(myStates:
#     pass
# </pre>
# ���֤�������������饹�ϰʲ��ξ����������褦�˼������ʤ���Фʤ�ʤ���
# <ol>
# <li> �������饹�Ǿ��֤����
# <li> StateMachine �Υ��󥹥ȥ饯�������Ͼ��֤ο�
# <li> �ʲ��Υ��������ؿ���(Return _function_name_(States)) �δؿ��Ȥ�������
# <ol>
#  <li> ���⤷�ʤ��ؿ���ɬ���������setNOP ��Ϳ���ʤ���Фʤ�ʤ�
#  <li> �ƾ������, set(Entry|PreDo|Do|PostDo|Exit)Action �ǥ�������������
#  <li> �������ܻ��Υ��������� setTransitionAction() �����ꡣ
# </ol>
# <li> ���ܻ��Υ��������ϡ�Ϳ����줿���߾��֡������֡������֤򸵤ˡ�
#   �桼�����������ʤ���Фʤ�ʤ���
# <li> ���֤��ѹ��� goTo() �ǡ����֤Υ����å��� isIn(state) �ǹԤ���
# <li> goTo()�ϼ����֤���Ū�˥��åȤ���ؿ��Ǥ��ꡢ���ܤβ��ݤϡ�
#   �桼�������߾��֤������Ƚ�Ǥ�����å���������ʤ���Фʤ�ʤ���
# </ol>
#
# ���Υ��饹�ϡ���Ĥξ��֤��Ф��ơ�
# <ul>
# <li> Entry action
# <li> PreDo action
# <li> Do action
# <li> PostDo action
# <li> Exit action
# </ul>
# 5�ĤΥ��������������뤳�Ȥ��Ǥ��롣
# Transition action �Ϥ�������ִ����ܤǸƤӽФ���륢�������ǡ�
# ���ο����񤤤ϥ桼����������ʤ���Фʤ�ʤ���
# 
# ���Υ��饹�ϰʲ��Τ褦�ʥ����ߥ󥰤ǳƥ�������󤬼¹Ԥ���롣
#
# <ul>
# <li> ���֤��ѹ�����(A->B)���֤����ܤ����� <br>
# (A:Exit)->|(���ֹ���:A->B)->(B:Entry)->(B:PreDo)->(B:Do)->(B:PostDo)
#
# <li> ���֤��ѹ����줺��B���֤�ݻ������� (|�ϥ��ƥåפζ��ڤ��ɽ��)<br>
# (B(n-1):PostDo)->|(B(n):PreDo)->(B(n):Do)->(B(n):PostDo)->|(B(n+1):PreDo)<br>
# PreDo, Do, PostDo �������֤��¹Ԥ���롣
#
# <li> �������ܤ����� <br>
# (B(n-1):PostDo)->(B(n-1):Exit)->|(B(n):Entry)->(B(n):PreDo) <br>
# ��ö Exit ���ƤФ줿�塢Entry ���¹Ԥ��졢�ʹߤ������Ʊ��ư��򤹤롣
# </ul>
#
# @since 0.4.0
#
# @else
#
# @brief
#
# @endif
class StateMachine:
  """
  """

  state_array = (RTC.CREATED_STATE,
                 RTC.INACTIVE_STATE,
                 RTC.ACTIVE_STATE,
                 RTC.ERROR_STATE)

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param num_of_state ���ơ��ȥޥ�����ξ��ֿ�
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self, num_of_state):
    self._num = num_of_state
    self._entry  = {}
    self._predo  = {}
    self._do     = {}
    self._postdo = {}
    self._exit   = {}

    self.setNullFunc(self._entry,  None)
    self.setNullFunc(self._do,     None)
    self.setNullFunc(self._exit,   None)
    self.setNullFunc(self._predo,  None)
    self.setNullFunc(self._postdo, None)
    self._transit = None
    self._mutex = threading.RLock()


  ##
  # @if jp
  # @brief NOP�ؿ�����Ͽ����
  #
  # NOP�ؿ�(���⤷�ʤ��ؿ�)����Ͽ���롣
  #
  # @param self
  # @param call_back ������Хå��ؿ�
  #
  # @else
  # @brief Set NOP function
  # @endif
  def setNOP(self, call_back):
    self.setNullFunc(self._entry,  call_back)
    self.setNullFunc(self._do,     call_back)
    self.setNullFunc(self._exit,   call_back)
    self.setNullFunc(self._predo,  call_back)
    self.setNullFunc(self._postdo, call_back)
    self._transit = call_back


  ##
  # @if jp
  # @brief Listener ���֥������Ȥ���Ͽ����
  #
  # �Ƽ異�������¹Ի��˸ƤӽФ���� Listener ���֥������Ȥ���Ͽ���롣
  #
  # @param self
  # @param listener Listener ���֥�������
  #
  # @else
  # @brief Set Listener Object
  # @endif
  def setListener(self, listener):
    self._listener = listener


  ##
  # @if jp
  # @brief Entry action �ؿ�����Ͽ����
  #
  # �ƾ��֤����ä��ݤ˼¹Ԥ���� Entry action �ѥ�����Хå��ؿ�����Ͽ���롣
  #
  # @param self
  # @param state ��Ͽ�оݾ���
  # @param call_back Entry action �ѥ�����Хå��ؿ�
  #
  # @return ���������¹Է��
  #
  # @else
  # @brief Set Entry action function
  # @endif
  def setEntryAction(self, state, call_back):
    if self._entry.has_key(state):
      self._entry[state] = call_back
    else:
      self._entry.setdefault(state, call_back)
    return True


  ##
  # @if jp
  # @brief PreDo action �ؿ�����Ͽ����
  #
  # �ƾ�����Ǽ¹Ԥ���� PreDo action �ѥ�����Хå��ؿ�����Ͽ���롣
  #
  # @param self
  # @param state ��Ͽ�оݾ���
  # @param call_back PreDo action �ѥ�����Хå��ؿ�
  #
  # @return ���������¹Է��
  #
  # @else
  # @brief Set PreDo action function
  # @endif
  def setPreDoAction(self, state, call_back):
    if self._predo.has_key(state):
      self._predo[state] = call_back
    else:
      self._predo.setdefault(state, call_back)
    return True


  ##
  # @if jp
  # @brief Do action �ؿ�����Ͽ����
  #
  # �ƾ�����Ǽ¹Ԥ���� Do action �ѥ�����Хå��ؿ�����Ͽ���롣
  #
  # @param self
  # @param state ��Ͽ�оݾ���
  # @param call_back Do action �ѥ�����Хå��ؿ�
  #
  # @return ���������¹Է��
  #
  # @else
  # @brief Set Do action function
  # @endif
  def setDoAction(self, state, call_back):
    if self._do.has_key(state):
      self._do[state] = call_back
    else:
      self._do.setdefault(state, call_back)
    return True


  ##
  # @if jp
  # @brief PostDo action �ؿ�����Ͽ����
  #
  # �ƾ�����Ǽ¹Ԥ���� PostDo action �ѥ�����Хå��ؿ�����Ͽ���롣
  #
  # @param self
  # @param state ��Ͽ�оݾ���
  # @param call_back PostDo action �ѥ�����Хå��ؿ�
  #
  # @return ���������¹Է��
  #
  # @else
  # @brief Set PostDo action function
  # @endif
  def setPostDoAction(self, state, call_back):
    if self._postdo.has_key(state):
      self._postdo[state] = call_back
    else:
      self._postdo.setdefault(state, call_back)
    return True


  ##
  # @if jp
  # @brief Exit action �ؿ�����Ͽ����
  #
  # �ƾ�����Ǽ¹Ԥ���� Exit action �ѥ�����Хå��ؿ�����Ͽ���롣
  #
  # @param self
  # @param state ��Ͽ�оݾ���
  # @param call_back Exit action �ѥ�����Хå��ؿ�
  #
  # @return ���������¹Է��
  #
  # @else
  # @brief Set Exit action function
  # @endif
  def setExitAction(self, state, call_back):
    if self._exit.has_key(state):
      self._exit[state] = call_back
    else:
      self._exit.setdefault(state, call_back)
    return True


  ##
  # @if jp
  # @brief State transition action �ؿ�����Ͽ����
  #
  # �������ܻ��˼¹Ԥ���� State transition action �ѥ�����Хå��ؿ���
  # ��Ͽ���롣
  #
  # @param self
  # @param call_back State transition �ѥ�����Хå��ؿ�
  #
  # @return ���������¹Է��
  #
  # @else
  # @brief Set state transition action function
  # @endif
  def setTransitionAction(self, call_back):
    self._transit = call_back
    return True


  ##
  # @if jp
  # @brief ������֤򥻥åȤ���
  #
  # ���ơ��ȥޥ���ν�����֤����ꤹ�롣
  #
  # @param self
  # @param states �������
  #
  # @else
  # @brief Set Exit action function
  # @endif
  def setStartState(self, states):
    self._states = StateHolder()
    self._states.curr = states.curr
    self._states.prev = states.prev
    self._states.next = states.next


  ##
  # @if jp
  # @brief ���֤��������
  #
  # ���־����������롣
  # ���ߤξ��֡��������ξ��֡�����ͽ��ξ��֤�������뤳�Ȥ��Ǥ��롣
  #
  # @param self
  #
  # @return ���־���
  #
  # @else
  # @brief Get state machine's status
  # @endif
  def getStates(self):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    return self._states


  ##
  # @if jp
  # @brief ���ߤξ��֤��������
  #
  # ���ߤξ��֤�������롣
  #
  # @param self
  #
  # @return ���ߤξ���
  #
  # @else
  # @brief Get current state
  # @endif
  def getState(self):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    return self._states.curr


  ##
  # @if jp
  # @brief ���߾��֤��ǧ
  #
  # ���ߤξ��֤��������ǻ��ꤷ�����֤Ȱ��פ��뤫��ǧ���롣
  #
  # @param self
  # @param state ��ǧ�оݾ���
  #
  # @return ���ֳ�ǧ���
  #
  # @else
  # @brief Evaluate current status
  # @endif
  def isIn(self, state):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    if self._states.curr == state:
      return True
    else:
      return False


  ##
  # @if jp
  # @brief ���֤�����
  #
  # ���ꤷ�����֤˾��֤����ܤ��롣
  # �ܴؿ��ϼ����֤���Ū�˥��åȤ���ؿ��Ǥ��롣
  # ���Τ��ᡢ���ܤβ��ݤϡ��桼�������߾��֤������Ƚ�Ǥ�����å���
  # �������ʤ���Фʤ�ʤ���
  # �����褬���ߤξ��֤�Ʊ�����ˤϡ��������ܥե饰�򥻥åȤ��롣
  #
  # @param self
  # @param state ���������
  #
  # @else
  # @brief Change status
  # @endif
  def goTo(self, state):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    self._states.next = state


  ##
  # @if jp
  # @brief ��ư�ؿ�
  #
  # ���ơ��ȥޥ���ζ�ư�ؿ���
  # �ºݤξ������ܤ���Ӿ�������ȯ�����γƥ��������θƤӤ�����¹Ԥ��롣
  #
  # @param self
  #
  # @else
  # @brief Worker function
  # @endif
  def worker(self):
    states = StateHolder()
    self.sync(states)

    # If no state transition required, execute set of do-actions
    if states.curr == states.next:
      # pre-do
      if self._predo[states.curr]:
        self._predo[states.curr](states)
      if self.need_trans():
        return

      # do
      if self._do[states.curr]:
        self._do[states.curr](states)
      if self.need_trans():
        return

      # post-do
      if self._postdo[states.curr]:
        self._postdo[states.curr](states)
    # If state transition required, exit current state and enter next state
    else:
      if self._exit[states.curr]:
        self._exit[states.curr](states)
      self.sync(states)

      # If state transition still required, move to the next state
      if states.curr != states.next:
        states.curr = states.next
        if self._entry[states.curr]:
          self._entry[states.curr](states)
        self.update_curr(states.curr)


  ##
  # @if jp
  # @brief NOP�ؿ�������
  #
  # NOP�ؿ�(���⤷�ʤ��ؿ�)����Ͽ���롣
  #
  # @param self
  # @param s ������Хå��ؿ�������
  # @param nullfunc ������Хå��ؿ�(NOP�ؿ�)
  #
  # @else
  # @brief Worker function
  # @endif
  def setNullFunc(self, s, nullfunc):
    for i in range(self._num):
      if s.has_key(StateMachine.state_array[i]):
        s[StateMachine.state_array[i]] = nullfunc
      else:
        s.setdefault(StateMachine.state_array[i], nullfunc)


  ##
  # @if jp
  # @brief ���֤�Ʊ������
  #
  # @param self
  # @param states OpenRTM_aist.StateHolder<RTC.LifeCycleState>
  #
  # @else
  # @endif
  def sync(self, states):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    states.prev = self._states.prev
    states.curr = self._states.curr
    states.next = self._states.next
    


  ##
  # @if jp
  # @brief ���ܤ�ɬ���������å�
  #
  # @param self
  #
  # @return ����ɬ������ǧ���
  #
  # @else
  # @endif
  def need_trans(self):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    return (self._states.curr != self._states.next)


  ##
  # @if jp
  # @brief ���߾��֤ι���
  #
  # @param self
  # @param curr RTC.LifeCycleState
  #
  # @else
  # @endif
  def update_curr(self, curr):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    self._states.curr = curr
