import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app as app
from .models import db, Customer

# Blueprint を定義
main = Blueprint('main', __name__)

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
    sort_by = request.args.get('sort_by', 'id')  # デフォルトでID順
    sort_order = request.args.get('sort_order', 'asc')  # 昇順または降順
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

        existing_customer = Customer.query.filter_by(email=email).first()
        if existing_customer:
            flash('同じメールアドレスの顧客がすでに存在します。', 'danger')
            return redirect(url_for('main.add_customer'))

        new_customer = Customer(name=name, email=email, phone=phone, company=company)
        db.session.add(new_customer)
        db.session.commit()
        export_customers_to_file()
        flash('顧客情報を追加しました。', 'success')
        return redirect(url_for('main.view_customers'))

    return render_template('add_customer.html')

# 検索機能エンドポイント
@main.route('/search_customers', methods=['GET'])
def search_customers():
    query = request.args.get('query')
    if query:
        results = Customer.query.filter(
            (Customer.name.ilike(f'%{query}%')) | 
            (Customer.email.ilike(f'%{query}%')) |
            (Customer.phone.ilike(f'%{query}%')) |
            (Customer.company.ilike(f'%{query}%'))
        ).all()
    else:
        results = []

    return render_template('view_customers.html', customers=results)

# 顧客情報を編集するエンドポイント
@main.route('/customers/edit/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if request.method == 'POST':
        customer.name = request.form.get('name')
        customer.email = request.form.get('email')
        customer.phone = request.form.get('phone')
        customer.company = request.form.get('company')

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
                        name, email, phone, *company = line.strip().split(',')
                        company = company[0] if company else None
                        if not Customer.query.filter_by(email=email).first():
                            new_customer = Customer(name=name.strip(), email=email.strip(), phone=phone.strip(), company=company)
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
    """
    サーバーを終了するエンドポイント。
    運用環境では直接停止するのではなく、メッセージを返すのみ。
    """
    env = app.config.get("ENV", "production")
    
    if env == "production":
        flash('運用環境ではこの操作はサポートされていません。', 'danger')
        return redirect(url_for('main.home'))
    
    try:
        shutdown_func = request.environ.get('werkzeug.server.shutdown')
        if shutdown_func is None:
            raise RuntimeError('終了機能がサポートされていません。')
        shutdown_func()
        flash('アプリケーションを終了しました。', 'success')
    except RuntimeError:
        os._exit(0)  # 強制終了（デバッグモードでのみ使用）
    return "アプリケーションを終了しました。"
