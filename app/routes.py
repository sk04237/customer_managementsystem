import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, Customer, Product

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

@main.route('/customers/import', methods=['GET', 'POST'])
def import_customers():
    """顧客データを `customers.txt` からインポート"""
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
            flash(f'インポート中にエラーが発生しました: {e}', 'danger')

    return render_template('import_customers.html')

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

@main.route('/products/import', methods=['GET', 'POST'])
def import_products():
    """商品データを `goods.txt` からインポート"""
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
            flash(f'インポート中にエラーが発生しました: {e}', 'danger')

    return render_template('import_products.html')

@main.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    """商品の情報を編集"""
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = float(request.form['price'])
        product.discount_limit = float(request.form.get('discount_limit', 0))
        db.session.commit()
        flash('商品情報を更新しました', 'success')
        return redirect(url_for('main.view_products'))
    
    return render_template('edit_product.html', product=product)

@main.route('/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    """商品を削除"""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('商品を削除しました', 'success')
    return redirect(url_for('main.view_products'))

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
