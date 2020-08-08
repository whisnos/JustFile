# coding: utf-8
# Author: www.debug5.com
from pyquery import PyQuery as pq
from tornado import ioloop, gen, httpclient, queues
from urllib.parse import urljoin

base_url = "http://www.baidu.com/"
concurrency = 3


async def get_url_links(url):
    # 这个函数功能是爬取链接里面所有的a标签链接
    print(8)
    response = await httpclient.AsyncHTTPClient().fetch(url)
    print(8)
    html = response.body.decode("utf-8")
    p = pq(html)
    links = []
    for tag_a in p("a").items():
        links.append(urljoin(base_url, tag_a.attr("href")))
    return links


async def main():
    # 采用集合 因为连接需要进行去重
    seen_set = set()
    # 采用的是tornado的队列，这个队列是非阻塞的队列(如果这个队列已满或为空，那会切换到其他协程)；而不是python自带的队列（当我们队列已满，再往里面push的话，是会阻塞的，当为空了，在get也是会阻塞的），
    q = queues.Queue()
    print(1)
    async def fetch_url(current_url):
        # 从这个链接没有抓取过的去挖掘出所有链接放到队列 可以 理解为 生产者
        print(4)
        if current_url in seen_set:
            return

        print(f"获取：{current_url}")
        seen_set.add(current_url)

        next_urls = await get_url_links(current_url)
        print(6)
        for next_url in next_urls:
            if next_url.startswith(base_url):
                # 注意 这个非阻塞的队列 并不是说把链接放入队列进行异步化，只是在满了或空了，进行切换到其他协程
                await q.put(next_url)
        print(7)

    async def worker():
        print(3)
        # 取数据
        # while 1:
        #     await q.get()
        # async for 的原理同上
        async for url in q:
            # async for 这边是不会退出的，所以 需要下面这句 进行return退出
            if url is None:
                return
            print(5,url)
            try:
                await fetch_url(url)
            except Exception as e:
                print(f"exception:{e}")
            finally:
                print("X")
                # 计数器，每put进入一个就加1，所以我们调用完了之后，要减去1
                q.task_done()

    print(2)
    # 放入初始url到队列进行开始爬取
    await q.put(base_url)

    # gen.multi 可以将我们多个协程对象 扔到事件循环里面，将启动协程，同时开启三个消费者
    workers = gen.multi([worker() for _ in range(concurrency)])

    # 会阻塞，直到队列里面没有数据为止
    await q.join()
    print("join")
    for _ in range(concurrency):
        # 放入相应的None数量 以至协程退出
        await q.put(None)
    print("None...")

    # 等待所有协程执行完毕 
    await workers
    print("over")


if __name__ == "__main__":
    ioloop.IOLoop.current().run_sync(main)
