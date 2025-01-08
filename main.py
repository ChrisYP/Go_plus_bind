# -*- coding: utf-8 -*-
# @Time    : 2024/1/07 20:06
# @Author  : Chris
# @Email   : 10512@qq.com
# @File    : main.py
# @Software: PyCharm
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable

from loguru import logger
from src.task import process


# logger.add("{time:YYYY-MM-DD}.log", level="DEBUG", rotation='00:00', retention="3 days")


def main(tasks: Iterable, workers):
    start_time = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(process, task) for task in tasks}
        completed_tasks = 0
        total_tasks = len(futures)
        for future in as_completed(futures):
            future.result()
            completed_tasks += 1
            logger.debug(f"完成进度: {completed_tasks}/{total_tasks} ({(completed_tasks / total_tasks) * 100:.2f}%)")

    end_time = time.perf_counter()
    logger.debug(f"总耗时: {end_time - start_time:.2f}秒")


if __name__ == '__main__':
    # 只需要设置 src/utils.py 里的代理设置即可
    with open("login.txt", "r") as f:
        login = f.read().strip().split('\n')
    main([i for i in login], 66)
