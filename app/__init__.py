from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# データベース管理用のSQLAlchemyインスタンスを作成

db = SQLAlchemy()

def create_app():
    # Flaskアプリケーションのインスタンスを作成
    app = Flask(__name__)

    # アプリの構成
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your_secret_key'

    # データベース初期化
    db.init_app(app)

    with app.app_context():
        from .app import main
        app.register_blueprint(main)
        db.create_all()

    return app
