```python
from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Customer

# ルートやビューを管理するためのBlueprintを作成
main = Blueprint('main', __name__)

@main.route('/')
def menu():
    return render_template('menu.html')

# 顧客情報を一覧表示するルート
@main.route('/customers', methods=['GET'])
def view_customers():
    customers = Customer.query.all()
    return render_template('view_customers.html', customers=customers)

# 顧客情報を追加するルート
@main.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        new_customer = Customer(name=name, email=email, phone=phone)
        db.session.add(new_customer)
        db.session.commit()
        return redirect(url_for('main.view_customers'))
    return render_template('add_customer.html')

# 顧客情報を編集するルート
@main.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    customer = Customer.query.get(id)
    if request.method == 'POST':
        customer.name = request.form['name']
        customer.email = request.form['email']
        customer.phone = request.form['phone']
        db.session.commit()
        return redirect(url_for('main.view_customers'))
    return render_template('edit_customer.html', customer=customer)
```
