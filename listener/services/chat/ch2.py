import asyncio


async def f1(a):
    """Предположим есть async-функция f1()"""
    print("set", a)
    return a + 1


async def f2(a):
    """если мы возьмем и вызовем эту функцию в функции f2() Без await"""
    print("get", a)
    b = f1(a + 1)
    print("res", b)
    return b


loop = asyncio.get_event_loop()
b = loop.run_until_complete(f2(a=1))
b = loop.run_until_complete(b)
print(b)

# get 1
# res <coroutine object set_ at 0x02FB4F90>
# set 2
# 3
