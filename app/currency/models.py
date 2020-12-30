from app import db


class Currency(db.Model):
    __tablename__ = "currency"
    __table_args__ = {'useexisting': True}

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, index=True)
    money_sign = db.Column(db.String, index=True, unique=True)

    def __init__(self, name: str, money_sign: str):
        self.name = name
        self.money_sign = money_sign

    def __repr__(self):
        return '{}'.format(self.money_sign)

    @classmethod
    def get_by_id(cls, pk: int):
        return Currency.query.filter_by(id=pk)
