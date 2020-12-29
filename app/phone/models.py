from app import db


class Phone(db.Model):
    __tablename__ = "Phone"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, index=True)
    value = db.Column(db.String, unique=True)
    monthy_price = db.Column(db.Numeric(8, 2))
    setup_price = db.Column(db.Numeric(8, 2))
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
    currency = db.relationship('app.currency.models.Currency', backref='phones', lazy=True)

    def __init__(self, value, monthy_price, setup_price, currency):
        self.value = value
        self.monthy_price = monthy_price
        self.setup_price = setup_price
        self.currency_id = currency

    @classmethod
    def get_by_id(cls, pk: int):
        return Phone.query.filter_by(id=pk).first()
