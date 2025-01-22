from . import db  # 相対インポート

class Customer(db.Model):
    """
    顧客情報を管理するデータベースモデル
    """
    id = db.Column(db.Integer, primary_key=True)  # 顧客ID（プライマリキー）
    name = db.Column(db.String(100), nullable=False)  # 顧客名
    email = db.Column(db.String(100), nullable=False, unique=True)  # メールアドレス（ユニーク制約）
    phone = db.Column(db.String(15), nullable=False)  # 電話番号
    company = db.Column(db.String(100), nullable=True)  # 会社名（オプション）

    def __repr__(self):
        """
        デバッグ時やログに出力される表現
        """
        return f'<Customer {self.name}, Company: {self.company}>'
