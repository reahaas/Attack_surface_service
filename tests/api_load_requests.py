import aiohttp
import asyncio

MAXREQ = 10000
MAXTHREAD = 50

URL = 'http://localhost/v1/attack?vm_id=vm-a211de'  # 'https://google.com'

g_thread_limit = asyncio.Semaphore(MAXTHREAD)


async def worker(session):
    async with session.get(URL) as response:
        response = await response.read()
        print(response)


async def run(worker, *argv):
    async with g_thread_limit:
        await worker(*argv)


async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[run(worker, session) for _ in range(MAXREQ)])


if __name__ == '__main__':
    # Don't use asyncio.run() - it produces a lot of errors on exit.
    asyncio.get_event_loop().run_until_complete(main())

