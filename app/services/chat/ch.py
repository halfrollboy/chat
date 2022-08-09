import asyncio


async def f1(a):
    """Предположим есть async-функция f1()"""
    print("set", a)
    return a + 1


async def f2(a):
    """если мы возьмем и вызовем эту функцию в функции f2() C await"""
    print("get", a)
    b = await f1(a + 1)
    print("res", b)
    return b


loop = asyncio.get_event_loop()
b = loop.run_until_complete(f2(a=1))
print(b)

# get 1
# set 2
# res 3
# 3
