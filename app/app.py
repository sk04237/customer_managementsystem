```python
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Customer
import os

main = Blueprint('main', __name__)

data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')

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
        return redirect(url_for('main.view_customers'))
    return render_template('edit_customer.html', customer=customer)

@main.route('/customers/import', methods=['POST'])
def import_customers():
    try:
        file_path = os.path.join(data_folder, 'customers.txt')
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue  # コメント行または空行は無視
                name, email, phone = line.split(',')
                new_customer = Customer(name=name.strip(), email=email.strip(), phone=phone.strip())
                db.session.add(new_customer)
            db.session.commit()
        flash('顧客情報をインポートしました！', 'success')
    except Exception as e:
        flash(f'エラーが発生しました: {str(e)}', 'danger')
    return redirect(url_for('main.view_customers'))
```
