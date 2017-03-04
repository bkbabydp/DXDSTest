需求
---

1.使用 SQLAlchemy 封装一个模型，需要支持一个流水号字段，按照 年月日+6位顺序流水的方式生成流水号。
创建对象时流水号应按日递增且唯一， 例如 170301000001, 170301000002, 170302000001
对该模型按自然月统计数量
2.使用生产、消费者模型实现任意demo，可自由发挥
3.使用Django及Flask分别实现一个基础的Restful API，数据维护在内存中即可无需数据库。按规范实现 GET/POST/PUT/PATCH/DELETE 方法


安装
---
进入当前目录：

    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirement-py3.txt
    
数据库
---
进入当前目录：

    ./manager.py db init
    ./manager.py db migrate
    ./manager.py db upgrade

运行
---
进入当前目录：

    ./manager.py runserver
    
其他帮助
---

    ./manager.py

测试
---
进入当前目录：

    ./manager.py test
    
用python测试：

    requests.get(url='http://127.0.0.1:5000/products').json()
    requests.get(url='http://127.0.0.1:5000/products/1').json()
    requests.post(url='http://127.0.0.1:5000/products', data=dict(name='你是一个大帅哥')).json()
    requests.put(url='http://127.0.0.1:5000/products/1', data=dict(name='你是一个大帅哥')).json()
    requests.patch(url='http://127.0.0.1:5000/products/1', data=dict(name='你是一个大帅哥')).json()
    requests.delete(url='http://127.0.0.1:5000/products/1', data=dict(name='你是一个大帅哥')).json()
    
    
注意
---
*记得确保`db`目录存在*
