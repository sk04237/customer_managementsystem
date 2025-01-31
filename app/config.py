import os

# Flask アプリの設定
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///customers.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # バックアップ設定
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    BACKUP_DIR = os.path.join(BASE_DIR, 'db_backups')
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    @staticmethod
    def backup_database():
        """ データベースのバックアップを作成 """
        import shutil
        import datetime

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(Config.BACKUP_DIR, f'backup_{timestamp}.db')

        shutil.copy('customers.db', backup_path)
        print(f"Database backup saved to {backup_path}")

    @staticmethod
    def restore_database(backup_file):
        """ 指定されたバックアップファイルからデータベースを復元 """
        if os.path.exists(backup_file):
            shutil.copy(backup_file, 'customers.db')
            print(f"Database restored from {backup_file}")
        else:
            print("Backup file not found.")
