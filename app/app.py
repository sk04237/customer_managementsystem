from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Customer
import os

main = Blueprint('main', __name__)

data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')
file_path = os.path.join(data_folder, 'customers.txt')


def export_to_text_file():
    """データベースの顧客情報をテキストファイルに書き出します。"""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("# 名前,メールアドレス,電話番号\n")
            customers = Customer.query.all()
            for customer in customers:
                file.write(f"{customer.name},{customer.email},{customer.phone}\n")
    except Exception as e:
        print(f"テキストファイルのエクスポート中にエラーが発生しました: {e}")


@main.route('/')
def menu():
    return render_template('menu.html')


@main.route('/customers', methods=['GET'])
def view_customers():
    customers = Customer.query.all()
    return render_template('view_customers.html', customers=customers)


@main.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        new_customer = Customer(name=name, email=email, phone=phone)
        db.session.add(new_customer)
        db.session.commit()
        export_to_text_file()  # データベース更新後にテキストファイルを更新
        return redirect(url_for('main.view_customers'))
    return render_template('add_customer.html')


@main.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    customer = Customer.query.get(id)
    if request.method == 'POST':
        customer.name = request.form['name']
        customer.email = request.form['email']
        customer.phone = request.form['phone']
        db.session.commit()
        export_to_text_file()  # データベース更新後にテキストファイルを更新
        return redirect(url_for('main.view_customers'))
    return render_template('edit_customer.html', customer=customer)


@main.route('/customers/import', methods=['POST'])
def import_customers():
    """テキストファイルから顧客情報をインポートします。"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue  # コメント行や空行をスキップ
                name, email, phone = line.split(',')
                if not Customer.query.filter_by(email=email).first():  # 重複を避ける
                    new_customer = Customer(name=name.strip(), email=email.strip(), phone=phone.strip())
                    db.session.add(new_customer)
            db.session.commit()
            flash('顧客情報をインポートしました！', 'success')
    except Exception as e:
        flash(f'インポート中にエラーが発生しました: {str(e)}', 'danger')
    return redirect(url_for('main.view_customers'))


@main.route('/customers/export', methods=['POST'])
def export_customers():
    """テキストファイルに顧客情報をエクスポートします。"""
    try:
        export_to_text_file()
        flash('顧客情報をテキストファイルにエクスポートしました！', 'success')
    except Exception as e:
        flash(f'エクスポート中にエラーが発生しました: {str(e)}', 'danger')
    return redirect(url_for('main.view_customers'))
