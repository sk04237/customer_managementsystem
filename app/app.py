import os
import locale
import redis
import shutil
import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from .models import db, Customer

# Blueprint を定義
main = Blueprint('main', __name__)
api = Blueprint('api', __name__)

# Redis による Key-Value Store を利用
try:
    kv_store = redis.Redis(host='localhost', port=6379, db=0)
except Exception:
    kv_store = None  # Redis が利用できない場合は無効化

def save_customer_to_kv_store(customer):
    """ 顧客情報を Key-Value Store (Redis) に保存 """
    if kv_store:
        kv_store.set(f'customer:{customer.id}', f'{customer.name},{customer.email},{customer.phone},{customer.company or ""}')

def get_customer_from_kv_store(customer_id):
    """ Key-Value Store から顧客情報を取得 """
    if kv_store:
        data = kv_store.get(f'customer:{customer_id}')
        if data:
            return data.decode('utf-8').split(',')
    return None

def export_customers_to_file():
    """データベースの顧客情報を customers.txt に書き出す"""
    file_path = os.path.join(os.path.dirname(__file__), '../customers.txt')
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("# 顧客情報フォーマット\n")
            file.write("# 名前,メールアドレス,電話番号,会社名\n")
            customers = Customer.query.all()
            for customer in customers:
                file.write(f"{customer.name},{customer.email},{customer.phone},{customer.company or ''}\n")
    except Exception as e:
        print(f"エクスポート中にエラーが発生しました: {e}")

# メニュー画面
@main.route('/')
def home():
    return render_template('menu.html')

# 顧客一覧を表示するエンドポイント
@main.route('/customers', methods=['GET'])
def view_customers():
    sort_by = request.args.get('sort_by', 'id')  
    sort_order = request.args.get('sort_order', 'asc')

    if sort_by == 'name':
        customers = Customer.query.all()
        locale.setlocale(locale.LC_COLLATE, 'ja_JP.UTF-8')

        customers.sort(key=lambda c: locale.strxfrm(c.name), reverse=(sort_order == 'desc'))
    else:
        if sort_order == 'asc':
            customers = Customer.query.order_by(getattr(Customer, sort_by).asc()).all()
        else:
            customers = Customer.query.order_by(getattr(Customer, sort_by).desc()).all()

    return render_template('view_customers.html', customers=customers, sort_by=sort_by, sort_order=sort_order)

# 顧客情報を追加するエンドポイント
@main.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        company = request.form.get('company')

        if not name or not email or not phone:
            flash('すべての項目を入力してください。', 'danger')
            return redirect(url_for('main.add_customer'))

        new_customer = Customer(name=name, email=email, phone=phone, company=company)
        db.session.add(new_customer)
        db.session.commit()
        save_customer_to_kv_store(new_customer)
        export_customers_to_file()
        flash('顧客情報を追加しました。', 'success')
        return redirect(url_for('main.view_customers'))

    return render_template('add_customer.html')

# REST API: 顧客情報を取得
@api.route('/api/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{
        "id": customer.id,
        "name": customer.name,
        "email": customer.email,
        "phone": customer.phone,
        "company": customer.company
    } for customer in customers])

@api.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        return jsonify({
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
            "company": customer.company
        })
    return jsonify({"error": "Customer not found"}), 404

@api.route('/api/customers/add', methods=['POST'])
def add_customer_api():
    data = request.json
    if not data or not all(k in data for k in ("name", "email", "phone")):
        return jsonify({"error": "Invalid data"}), 400

    new_customer = Customer(
        name=data["name"],
        email=data["email"],
        phone=data["phone"],
        company=data.get("company")
    )

    db.session.add(new_customer)
    db.session.commit()
    save_customer_to_kv_store(new_customer)

    return jsonify({"message": "Customer added successfully"}), 201

@api.route('/api/customers/edit/<int:customer_id>', methods=['PUT'])
def edit_customer_api(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    data = request.json
    customer.name = data.get("name", customer.name)
    customer.email = data.get("email", customer.email)
    customer.phone = data.get("phone", customer.phone)
    customer.company = data.get("company", customer.company)

    db.session.commit()
    save_customer_to_kv_store(customer)

    return jsonify({"message": "Customer updated successfully"}), 200

@api.route('/api/customers/delete/<int:customer_id>', methods=['DELETE'])
def delete_customer_api(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": "Customer deleted successfully"}), 200

# データベースのバックアップ
def backup_database():
    backup_dir = 'db_backups'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f'backup_{timestamp}.db')

    shutil.copy('customers.db', backup_path)
    print(f"Database backup saved to {backup_path}")

def restore_database(backup_file):
    if os.path.exists(backup_file):
        shutil.copy(backup_file, 'customers.db')
        print(f"Database restored from {backup_file}")
    else:
        print("Backup file not found.")
