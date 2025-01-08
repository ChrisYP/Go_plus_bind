# -*- coding: utf-8 -*-
# @Time    : 2024/6/23 20:05
# @Author  : Chris
# @Email   : 10512@qq.com
# @File    : task.py
# @Software: PyCharm
import random
import string
import uuid

import time

from loguru import logger
import requests
from src.utils import aesEncrypt

with open("success.txt", "r") as f:
    success_list = f.read().strip().split('\n')


def get_proxy():
    return f"http://channel-ipv6-country_US-r_10m-s_{''.join(random.sample(string.ascii_letters + string.digits, 10))}:password@gate.nstproxy.io:24125"


def set_uuid_aes(u):
    return aesEncrypt(u, "YeHKjudwq8ZVdZ2TZGH39RSzhHVy9ksN", "3MdB7sKkA4Tg3Gpr")


def process(info):
    try:
        address, _, token = info.split("----")
    except BaseException as e:
        logger.error(info)
        return
    if address in success_list:
        logger.info(f"{address} has been bound")
        return
    _uuid = uuid.uuid4()
    __uuid_data = set_uuid_aes(str(_uuid))
    while 1:
        try:
            __proxy = get_proxy()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'sec-ch-ua-platform': '"macOS"',
                'ps-dataurlconfigid': __uuid_data,
                'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'x-project': 'secwarex',
                'x-address': address,
                'manageid': '100004',
                'chain_type': 'EVM',
                'token': token,
                'origin': 'https://app.gopluslabs.io',
                'sec-fetch-site': 'cross-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://app.gopluslabs.io/',
                'accept-language': 'zh-CN,zh;q=0.9',
                'priority': 'u=1, i',
            }

            params = {
                'type': '3',
                'params': 'plugin',
            }

            requests.get('https://api.secwarex.io/api/v1/theme/getNotificationConfig', params=params,
                         headers=headers,
                         proxies={"https": __proxy}, verify=False)

            requests.get('https://api.secwarex.io/api/v1/plugin/active', headers=headers, proxies={"https": __proxy},
                         verify=False)

            # =================================================================================================

            params = {
                'type': '2',
                'params': "",
            }

            requests.get('https://api.secwarex.io/api/v1/theme/getNotificationConfig', params=params,
                         headers=headers,
                         proxies={"https": __proxy}, verify=False)

            # =================================================================================================

            params = {
                'taskId': '425',
                'themeId': '217',
            }

            response = requests.get('https://api.secwarex.io/api/v1/task/plugin/search', params=params, headers=headers,
                                    proxies={"https": __proxy}, verify=False).json()
            logger.info(response)
            if response.get("code") == 0:
                logger.success(f"{address} bind success")
                with open("success.txt", "a") as f1:
                    f1.write(f"{address}\n")
                break
            else:
                logger.error(f'{address} bind failed. {response}')
                continue
        except BaseException:
            time.sleep(1)
            continue


if __name__ == '__main__':
    # 代理注册 https://app.nstproxy.com/register?i=I67hey
    # 注册之后 通道id 替换到get_proxy()函数中的channel 密码替换到get_proxy()函数中的password
    pass
