import os
import locale
import redis
import shutil
import datetime
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from models import db, Customer, Product, CustomerProduct

# Flask アプリケーションの設定
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db.init_app(app)

# Redis 設定
try:
    kv_store = redis.Redis(host='localhost', port=6379, db=0)
except Exception:
    kv_store = None

# メニュー関連のルート
@app.route('/')
def main_menu():
    return render_template('menu.html')

@app.route('/customers_menu')
def customers_menu():
    return render_template('customers_menu.html')

@app.route('/products_menu')
def products_menu():
    return render_template('products_menu.html')

# 割引限度額の設定 (上司のみ)
ADMIN_PASSWORD = "supervisor2024"

@app.route('/discount_settings', methods=['GET', 'POST'])
def discount_settings():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('set_discount'))
        else:
            flash('パスワードが間違っています', 'danger')

    return render_template('discount_login.html')

@app.route('/set_discount', methods=['GET', 'POST'])
def set_discount():
    if not session.get('admin'):
        flash('認証が必要です', 'danger')
        return redirect(url_for('discount_settings'))

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

# 顧客管理
@app.route('/customers', methods=['GET'])
def view_customers():
    customers = Customer.query.all()
    return render_template('view_customers.html', customers=customers)

@app.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        company = request.form.get('company')

        if not name or not email or not phone:
            flash('すべての項目を入力してください', 'danger')
            return redirect(url_for('add_customer'))

        new_customer = Customer(name=name, email=email, phone=phone, company=company)
        db.session.add(new_customer)
        db.session.commit()
        flash('顧客情報を追加しました', 'success')

    return render_template('add_customer.html')

# 商品管理
@app.route('/products', methods=['GET'])
def view_products():
    products = Product.query.all()
    return render_template('view_products.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')

        if not name or not price:
            flash('すべての項目を入力してください', 'danger')
            return redirect(url_for('add_product'))

        new_product = Product(name=name, price=float(price), discount_limit=0)
        db.session.add(new_product)
        db.session.commit()
        flash('商品情報を追加しました', 'success')

    return render_template('add_product.html')

# 顧客と商品の関連付け
@app.route('/customer_product_link', methods=['GET', 'POST'])
def customer_product_link():
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        product_id = request.form.get('product_id')
        desired_price = request.form.get('desired_price')

        if not customer_id or not product_id or not desired_price:
            flash('すべての項目を入力してください', 'danger')
            return redirect(url_for('customer_product_link'))

        new_link = CustomerProduct(customer_id=customer_id, product_id=product_id, desired_price=desired_price)
        db.session.add(new_link)
        db.session.commit()
        flash('顧客と商品の関連を追加しました', 'success')

    customers = Customer.query.all()
    products = Product.query.all()
    return render_template('customer_product_link.html', customers=customers, products=products)

# REST API: 顧客情報を取得
@app.route('/api/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{
        "id": customer.id,
        "name": customer.name,
        "email": customer.email,
        "phone": customer.phone,
        "company": customer.company
    } for customer in customers])

# REST API: 商品情報を取得
@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "discount_limit": product.discount_limit
    } for product in products])

# REST API: 顧客の希望価格リストを取得
@app.route('/api/customer_requests', methods=['GET'])
def get_customer_requests():
    requests = CustomerProduct.query.all()
    return jsonify([{
        "customer": req.customer.name,
        "product": req.product.name,
        "desired_price": req.desired_price
    } for req in requests])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
