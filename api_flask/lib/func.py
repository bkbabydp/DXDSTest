# -*- coding: UTF-8 -*-


from typing import Iterable

__author__ = 'David Zhang'


def isstr(obj):
    """判断对象是否是字符串

    :param obj:
    :return:
    :rtype: bool
    """
    return isinstance(obj, str)


def isfunction(obj):
    """判断对象是否是函数

    :param obj:
    :return:
    :rtype: bool
    """
    return hasattr(obj, '__call__')


def isiterable(obj):
    """判断对象是否可遍历

    :param obj:
    :return:
    :rtype: bool
    """
    return isinstance(obj, Iterable)


def zfill(obj, width):
    """返回长度为 width 的字符串，前面其余部分用 0 填充

    :param obj:
    :param width:
    :type width: int
    :return:
    :rtype: str
    """
    s = str(obj)
    l = len(s)
    return s.zfill(width)[l - width if l > width else 0:]
