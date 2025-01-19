import os
import sys  # アプリケーション終了に必要
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Customer

main = Blueprint('main', __name__)

def export_customers_to_file():
    """データベースの顧客情報をcustomers.txtに書き出す"""
    file_path = os.path.join(os.path.dirname(__file__), '../customers.txt')
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("# 顧客情報フォーマット\n")
            file.write("# 名前,メールアドレス,電話番号\n")
            customers = Customer.query.all()
            for customer in customers:
                file.write(f"{customer.name},{customer.email},{customer.phone}\n")
    except Exception as e:
        print(f"エクスポート中にエラーが発生しました: {e}")

# メニュー画面
@main.route('/')
def home():
    return render_template('menu.html')

# 顧客一覧を表示するエンドポイント
@main.route('/customers', methods=['GET'])
def view_customers():
    customers = Customer.query.all()
    return render_template('view_customers.html', customers=customers)

# 顧客情報を追加するエンドポイント
@main.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        if not name or not email or not phone:
            flash('すべての項目を入力してください。', 'danger')
            return redirect(url_for('main.add_customer'))

        existing_customer = Customer.query.filter_by(email=email).first()
        if existing_customer:
            flash('同じメールアドレスの顧客がすでに存在します。', 'danger')
            return redirect(url_for('main.add_customer'))

        new_customer = Customer(name=name, email=email, phone=phone)
        db.session.add(new_customer)
        db.session.commit()
        export_customers_to_file()
        flash('顧客情報を追加しました。', 'success')
        return redirect(url_for('main.view_customers'))

    return render_template('add_customer.html')

# 顧客情報を編集するエンドポイント
@main.route('/customers/edit/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if request.method == 'POST':
        customer.name = request.form.get('name')
        customer.email = request.form.get('email')
        customer.phone = request.form.get('phone')

        if not customer.name or not customer.email or not customer.phone:
            flash('すべての項目を入力してください。', 'danger')
            return redirect(url_for('main.edit_customer', customer_id=customer.id))

        db.session.commit()
        export_customers_to_file()
        flash('顧客情報を更新しました。', 'success')
        return redirect(url_for('main.view_customers'))

    return render_template('edit_customer.html', customer=customer)

# 顧客情報を削除するエンドポイント
@main.route('/customers/delete/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    export_customers_to_file()
    flash('顧客情報を削除しました。', 'success')
    return redirect(url_for('main.view_customers'))

# 顧客情報をインポートするエンドポイント
@main.route('/customers/import', methods=['GET', 'POST'])
def import_customers():
    if request.method == 'POST':
        file_path = os.path.join(os.path.dirname(__file__), '../customers.txt')
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if line.startswith('#') or not line.strip():
                        continue
                    try:
                        name, email, phone = line.strip().split(',')
                        if not Customer.query.filter_by(email=email).first():
                            new_customer = Customer(name=name.strip(), email=email.strip(), phone=phone.strip())
                            db.session.add(new_customer)
                    except ValueError:
                        flash(f'無効なフォーマット: {line.strip()}', 'danger')
            db.session.commit()
            flash('顧客情報をインポートしました。', 'success')
        except Exception as e:
            flash(f'インポート中にエラーが発生しました: {e}', 'danger')
        return redirect(url_for('main.view_customers'))
    return render_template('import_customers.html')

# アプリケーション終了エンドポイント
@main.route('/shutdown', methods=['POST'])
def shutdown():
    """アプリケーションを終了するエンドポイント"""
    try:
        shutdown_func = request.environ.get('werkzeug.server.shutdown')
        if shutdown_func is None:
            raise RuntimeError('終了機能がサポートされていません。')
        shutdown_func()
    except RuntimeError:
        # サポートされていない場合でも安全に終了する
        os._exit(0)
    return "アプリケーションを終了しました。"
