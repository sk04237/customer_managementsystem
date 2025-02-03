from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

# SQLAlchemyのインスタンスを作成
db = SQLAlchemy()

def create_app():
    """Flask アプリケーションを作成"""
    app = Flask(__name__)

    # 設定を適用
    app.config.from_object(Config)

    # データベースの初期化
    db.init_app(app)

    # Blueprintの登録
    from app.routes import main
    app.register_blueprint(main)

    # データベースを作成
    with app.app_context():
        db.create_all()

    return app
