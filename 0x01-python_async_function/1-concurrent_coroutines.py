#!/usr/bin/env python3
""" Docstring """
import random
from typing import List
import asyncio

wait_random = __import__("0-basic_async_syntax").wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """ Doc string """
    listDelays = []
    for _ in range(n):
        listDelays.append(asyncio.create_task(wait_random(max_delay)))
    return sorted(await asyncio.gather(*listDelays))
