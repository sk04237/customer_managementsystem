from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from models import db, Customer  # インポートを修正
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db.init_app(app)

main = Blueprint('main', __name__)

# メニュー画面
@main.route('/')
def home():
    return render_template('menu.html')  # メニュー画面

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

        # 未入力チェック
        if not name or not email or not phone:
            flash('すべての項目を入力してください。', 'danger')
            return redirect(url_for('main.add_customer'))

        # 重複チェック
        existing_customer = Customer.query.filter_by(email=email).first()
        if existing_customer:
            flash('同じメールアドレスの顧客がすでに存在します。', 'danger')
            return redirect(url_for('main.add_customer'))

        # 新しい顧客をデータベースに追加
        new_customer = Customer(name=name, email=email, phone=phone)
        db.session.add(new_customer)
        db.session.commit()
        flash('顧客情報を追加しました。', 'success')
        return redirect(url_for('main.view_customers'))

    return render_template('add_customer.html')

# 顧客情報をインポートするエンドポイント
@main.route('/customers/import', methods=['GET', 'POST'])
def import_customers():
    if request.method == 'POST':
        file_path = os.path.join(os.path.dirname(__file__), 'customers.txt')
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if line.startswith('#') or not line.strip():
                        continue
                    name, email, phone = line.strip().split(',')
                    if not Customer.query.filter_by(email=email).first():
                        new_customer = Customer(name=name.strip(), email=email.strip(), phone=phone.strip())
                        db.session.add(new_customer)
            db.session.commit()
            flash('顧客情報をインポートしました。', 'success')
        except Exception as e:
            flash(f'インポート中にエラーが発生しました: {e}', 'danger')
        return redirect(url_for('main.view_customers'))
    return render_template('import_customers.html')

app.register_blueprint(main)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
