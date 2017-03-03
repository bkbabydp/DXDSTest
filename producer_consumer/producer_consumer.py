#! venv/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
import time
import random
import binascii
import requests

import multiprocessing as mp
from multiprocessing.managers import BaseManager


class QueueClient:
    def __init__(self, ip='127.0.0.1', port=3000, authkey='lzw520'):
        self.queue = None
        self._ip = ip
        self._port = port
        self._authkey = authkey
        self.manager = None

    def connect(self):
        BaseManager.register('get_product_queue')

        self.manager = BaseManager(address=(self._ip, self._port), authkey=self._authkey.encode(encoding='utf-8'))

        while True:
            try:
                print('正在连接产品队列服务器：%s' % self._ip)
                self.manager.connect()
                break
            except ConnectionError:
                print('产品队列服务器连接失败，请等待5秒尝试重新连接')
                time.sleep(5)

        self.queue = self.manager.get_product_queue()


class Producer(mp.Process):
    """生产者线程"""

    def __init__(self, queue, *args, **kwargs):
        super(Producer, self).__init__(*args, **kwargs)
        self.queue = queue  # type: mp.Queue

    def run(self):
        while True:
            try:
                rnd_id = random.randint(1, 1000)
                rnd_name = binascii.hexlify(os.urandom(8)).decode()
                product = dict(id=rnd_id, name=rnd_name)
                self.queue.put(product)
                print('[%s:%d] 生产一个产品 [%s]，当前产品队列共计 %d 个' % (
                    mp.current_process().name,
                    os.getpid(),
                    str(product),
                    self.queue.qsize()
                ))
                time.sleep(random.randint(1, 10))
            except EOFError:
                print('[错误]产品队列服务器已关闭')
                print('[%s:%d] 子进程关闭' % (
                    mp.current_process().name,
                    os.getpid()
                ))
                break
            except KeyboardInterrupt:
                print('[错误]用户指令->退出')
                print('[%s:%d] 子进程关闭' % (
                    mp.current_process().name,
                    os.getpid()
                ))
                break


class Consumer(mp.Process):
    """消费者线程"""

    def __init__(self, queue, api_server_domain, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        self.queue = queue  # type: mp.Queue
        self._api_server_domain = api_server_domain

    def run(self):
        while True:
            try:
                if not self.queue.empty():
                    product = self.queue.get()
                    url = '%s/v1/products/' % self._api_server_domain
                    json = requests.post(
                        url=url,
                        data=dict(name=product['name'])
                    ).json()
                    print('[%s:%d] 消费一个产品：\n%s\n访问API后返回数据：\n%s\n当前产品库存 %d 个\n' % (
                        mp.current_process().name,
                        os.getpid(),
                        str(product),
                        json,
                        self.queue.qsize()
                    ))
                    print()
                    time.sleep(random.randint(1, 3))
            except EOFError:
                print('[错误]产品队列服务器已关闭')
                print('[%s:%d] 子进程关闭' % (
                    mp.current_process().name,
                    os.getpid()
                ))
                break
            except KeyboardInterrupt:
                print('[错误]用户指令->退出')
                print('[%s:%d] 子进程关闭' % (
                    mp.current_process().name,
                    os.getpid()
                ))
                break


if __name__ == '__main__':

    argv = sys.argv

    producer_num = int(argv[1]) if len(argv) > 1 else 0
    consumer_num = int(argv[2]) if len(argv) > 2 else 0
    queue_ip = argv[3] if len(argv) > 3 else '127.0.0.1'
    api_domain = argv[4] if len(argv) > 4 else 'http://127.0.0.1:5000'

    if queue_ip and api_domain:
        print('[生产者-消费者] 模拟程序开始运行：')

        client = QueueClient(ip=queue_ip)
        client.connect()

        processes_pool = []

        for i in range(producer_num):
            processes_pool.append(
                ['Producer-%s' % i, Producer(queue=client.queue, name='Producer-%s' % i)]
            )

        for i in range(consumer_num):
            processes_pool.append(
                ['Consumer-%s' % i, Consumer(queue=client.queue, api_server_domain=api_domain, name='Consumer-%s' % i)]
            )

        for name, p in processes_pool:
            print('%s [start]' % name)
            p.start()

        try:
            for name, p in processes_pool:
                print('%s [join]' % name)
                p.join()
        except KeyboardInterrupt:
            print('[错误]用户指令->退出')
        finally:
            print('主进程已关闭')
