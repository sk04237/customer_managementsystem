import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, Customer, Product, CustomerProduct

main = Blueprint('main', __name__)

ADMIN_PASSWORD = "supervisor2024"

# ==========================
# メインメニュー
# ==========================
@main.route('/')
def main_menu():
    return render_template('menu.html')

# ==========================
# 顧客管理メニュー
# ==========================
@main.route('/customers_menu')
def customers_menu():
    return render_template('customers_menu.html')

@main.route('/customers')
def view_customers():
    customers = Customer.query.all()
    return render_template('view_customers.html', customers=customers)

@main.route('/customers/import', methods=['GET', 'POST'])
def import_customers():
    if request.method == 'POST':
        file_path = "customers.txt"
        if not os.path.exists(file_path):
            flash('customers.txt が見つかりません', 'danger')
            return redirect(url_for('main.customers_menu'))

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if line.startswith('#') or not line.strip():
                        continue
                    try:
                        name, email, phone, *company = line.strip().split(',')
                        company = company[0] if company else None
                        if not Customer.query.filter_by(email=email).first():
                            new_customer = Customer(name=name, email=email, phone=phone, company=company)
                            db.session.add(new_customer)
                    except ValueError:
                        flash(f'無効なフォーマット: {line.strip()}', 'danger')

            db.session.commit()
            flash('顧客情報をインポートしました', 'success')
        except Exception as e:
            flash(f'インポートエラー: {e}', 'danger')

    return render_template('import_customers.html')

# ==========================
# 商品管理メニュー
# ==========================
@main.route('/products_menu')
def products_menu():
    return render_template('products_menu.html')

@main.route('/products')
def view_products():
    products = Product.query.all()
    return render_template('view_products.html', products=products)

@main.route('/products/import', methods=['GET', 'POST'])
def import_products():
    if request.method == 'POST':
        file_path = "goods.txt"
        if not os.path.exists(file_path):
            flash('goods.txt が見つかりません', 'danger')
            return redirect(url_for('main.products_menu'))

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if line.startswith('#') or not line.strip():
                        continue
                    try:
                        name, price, discount_limit = line.strip().split(',')
                        price = float(price)
                        discount_limit = float(discount_limit) if discount_limit else 0
                        if not Product.query.filter_by(name=name).first():
                            new_product = Product(name=name, price=price, discount_limit=discount_limit)
                            db.session.add(new_product)
                    except ValueError:
                        flash(f'無効なフォーマット: {line.strip()}', 'danger')

            db.session.commit()
            flash('商品情報をインポートしました', 'success')
        except Exception as e:
            flash(f'インポートエラー: {e}', 'danger')

    return render_template('import_products.html')

# ==========================
# 顧客と商品の関連付け
# ==========================
@main.route('/customer_product_link', methods=['GET', 'POST'])
def customer_product_link():
    customers = Customer.query.all()
    products = Product.query.all()

    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        product_id = request.form.get('product_id')
        desired_price = request.form.get('desired_price')

        if not customer_id or not product_id or not desired_price:
            flash('すべての項目を入力してください', 'danger')
            return redirect(url_for('main.customer_product_link'))

        existing_entry = CustomerProduct.query.filter_by(customer_id=customer_id, product_id=product_id).first()
        if existing_entry:
            flash('この顧客と商品の関連はすでに存在します', 'warning')
            return redirect(url_for('main.customer_product_link'))

        new_link = CustomerProduct(customer_id=customer_id, product_id=product_id, desired_price=desired_price)
        db.session.add(new_link)
        db.session.commit()
        flash('顧客と商品を結びつけました', 'success')
        return redirect(url_for('main.customer_product_link'))

    return render_template('customer_product_link.html', customers=customers, products=products)

# ==========================
# 限度額設定メニュー
# ==========================
@main.route('/discount_settings', methods=['GET', 'POST'])
def discount_settings():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('main.set_discount'))
        else:
            flash('パスワードが間違っています', 'danger')
    return render_template('discount_login.html')

@main.route('/set_discount', methods=['GET', 'POST'])
def set_discount():
    if not session.get('admin'):
        flash('認証が必要です', 'danger')
        return redirect(url_for('main.discount_settings'))

    if request.method == 'POST':
        product_id = request.form.get('product_id')
        new_discount_limit = request.form.get('discount_limit')
        product = Product.query.get(product_id)
        if product:
            product.discount_limit = new_discount_limit
            db.session.commit()
            flash('割引限度額を更新しました', 'success')
        else:
            flash('商品が見つかりません', 'danger')

    products = Product.query.all()
    return render_template('set_discount.html', products=products)
