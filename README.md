# アプリケーション実行手順

このガイドでは、Flaskベースの顧客管理システムを実行するための手順を説明します。

---

## **前提条件**
以下がシステムにインストールされていることを確認してください：

1. Python 3.7 以上
2. pip（Python パッケージマネージャ）
3. 仮想環境を構築できるツール（`venv`）
4. SQLite（デフォルトでPythonに組み込まれています）

---

## **実行手順**

### **1. リポジトリをクローン**
プロジェクトを取得するために、以下のコマンドを実行します：
```bash
git clone <リポジトリURL>
cd customer-management-system
```

### **2. 仮想環境を作成**
Python仮想環境をセットアップします。
```bash
python3 -m venv venv
```

### **3. 仮想環境を有効化**
- **Linux/macOS**:
  ```bash
  source venv/bin/activate
  ```
- **Windows**:
  ```bash
  venv\Scripts\activate
  ```

### **4. 必要な依存関係をインストール**
プロジェクトに必要なライブラリをインストールします。
```bash
pip install -r requirements.txt
```

### **5. 環境変数を設定**
`.env` ファイルをプロジェクトディレクトリに作成し、以下の内容を記述します：
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
```

### **6. データベースを初期化**
アプリケーションが初めて実行される際に必要なデータベースを作成します。
```bash
flask shell
```
以下のコマンドをFlaskシェルで実行：
```python
from app import db
from app.models import Customer

db.create_all()
exit()
```

### **7. アプリケーションを起動**
以下のコマンドでアプリケーションを実行します：
```bash
flask run
```

### **8. ブラウザでアクセス**
デフォルトでは以下のURLでアプリケーションを利用できます：
```
http://127.0.0.1:5000/
```

---

## **主なエンドポイント**
| エンドポイント         | メソッド | 説明                       |
|-------------------------|----------|----------------------------|
| `/`                     | GET      | メインメニュー             |
| `/customers`            | GET      | 顧客情報の一覧を表示       |
| `/customers/add`        | GET/POST | 新しい顧客情報を追加       |
| `/customers/edit/<id>`  | GET/POST | 既存の顧客情報を編集       |
| `/customers/import`     | POST     | テキストファイルからインポート |
| `/customers/export`     | POST     | テキストファイルにエクスポート |

---

## **デバッグおよび問題解決**

### **デバッグモードを有効化**
開発中にエラー内容を確認するためにデバッグモードを有効化してください：
```
FLASK_ENV=development
FLASK_DEBUG=1
```

### **よくある問題と解決方法**

1. **`python` コマンドが見つからない**:
   - Python 3 をインストールし、`python3` コマンドを使用してください。

2. **データベースエラー**:
   - `db.create_all()` を実行してテーブルを作成してください。

3. **依存関係がインストールされない**:
   - `pip` のバージョンを確認し、最新バージョンに更新してください。
     ```bash
     pip install --upgrade pip
     ```

---

