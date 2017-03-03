
需求
---
生产、消费者模型实现多进程+分布式demo

该模型可以在多台主机上运行

生产者生产产品放在队列服务器上，消费者去队列服务器获取产品，并调用 RESTful api 对数据库进行操作

安装
---
进入当前目录：

    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirement-py3.txt
    deactivate
    
运行
---
进入当前目录：

启动队列数据服务器：
    
    ./queue_server.py
    
启动分布式服务器：

其中
* `producer_num` - 生产者进程数
* `consumer_num` - 消费者进程数
* `queue_ip` - 队列服务器所在的 IP 地址
* `api_domain` - Flask/Django 服务器所在的 IP地址／域名


    ./producer_consumer.py <producer_num> <consumer_num> <queue_ip> <api_domain>
    

