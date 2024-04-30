import asyncio
import random

async def coroutine_one(prefix:str):
    amount = 0.0
    for index in range(10):
        delay = random.uniform(1.1,5.4)
        await asyncio.sleep(delay)
        print(prefix + '-' + str(index) +'-' + str(delay))
        amount = amount + delay
    return amount

async def main():
    async with asyncio.TaskGroup() as tg:
        """
        The await is implicit when the context manager exits.
        """
        task1 = tg.create_task(coroutine_one('first'))
        task2 = tg.create_task(coroutine_one('second'))
        task3 = tg.create_task(coroutine_one('third'))
    print(f"Both tasks have completed now: {task1.result()}, {task2.result()}, {task3.result()}")

asyncio.run(main())