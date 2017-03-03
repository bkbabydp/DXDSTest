# -*- coding: UTF-8 -*-


from flask import Blueprint

from lib.inflector import Inflector


class BaseController:
    def __init__(self, scope, element_name):
        """

        :param app:
        :type app: Flask
        :param element_name:
        :type element_name: str
        """
        inflector = Inflector()
        self._element_name = inflector.tableize(element_name)

        self.blueprint = Blueprint(
            name=self._element_name,
            import_name=__name__,
            url_prefix='/%s/%s' % (scope, self._element_name)
        )

        self.routes = [
            ['/', ['GET'], self.index],  # 列所有元素
            ['/', ['POST'], self.create],  # 新建一个元素
            ['/new', ['GET'], self.new],  # 表单页面-用于新建一个元素
            ['/<id_>/edit', ['GET'], self.edit],  # 表单页面-用于编辑某个元素
            ['/<id_>', ['GET'], self.show],  # 展示某个元素
            ['/<id_>', ['PATCH', 'PUT'], self.update],  # 更新某个元素
            ['/<id_>', ['DELETE'], self.destroy]  # 删除某个元素
        ]

        self._init_app(self.blueprint)

    def _init_app(self, app):
        for r, m, v in self.routes:
            app.add_url_rule(rule=r, endpoint=None, view_func=v, methods=m)

    @property
    def element_names(self):
        return self._element_name

    def index(self):
        pass

    def create(self):
        pass

    def new(self):
        pass

    def edit(self, id_):
        pass

    def show(self, id_):
        pass

    def update(self, id_):
        pass

    def destroy(self, id_):
        pass
