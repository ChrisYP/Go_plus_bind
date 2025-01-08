# -*- coding: utf-8 -*-
# @Time    : 2024/6/23 21:17
# @Author  : Chris
# @Email   : 10512@qq.com
# @File    : utils.py
# @Software: PyCharm
import asyncio
import os
import signal
from typing import Callable

import base64

from binascii import a2b_hex
from binascii import b2a_hex

from Crypto.Cipher import AES

from Crypto.Util.Padding import pad
from loguru import logger


def suicide(endingFunc: Callable = None) -> None:
    """程序自杀"""
    if endingFunc:
        if asyncio.iscoroutinefunction(endingFunc):
            hasattr(
                asyncio, "WindowsSelectorEventLoopPolicy"
            ) and asyncio.set_event_loop_policy(
                asyncio.WindowsSelectorEventLoopPolicy()
            )
            asyncio.run(endingFunc())
        else:
            endingFunc()
    logger.warning("Process finished with exit code 15")
    os.kill(os.getpid(), signal.SIGTERM)


def aesEncrypt(content, key, iv="", encode="BASE64", decode=None):
    """
    AES 加密
    :param content: 待加密文本
    :param key: AES key
    :param iv: AES iv(CBC模式才需要)
    :param encode: HEX/BASE64
    :param decode: key/iv 解码方式 None代表 .encode() "HEX" a2b_hex "BASE64"
    :return:
    """
    if decode == "HEX":
        key = a2b_hex(key)
        if iv:
            iv = a2b_hex(iv)
    elif decode == "BASE64":
        key = base64.b64decode(key)
        if iv:
            iv = base64.b64decode(iv)
    else:
        key = key.encode()
        if iv:
            iv = iv.encode()
    mode = "CBC" if iv else "ECB"
    if mode == "ECB":
        aes = AES.new(key, AES.MODE_ECB)
    else:
        aes = AES.new(key, AES.MODE_CBC, iv)
    encrypt_bytes = aes.encrypt(pad(content.encode(), AES.block_size))
    if encode == "BASE64":
        result = base64.b64encode(encrypt_bytes)
    else:
        result = b2a_hex(encrypt_bytes)
    return result.decode()


if __name__ == '__main__':
    pass
