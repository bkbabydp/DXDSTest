#! venv/bin/python3
# -*- coding: UTF-8 -*-

import queue

from multiprocessing.managers import BaseManager


class QueueServer:
    def __init__(self, ip='0.0.0.0', port=3000, authkey='lzw520'):
        self._queue = queue.Queue()
        self._ip = ip
        self._port = port
        self._authkey = authkey
        self.manager = None

    def start(self):
        BaseManager.register('get_product_queue', callable=lambda: self._queue)

        self.manager = BaseManager(address=(self._ip, self._port), authkey=self._authkey.encode(encoding='utf-8'))
        self.manager.start()
        print('产品队列服务器已启动！')

    def shutdown(self):
        if self.manager:
            self.manager.shutdown()
            print('服务器已关闭！')
        else:
            print('关闭失败：服务器未启动！')


if __name__ == '__main__':
    server = QueueServer()
    server.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('\n用户指令-退出\n')
    finally:
        server.shutdown()
