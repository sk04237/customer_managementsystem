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
    """メインメニューを表示"""
    return render_template('menu.html')

# ==========================
# 顧客管理メニュー
# ==========================
@main.route('/customers_menu')
def customers_menu():
    """顧客管理メニューを表示"""
    return render_template('customers_menu.html')

@main.route('/customers')
def view_customers():
    """顧客一覧を表示"""
    customers = Customer.query.all()
    return render_template('view_customers.html', customers=customers)

@main.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    """新規顧客を追加"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        company = request.form.get('company', None)
        new_customer = Customer(name=name, email=email, phone=phone, company=company)
        db.session.add(new_customer)
        db.session.commit()
        flash('顧客情報を追加しました', 'success')
        return redirect(url_for('main.view_customers'))
    
    return render_template('add_customer.html')

# ==========================
# 商品管理メニュー
# ==========================
@main.route('/products_menu')
def products_menu():
    """商品管理メニューを表示"""
    return render_template('products_menu.html')

@main.route('/products')
def view_products():
    """商品一覧を表示"""
    products = Product.query.all()
    return render_template('view_products.html', products=products)

@main.route('/products/add', methods=['GET', 'POST'])
def add_product():
    """新規商品を追加"""
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        discount_limit = float(request.form.get('discount_limit', 0))
        new_product = Product(name=name, price=price, discount_limit=discount_limit)
        db.session.add(new_product)
        db.session.commit()
        flash('商品を追加しました', 'success')
        return redirect(url_for('main.view_products'))
    
    return render_template('add_product.html')

# ==========================
# 顧客と商品の関連付け
# ==========================
@main.route('/customers/<int:customer_id>/link_product', methods=['GET', 'POST'])
def link_product(customer_id):
    """顧客に商品を関連付ける"""
    customer = Customer.query.get_or_404(customer_id)
    products = Product.query.all()

    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        desired_price = float(request.form['desired_price'])

        existing_entry = CustomerProduct.query.filter_by(customer_id=customer_id, product_id=product_id).first()
        if existing_entry:
            flash('この顧客にはすでにこの商品が関連付けられています。', 'warning')
        else:
            new_link = CustomerProduct(customer_id=customer_id, product_id=product_id, desired_price=desired_price)
            db.session.add(new_link)
            db.session.commit()
            flash('商品を顧客に関連付けました', 'success')

        return redirect(url_for('main.view_customers'))

    return render_template('customer_product_link.html', customer=customer, products=products)

# ==========================
# 限度額設定メニュー
# ==========================
@main.route('/discount_settings', methods=['GET', 'POST'])
def discount_settings():
    """割引限度額の設定（上司のみアクセス可能）"""
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
    """割引限度額の設定ページ（認証済みユーザーのみ）"""
    if not session.get('admin'):
        flash('認証が必要です', 'danger')
        return redirect(url_for('main.discount_settings'))

    if request.method == 'POST':
        product_id = request.form.get('product_id')
        new_discount_limit = float(request.form.get('discount_limit'))
        product = Product.query.get(product_id)
        if product:
            product.discount_limit = new_discount_limit
            db.session.commit()
            flash('割引限度額を更新しました', 'success')
        else:
            flash('商品が見つかりません', 'danger')

    products = Product.query.all()
    return render_template('set_discount.html', products=products)
