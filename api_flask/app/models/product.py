# -*- coding: UTF-8 -*-


from datetime import datetime, timedelta

from .. import db

from lib.func import zfill


class Product(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    # 产品编号
    product_id = db.Column(db.String, nullable=False, unique=True, index=True)
    # 产品名
    name = db.Column(db.String, nullable=False)
    # 提交时间
    submit_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, name: str):
        self.name = name
        self.product_id = Product.create_product_id()
        self.submit_time = datetime.now()

    def __repr__(self):
        return '<%s %s %s>' % (self.__class__, self.product_id, self.name)

    def to_json(self):
        return dict(
            id=self.id_,
            product_id=self.product_id,
            name=self.name,
            submit_time=self.submit_time
        )

    @staticmethod
    def get_product_id_date_part(date: datetime) -> (str, int, int, int):
        year, month, day = date.year, date.month, date.day
        date_part = '%s%s%s' % (zfill(year, 2), zfill(month, 2), zfill(day, 2))
        return date_part, year, month, day

    @staticmethod
    def create_product_id() -> str:
        date_part, year, month, day = Product.get_product_id_date_part(datetime.now())

        today_wee_hours = datetime(year=year, month=month, day=day)
        tomorrow_wee_hours = today_wee_hours + timedelta(days=1)

        last_p = Product.query.filter(
            Product.submit_time.between(today_wee_hours, tomorrow_wee_hours)
        ).order_by(Product.product_id.desc()).first()  # type: Product

        if last_p:
            num = int(last_p.product_id[6:])
        else:
            num = 0

        num_part = '%s' % zfill(num + 1, 6)

        return '%s%s' % (date_part, num_part)

    @staticmethod
    def get_by_month(date: datetime):
        date_part, _, _, _ = Product.get_product_id_date_part(date)
        return Product.query.filter(
            Product.product_id.like(other='%s%%' % date_part[:4])
        ).all()
