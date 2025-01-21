from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# データベースオブジェクトを作成
db = SQLAlchemy()

def create_app():
    """
    Flaskアプリケーションを作成して初期化する。
    """
    app = Flask(__name__)

    # アプリケーション設定
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'  # SQLiteデータベースのパス
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 不要な通知を無効化
    app.secret_key = 'your_secret_key'  # セッション用のシークレットキー

    # データベースを初期化
    db.init_app(app)

    with app.app_context():
        # Blueprintを登録
        from app.app import main  # 相対インポートを使用してBlueprintをインポート
        app.register_blueprint(main)
        
        # データベースを作成
        db.create_all()

    return app

# エントリーポイント
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)  # デバッグモードでアプリケーションを起動

