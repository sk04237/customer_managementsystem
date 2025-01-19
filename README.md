# 顧客管理システム

このアプリケーションは、Flaskを使用した簡単な顧客管理システムです。顧客情報の一覧表示、追加、編集、削除、インポート機能を提供します。

---

## 必要条件

以下がインストールされている必要があります：

- **Python 3.8以上**
- **pip**（Pythonパッケージ管理ツール）
- **仮想環境を構築するためのvenvモジュール**

---

## セットアップ手順

### 1. **リポジトリを準備**
プロジェクトフォルダに移動し、ファイルが正しく配置されていることを確認してください。

```bash
cd ~/ダウンロード/customer_managementsystem-main
```

プロジェクトの構成例：
```plaintext
customer_managementsystem-main/
├── app/
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── menu.html
│   │   ├── add_customer.html
│   │   ├── edit_customer.html
│   │   ├── import_customers.html
│   │   └── view_customers.html
├── customers.txt
├── run.py
├── requirements.txt
├── README.md
```

---

### 2. **仮想環境を作成**
仮想環境を作成してアクティブ化します。

```bash
python3 -m venv venv
```

#### 仮想環境をアクティブ化:
- **Linux/macOS**:
    ```bash
    source venv/bin/activate
    ```
- **Windows**:
    ```bash
    venv\Scripts\activate
    ```

---

### 3. **依存パッケージをインストール**
`requirements.txt`に記載された依存パッケージをインストールします。

```bash
pip install -r requirements.txt
```

---

### 4. **アプリケーションを起動**
以下のコマンドを実行してアプリケーションを起動します。

```bash
python run.py
```

起動後、次のメッセージが表示されます：
```plaintext
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

---

## 使用方法

### 1. **ブラウザでアクセス**
- Webブラウザを開き、次のURLを入力します：
    ```
    http://127.0.0.1:5000/
    ```

### 2. **主な機能**
- **顧客一覧を見る**: 登録されている顧客情報を表示します。
- **顧客を追加する**: 新しい顧客を登録します。
- **顧客情報を編集する**: 既存の顧客情報を編集します。
- **顧客情報を削除する**: 不要な顧客を削除します。
- **顧客情報をインポートする**: `customers.txt`から一括で顧客情報をインポートします。

### 3. **データの保存**
- アプリケーション内での変更内容は自動的に`customers.txt`に保存されます。

---

## トラブルシューティング

### 1. **アプリケーションが起動しない場合**
- 仮想環境が有効になっていることを確認してください。
- 必要なライブラリがインストールされているか確認：
    ```bash
    pip list
    ```

### 2. **顧客データがインポートされない場合**
- `customers.txt`が正しいフォーマットで記述されていることを確認してください。
- 例：
    ```plaintext
    山田太郎,yamada@example.com,09012345678
    鈴木花子,suzuki@example.com,08098765432
    ```

### 3. **アプリケーション終了時のエラー**
- 開発モードでない場合、終了機能は動作しません。本番環境ではサーバー管理ツールを使用して停止してください。

---


