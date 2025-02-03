# 顧客管理システム（Customer Management System）

このプロジェクトは、顧客情報と取扱商品を管理し、顧客と商品の関連付け、割引限度額の設定を可能にするシステムです。

---

## **機能概要**
- **顧客管理**
  - `customers.txt` から顧客情報をインポート
  - 顧客一覧の表示
  - 新規顧客の登録
- **商品管理**
  - `goods.txt` から商品情報をインポート
  - 商品一覧の表示
  - 新規商品の登録
- **顧客と商品の関連付け**
  - 顧客が希望価格を入力し、商品との関連付けを行う
  - 既存の関連付けを防止
- **割引限度額の設定（管理者のみ）**
  - 管理者パスワードによる認証
  - 各商品の割引限度額を設定

---

## **動作環境**
- Python 3.9 以上
- Flask
- SQLite3
- Jinja2

---

## **セットアップ手順**

### **1. 仮想環境を作成**
```sh
python3 -m venv venv
```

### **2. 仮想環境を有効化**
Windows:
```sh
venv\Scripts\activate
```
Mac/Linux:
```sh
source venv/bin/activate
```

### **3. 必要なパッケージをインストール**
```sh
pip install -r requirements.txt
```

### **4. データベースの作成**
```sh
python run.py
```

---

## **実行方法**
仮想環境を有効化した状態で以下のコマンドを実行
```sh
python run.py
```
アプリが起動し、ブラウザで `http://127.0.0.1:5000/` にアクセスすることで利用できます。

---

## **使用方法**
### **1. 顧客管理**
| URL | 機能 |
| --- | --- |
| `/customers` | 顧客一覧の表示 |
| `/customers/import` | `customers.txt` から顧客情報をインポート |
| `/customers/add` | 新規顧客の登録 |

### **2. 商品管理**
| URL | 機能 |
| --- | --- |
| `/products` | 商品一覧の表示 |
| `/products/import` | `goods.txt` から商品情報をインポート |
| `/products/add` | 新規商品の登録 |

### **3. 顧客と商品の関連付け**
| URL | 機能 |
| --- | --- |
| `/customer_product_link` | 顧客と商品の関連付け（希望価格を設定） |

### **4. 割引限度額の設定（管理者専用）**
| URL | 機能 |
| --- | --- |
| `/discount_settings` | 管理者パスワードを入力し、設定ページに移動 |
| `/set_discount` | 各商品の割引限度額を設定 |

---

## **データフォーマット**
### **1. `customers.txt`（顧客情報）**
```txt
名前,メールアドレス,電話番号,会社名（任意）
田中太郎,tanaka@example.com,09012345678,ABC商事
山田花子,yamada@example.com,08098765432,
```
**注意:** 会社名がない場合はカンマの後を空白にする。

### **2. `goods.txt`（商品情報）**
```txt
商品名,価格,割引限度額
ノートPC,100000,5000
スマートフォン,80000,3000
```
**注意:** 割引限度額が不要な場合は `0` を入力。

---

## **管理者パスワード**
限度額設定機能を利用するためには、管理者パスワードを入力する必要があります。
デフォルトの管理者パスワードは以下の通りです。

```
supervisor2024
```

パスワードを変更したい場合は `routes.py` の以下の部分を編集してください。

```python
ADMIN_PASSWORD = "変更したいパスワード"
```

---

## **ファイル構成**
```
/customer_managementsystem/
│── run.py              # アプリケーションのエントリーポイント
│── requirements.txt    # 必要ライブラリ一覧
│── README.md           # 説明書
│── customers.txt       # 顧客データファイル
│── goods.txt           # 商品データファイル
│
├── app/                # アプリケーション本体
│   │── __init__.py     # Flaskアプリの初期化
│   │── models.py       # データベースモデル
│   │── routes.py       # ルーティング設定
│   │── config.py       # 設定ファイル
│   │── templates/      # HTMLテンプレート
│   │── static/         # 静的ファイル（CSS, JavaScript）
│
├── venv/               # 仮想環境（Pythonの依存関係を管理）
│
└── instance/           # SQLiteデータベースファイル
```

---

## **トラブルシューティング**
### **1. `ModuleNotFoundError` が発生する**
```sh
pip install -r requirements.txt
```

### **2. `sqlite3.OperationalError: unable to open database file`**
```sh
mkdir instance
python run.py
```

### **3. `Not Found` エラーが発生する**
```python
from app import create_app
app = create_app()
print(app.url_map)
```

---
