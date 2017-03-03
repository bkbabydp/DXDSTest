# -*- coding: UTF-8 -*-


from flask import jsonify
from flask import request

import traceback
import time
import datetime

from .base import BaseController
from ..models import Product
from .. import db


class ProductController(BaseController):
    def index(self):
        try:
            month_str = request.args.get('count_by_month', None)
            if month_str:
                # '2017-03'
                try:
                    month_time = time.strptime(month_str, '%Y-%m')
                    month_datetime = datetime.datetime(*month_time[:3])
                except ValueError:
                    raise BaseException('无效的自然月参数，有效格式例如：2017-03')

                ps = Product.get_by_month(month_datetime)
            else:
                ps = Product.query.all()

            return jsonify(
                status=200,
                data=dict(
                    count=len(ps),
                    products=[p.to_json() for p in ps]
                )
            )
        except Exception as err:
            traceback.print_exc()
            return jsonify(
                status=404,
                error=str(err)
            )
        except BaseException as err:
            traceback.print_exc()
            return jsonify(
                status=404,
                error=str(err)
            )

    def show(self, id_):
        try:
            p = Product.query.filter(Product.id_ == id_).first()
            if p:
                return jsonify(
                    status=200,
                    data=dict(
                        count=1,
                        products=[p.to_json()]
                    )
                )
            else:
                return jsonify(
                    status=404,
                    data=dict(count=0, products=[])
                )
        except Exception as err:
            traceback.print_exc()
            return jsonify(
                status=404,
                error=str(err)
            )

    def create(self):
        try:
            name = request.form.get('name', None)
            if name:
                p = Product(name=name)
                db.session.merge(p)
                db.session.commit()

                return jsonify(
                    status=201,
                    data=dict(
                        count=1,
                        products=[p.to_json()]
                    )
                )
            else:
                raise BaseException('参数name不能为空')
        except Exception as err:
            traceback.print_exc()
            return jsonify(
                status=400,
                error=str(err)
            )
        except BaseException as err:
            traceback.print_exc()
            return jsonify(
                status=400,
                error=str(err)
            )

    def update(self, id_):
        try:
            name = request.form.get('name', None)
            if name:
                p = Product.query.filter(Product.id_ == id_).first()  # type: Product
                if p:
                    p.name = name
                    db.session.merge(p)
                    db.session.commit()

                    return jsonify(
                        status=201,
                        data=dict(
                            count=1,
                            products=[p.to_json()]
                        )
                    )
                else:
                    raise BaseException('该数据不存在')
            else:
                raise BaseException('参数name不能为空')
        except Exception as err:
            traceback.print_exc()
            return jsonify(
                status=400,
                error=str(err)
            )
        except BaseException as err:
            traceback.print_exc()
            return jsonify(
                status=400,
                error=str(err)
            )

    def destroy(self, id_):
        try:
            p = Product.query.filter(Product.id_ == id_).first()  # type: Product
            if p:
                db.session.delete(p)
                db.session.commit()

                return jsonify(
                    status=204,
                    data=dict(count=0, products=[])
                )
            else:
                raise BaseException('该数据不存在')
        except Exception as err:
            traceback.print_exc()
            return jsonify(
                status=400,
                error=str(err)
            )
        except BaseException as err:
            traceback.print_exc()
            return jsonify(
                status=400,
                error=str(err)
            )
