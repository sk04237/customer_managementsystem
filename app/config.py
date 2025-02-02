import os

class Config:
    """Flask アプリケーションの設定"""
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # `app/` の絶対パスを取得
    INSTANCE_DIR = os.path.join(BASE_DIR, '../instance')  # `instance/` フォルダのパス

    # `instance/` フォルダが存在しない場合、作成する
    if not os.path.exists(INSTANCE_DIR):
        os.makedirs(INSTANCE_DIR)

    # SQLite データベースの URI を指定
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(INSTANCE_DIR, 'customers.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # セキュリティキー
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
