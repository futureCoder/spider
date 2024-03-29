import asyncio
import aiohttp
import datetime
import itertools
import re
import pandas as pd
import 数据存储 as ds

start = datetime.datetime.now()


class Spider(object):
    # 初始化
    def __init__(self):
        self.semaphore = asyncio.Semaphore(10)
        self.judge = True
        self.headers = {
            'Connection': 'Keep-Alive',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'bj.lianjia.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'

        }

    async def scrape(self, url):
        async with self.semaphore:  # 有信号量的时候
            session = aiohttp.ClientSession(headers=self.headers)
            response = await session.get(url)  # await用于挂起阻塞的异步调用接口
            await asyncio.sleep(1)
            result = await response.text()
            await session.close()
            return result

    async def scrape_index(self, item):
        url = f'https://bj.lianjia.com/ershoufang/{item[0]}/pg{item[1]}/'
        text = await self.scrape(url)
        await self.parse(item, text)
        print('完成  ', item[0], item[1])
        await asyncio.sleep(1)

    async def parse(self, item, text):
        # 正则匹配提取数据
        try:
            datas = ds.getIntoPage(item[0], text)
            datas.to_csv('爬取结果/' + item[0] + '.csv', mode='a+', index=False, header=False, encoding='gb18030')
        except Exception as e:
            print(e)

    def main(self):
        # regions = ['xierqi1', 'qinghe11', 'xibeiwang']
        regions = ['haidian', 'dongcheng', 'xicheng']
        page = [str(i) for i in range(1, 100)]
        items = [d for d in itertools.product(regions, page)]
        # 爬取100页的数据
        scrape_index_tasks = [asyncio.ensure_future(self.scrape_index(item)) for item in items]
        loop = asyncio.get_event_loop()
        tasks = asyncio.gather(*scrape_index_tasks)
        loop.run_until_complete(tasks)


if __name__ == '__main__':
    spider = Spider()
    spider.main()
