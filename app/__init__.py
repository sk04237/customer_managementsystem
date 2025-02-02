from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

# SQLAlchemy のインスタンスを作成
db = SQLAlchemy()

def create_app():
    """Flask アプリケーションを作成し、設定・データベースを初期化する"""
    app = Flask(__name__)
    
    # 設定を適用
    app.config.from_object(Config)

    # データベースの初期化
    db.init_app(app)

    # Blueprint の登録
    from app.routes import main
    app.register_blueprint(main)

    # データベースを作成（エラーハンドリング付き）
    with app.app_context():
        try:
            db.create_all()
            print("Database initialized successfully.")
        except Exception as e:
            print(f"Database initialization failed: {e}")

    return app
