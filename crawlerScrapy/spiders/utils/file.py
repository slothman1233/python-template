from enum import Enum
from pathlib import Path
import os

import shutil

class file_read_enum(Enum):
    '''
    文件读取类型枚举

    Notes
    ----------
    default : 1
        读取全部
    readline ： 2
        读取第一行
    readlines ： 3
        逐行读取返回数组
    '''
    default = 1,
    readline = 2,
    readlines = 3

class file_write_enum(Enum):
    '''
    文件写入类型枚举

    Notes
    ----------
    default : 1
        覆盖
    addto ： 2
        追加

    '''
    default = 1,
    addto = 2

def file_read(path='', mode=file_read_enum.default, size=None):
    '''
    文件读取

    Parameters
    ----------
    path : string
        文件地址
    mode : file_read_enum
        文件读取类型
    size : int
        读取长度，值正对 mode = file_read_enum.default 的模式下有效


    Returns
    ----------
    string

    读取的内容

    '''
    try:
        with open(file=path, mode="r", encoding="utf-8") as fb:
            if mode == file_read_enum.default:
                return fb.read(size)
            elif mode == file_read_enum.readline:
                return fb.readline()
            elif mode == file_read_enum.readlines:
                return fb.readlines()
            else:
                return fb.read(size)
    except FileNotFoundError:
        print("文件不存在")
        return None
    except PermissionError:
        print("没有权限访问")
        return None

def file_write(path='', content='', mode=file_write_enum.default):
    '''
    文件写入

    Parameters
    ----------
    path : string
        文件地址
    content : string
        写入内容
    mode : file_write_enum
        写入模式



    Returns
    ----------
    boolean

    存在True
    否则False
    '''

    try:
        md = 'w' if mode == file_write_enum.default else 'a'

        with open(file=path, mode=md, encoding="utf-8") as fb:
            fb.write(content)
    except PermissionError:
        print("没有权限访问")
        return False
    except:
        print("写入失败")
        return False
    else:
        return True

def file_isexists(path):
    '''
    文件夹是否存在

    Parameters
    ----------
    path : string
        文件夹地址


    Returns
    ----------
    boolean

    存在True
    否则False
    '''
    return Path(path).is_dir()

def file_isfiles(path):
    '''
    文件是否存在

    Parameters
    ----------
    path : string
        文件地址


    Returns
    ----------
    boolean

    存在True
    否则False
    '''
    return Path(path).is_file()

def file_access(path, mode):
    '''
    判断文件是否可做读写操作

    Parameters
    ----------
    path : string
        文件地址
    mode : int
        os.F_OK: 检查文件是否存在;
        os.R_OK: 检查文件是否可读;
        os.W_OK: 检查文件是否可以写入;
        os.X_OK: 检查文件是否可以执行


    Returns
    ----------
    boolean

    存在True
    否则False
    '''
    return os.access(path, mode)

def del_folder(path):
    '''
    删除文件夹

    Parameters
    ----------
    path : string
        文件夹路径

    Returns
    ----------
    bool
    True 成功
    False 失败
    '''
    try:
        shutil.rmtree(path)
    except OSError as e:
        print(e)
        return False
    else:
        print("删除文件夹成功")
        return True

def del_file(filepath):
    '''
    删除文件

    Parameters
    ----------
    filepath : string
        文件路径

    Returns
    ----------
    bool
    True 成功
    False 失败
    '''
    try:
        os.remove(filepath)
    except OSError as e:
        print(e)
        return False
    else:
        print("删除文件成功")
        return True