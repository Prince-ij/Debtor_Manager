from app import app, db
import sqlalchemy as sa
from flask_login import login_required
from flask import render_template, flash, redirect, url_for
from flask import request
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Debtor

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        remember = request.form.get("remember_me") is not None

        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=remember)
        return redirect(url_for('dashboard'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_required
@app.route('/dashboard')
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
   
    total_amount_due = current_user.total_amount_due
    total_debtors = current_user.total_debtors
    return render_template('dashboard.html', total_amount=total_amount_due, total_debtors=total_debtors)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if password == confirm_password:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error='passwords do not match !')
    return render_template('register.html')

@login_required
@app.route('/profile')
def profile():
    return render_template('profile.html', user=current_user)

@login_required
@app.route('/add_debtor', methods=['GET', 'POST'])
def add_debtor():
    if request.method == 'POST':
        username = request.form.get("username")
        amount_due = request.form.get("amount_due")
        description = request.form.get("description")

        if not username or not amount_due:
            flash('Username and Amount Due are required', 'error')
            return redirect(url_for('add_debtor'))

        try:
            amount_due = float(amount_due)
        except ValueError:
            flash('Amount due must be a number.', 'error')
            return redirect(url_for('add_debtor'))

        new_debtor = Debtor(
                username=username,
                amount_due=amount_due,
                description=description,
                user_id = current_user.id
                )

        db.session.add(new_debtor)
        db.session.commit()

        flash('Debtor added Successfully', 'success')
        return redirect(url_for('add_debtor'))
    return render_template('add_debtor.html')

@app.route('/remove/<int:debtor_id>', methods=['GET', 'POST'])
@login_required
def remove(debtor_id):
    debtor = Debtor.query.get(debtor_id)
    db.session.delete(debtor)
    db.session.commit()

    return redirect(url_for('view_debtor'))


@login_required
@app.route('/view_debtor')
def view_debtor():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    debtors = Debtor.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=per_page)
    return render_template('view_debtor.html', debtors=debtors)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        current_user.username = request.form.get("name")
        current_user.email = request.form.get("email")
        current_user.phone_number = request.form.get("phone")
        current_user.address = request.form.get("address")
        db.session.commit()
        flash('Your changes have been saved ')
        return redirect(url_for('settings'))
    return render_template('settings.html', user=current_user)
