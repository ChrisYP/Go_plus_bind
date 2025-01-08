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


def aesEncrypt(content, key, iv="", encode="BASE64", decode=None):
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
