from app import db

class Customer(db.Model):
    """顧客情報を管理するテーブル"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False)
    company = db.Column(db.String(100), nullable=True)

    # 顧客と商品の関連（多対多）
    products = db.relationship('CustomerProduct', backref='customer', lazy=True)

class Product(db.Model):
    """商品情報を管理するテーブル"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    discount_limit = db.Column(db.Float, nullable=True, default=0)  # デフォルトを設定

    # 商品と顧客の関連（多対多）
    customers = db.relationship('CustomerProduct', backref='product', lazy=True)

class CustomerProduct(db.Model):
    """顧客と商品を結びつける中間テーブル"""
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    desired_price = db.Column(db.Float, nullable=False)

    # ユニーク制約（1人の顧客が同じ商品を複数回登録しないように）
    __table_args__ = (db.UniqueConstraint('customer_id', 'product_id', name='_customer_product_uc'),)
