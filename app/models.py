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

# Key-Value Store (例: Redis) を利用する場合
try:
    import redis
    kv_store = redis.Redis(host='localhost', port=6379, db=0)
except ImportError:
    kv_store = None  # Redis がインストールされていない場合は無効化

def save_customer_to_kv_store(customer):
    """ 顧客情報を Key-Value Store に保存 """
    if kv_store:
        kv_store.set(f'customer:{customer.id}', f'{customer.name},{customer.email},{customer.phone},{customer.company}')

def get_customer_from_kv_store(customer_id):
    """ Key-Value Store から顧客情報を取得 """
    if kv_store:
        data = kv_store.get(f'customer:{customer_id}')
        if data:
            return data.decode('utf-8').split(',')
    return None
