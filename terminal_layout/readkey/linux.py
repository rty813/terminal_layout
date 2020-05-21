# -*- coding: utf-8 -*-
# Initially taken from:
# http://code.activestate.com/recipes/134892/
# Thanks to Danny Yoo
import os
import sys
import tty
import termios

from terminal_layout.logger import logger
from terminal_layout.readkey.key import Key


def readkey():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        c = os.read(fd, 3)
        try:
            c = str(c, encoding='utf-8')
        except:
            c = ''
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if c == Key.CTRL_C:
        raise KeyboardInterrupt
    return c


def readkey_old():
    fd = sys.stdin.fileno()
    old_ttyinfo = termios.tcgetattr(fd)
    # 配置终端
    new_ttyinfo = old_ttyinfo[:]

    # 使用非规范模式(索引3是c_lflag 也就是本地模式)
    new_ttyinfo[3] &= ~termios.ICANON
    # # 关闭回显(输入不会被显示)
    new_ttyinfo[3] &= ~termios.ECHO
    try:
        termios.tcsetattr(fd, termios.TCSANOW, new_ttyinfo)
        c = os.read(fd, 2)
        c = str(c, encoding='utf-8')
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_ttyinfo)
    if c == Key.CTRL_C:
        raise KeyboardInterrupt
    return c
