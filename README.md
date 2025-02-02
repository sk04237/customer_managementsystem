# 顧客・商品管理システム

## 概要
このシステムは、顧客と商品を管理し、取引先の希望価格や割引限度額を管理するためのWebアプリケーションです。

### 主な機能
- 顧客情報の管理（追加、編集、削除、一覧表示、検索）
- 商品情報の管理（追加、編集、削除、一覧表示）
- 顧客と商品の関連付け（希望価格の登録）
- `customers.txt` および `goods.txt` のデータ入出力
- 上司のみがアクセス可能な割引限度額設定ページ（パスワード認証）
- REST API によるデータ取得

## 動作環境
| 項目        | 詳細 |
|------------|--------------------------------|
| OS         | Windows / macOS / Linux |
| Python     | 3.8 以上 |
| フレームワーク | Flask |
| データベース | SQLite |
| 依存ライブラリ | Flask, Flask-SQLAlchemy, Redis（任意） |

## セットアップ手順
### 仮想環境の作成（推奨）
```sh
python -m venv venv
source venv/bin/activate  # macOS / Linux
venv\Scripts\activate     # Windows
```

### 必要なパッケージのインストール
```sh
pip install -r requirements.txt
```

### データベースの作成
```sh
python app.py
```

### アプリケーションの起動
```sh
python app.py
```

### Webブラウザでのアクセス
```
http://127.0.0.1:5000
```

## 使用方法
### メインメニュー
| メニュー | 説明 |
|---------|----------------------------------|
| 顧客管理 | 顧客の追加、編集、削除、一覧表示、検索 |
| 商品管理 | 商品の追加、編集、削除、一覧表示 |
| 割引限度額設定 | 上司のみがアクセスできるページ（パスワード認証） |

### 顧客管理
| URL | 機能 |
|-----|------|
| `/customers` | 顧客一覧を表示 |
| `/customers/add` | 顧客を追加 |
| `/customers/edit/<id>` | 顧客情報を編集 |
| `/customers/delete/<id>` | 顧客を削除 |
| `/customers/import` | `customers.txt` からデータをインポート |

#### `customers.txt` のフォーマット
```
# 名前,メール,電話番号,会社
山田 太郎,yamada@example.com,08012345678,株式会社A
鈴木 一郎,suzuki@example.com,09087654321,株式会社B
```

### 商品管理
| URL | 機能 |
|-----|------|
| `/products` | 商品一覧を表示 |
| `/products/add` | 商品を追加 |
| `/products/edit/<id>` | 商品情報を編集 |
| `/products/delete/<id>` | 商品を削除 |
| `/products/import` | `goods.txt` からデータをインポート |

#### `goods.txt` のフォーマット
```
# 商品名,価格,割引限度額
ノートPC,120000,10000
スマートフォン,80000,5000
```

### 顧客と商品の関連付け
| URL | 機能 |
|-----|------|
| `/customer_product_link` | 顧客と商品を紐づけ、希望価格を登録 |

### 割引限度額設定（上司のみ）
| URL | 機能 |
|-----|------|
| `/discount_settings` | パスワード認証で管理ページへ |
| `/set_discount` | 商品ごとの割引限度額を設定 |

#### パスワード（デフォルト設定）
```
supervisor2024
```

## REST API
### 顧客一覧
```http
GET /api/customers
```
#### レスポンス例
```json
[
    {"id": 1, "name": "山田 太郎", "email": "yamada@example.com", "phone": "08012345678", "company": "株式会社A"},
    {"id": 2, "name": "鈴木 一郎", "email": "suzuki@example.com", "phone": "09087654321", "company": "株式会社B"}
]
```

### 商品一覧
```http
GET /api/products
```
#### レスポンス例
```json
[
    {"id": 1, "name": "ノートPC", "price": 120000, "discount_limit": 10000},
    {"id": 2, "name": "スマートフォン", "price": 80000, "discount_limit": 5000}
]
```

### 顧客の希望価格リスト
```http
GET /api/customer_requests
```
#### レスポンス例
```json
[
    {"customer": "山田 太郎", "product": "ノートPC", "desired_price": 110000},
    {"customer": "鈴木 一郎", "product": "スマートフォン", "desired_price": 75000}
]
```

## 注意点
- 割引限度額の設定は上司のみ可能（パスワード認証あり）
- データのインポートは `.txt` ファイルを UTF-8 で保存すること
- サーバーを外部公開する場合は `SECRET_KEY` を変更すること

## コード構成
```
/
│── app.py              # メインアプリケーション
│── models.py           # データベースモデル
│── templates/          # HTMLテンプレート
│── static/             # CSS・JSファイル
│── customers.txt       # 顧客データ
│── goods.txt           # 商品データ
│── requirements.txt    # 必要ライブラリ一覧
│── README.md           # このファイル
```


