from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, Customer, Product, CustomerProduct

main = Blueprint('main', __name__)

ADMIN_PASSWORD = "supervisor2024"

@main.route('/')
def main_menu():
    """メインメニューを表示"""
    return render_template('menu.html')

@main.route('/customers')
def view_customers():
    """顧客一覧を表示"""
    customers = Customer.query.all()
    return render_template('view_customers.html', customers=customers)

@main.route('/products')
def view_products():
    """商品一覧を表示"""
    products = Product.query.all()
    return render_template('view_products.html', products=products)

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

@main.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    """新規顧客を追加"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        company = request.form['company']
        new_customer = Customer(name=name, email=email, phone=phone, company=company)
        db.session.add(new_customer)
        db.session.commit()
        flash('顧客情報を追加しました', 'success')
        return redirect(url_for('main.view_customers'))
    
    return render_template('add_customer.html')

@main.route('/customers/edit/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    """顧客情報を編集"""
    customer = Customer.query.get_or_404(customer_id)
    
    if request.method == 'POST':
        customer.name = request.form['name']
        customer.email = request.form['email']
        customer.phone = request.form['phone']
        customer.company = request.form['company']
        db.session.commit()
        flash('顧客情報を更新しました', 'success')
        return redirect(url_for('main.view_customers'))
    
    return render_template('edit_customer.html', customer=customer)

@main.route('/customers/delete/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    """顧客を削除"""
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    flash('顧客情報を削除しました', 'success')
    return redirect(url_for('main.view_customers'))

@main.route('/customers/import', methods=['GET', 'POST'])
def import_customers():
    """顧客データを `customers.txt` からインポート"""
    if request.method == 'POST':
        try:
            with open("customers.txt", 'r', encoding='utf-8') as file:
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
            flash('顧客情報をインポートしました。', 'success')
        except Exception as e:
            flash(f'インポート中にエラーが発生しました: {e}', 'danger')
    return render_template('import_customers.html')
