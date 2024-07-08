#!/usr/bin/env python3
""" Docstring """
import random
import asyncio


async def wait_random(max_delay: int = 10) -> float:
    """ Doc string """
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
