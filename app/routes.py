from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import AddExpenseForm
from datetime import date
from flask import session
from app import csrf
import csv
from io import StringIO
from flask import make_response
from app.models import User, Expense, Income
from flask_login import LoginManager
from flask import Blueprint, jsonify





main = Blueprint('main', __name__)

@main.route('/')
def home():
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('main.register'))
        
        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_pw
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', form=form)

login_manager = LoginManager()

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('main.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@main.route('/test')
def test():
    return "Test route works!"

@main.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    form = AddExpenseForm()
    if form.validate_on_submit():
        new_expense = Expense(
            amount=form.amount.data,
            category=form.category.data,
            description=form.description.data,
            date=form.date.data or date.today(),
            owner=current_user
        )
        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('main.view_expenses'))
    return render_template('add_expense.html', form=form)

@main.route('/expenses', methods=['GET', 'POST'])
@login_required
def view_expenses():
    # ── filters from the query‑string ───────────────────────────
    category_filter = request.args.get('category')
    start_date      = request.args.get('start_date')
    end_date        = request.args.get('end_date')
    show_chart      = request.args.get('show_chart')

    # ── optional income input from the query‑string ─────────────
    income_input = request.args.get('income', type=float)
    if income_input is not None:
        # upsert the user’s income in the DB
        existing = Income.query.filter_by(user_id=current_user.id).first()
        if existing:
            existing.amount = income_input
        else:
            db.session.add(Income(amount=income_input, user_id=current_user.id))
        db.session.commit()

    # ── fetch the stored income (default 0) ─────────────────────
    income_obj = Income.query.filter_by(user_id=current_user.id).first()
    income     = income_obj.amount if income_obj else 0

    # ── build the expense query with filters ────────────────────
    expenses_q = Expense.query.filter_by(user_id=current_user.id)
    if category_filter:
        expenses_q = expenses_q.filter_by(category=category_filter)
    if start_date:
        expenses_q = expenses_q.filter(Expense.date >= start_date)
    if end_date:
        expenses_q = expenses_q.filter(Expense.date <= end_date)

    page = request.args.get('page', 1, type=int)
    per_page = 5

    expenses_pagination = expenses_q.order_by(Expense.date.desc()).paginate(page=page, per_page=per_page)
    expenses = expenses_pagination.items
    total    = sum(e.amount for e in expenses)
    remaining = income - total

    # ── category totals for the pie‑chart ───────────────────────
    category_data = {}
    if show_chart:
        total_expense = 0
        for e in expenses:
            category_data[e.category] = category_data.get(e.category, 0) + e.amount
            total_expense += e.amount

        income_obj = Income.query.filter_by(user_id=current_user.id).first()
        income = income_obj.amount if income_obj else 0

        income_remaining = max(0, income - total_expense)
        category_data = {'Remaining Income': income_remaining, **category_data}



    # ── render ──────────────────────────────────────────────────
    return render_template('view_expenses.html',
        expenses=expenses,
        pagination=expenses_pagination,
        total=total,
        category_data=category_data,
        show_chart=show_chart,
        category_filter=category_filter,
        start_date=start_date,
        end_date=end_date,
        income=income,
        remaining=remaining
    )

@main.route("/health")
def health():
    return jsonify(status="ok"), 200


@main.route('/delete/<int:expense_id>', methods=['POST'])
@csrf.exempt  # ✅ This tells Flask to skip CSRF check for this route
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)

    if expense.owner != current_user:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('main.view_expenses'))

    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully.', 'success')
    return redirect(url_for('main.view_expenses'))

@main.route('/test-csrf', methods=['GET', 'POST'])
@login_required
def test_csrf():
    if request.method == 'POST':
        flash('CSRF passed. POST worked!', 'success')
        return redirect(url_for('main.test_csrf'))
    return render_template('test_csrf.html')



@main.route('/export')
@login_required
def export_expenses():
    import csv
    from io import StringIO
    from flask import make_response

    category_filter = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    expenses_query = Expense.query.filter_by(user_id=current_user.id)
    if category_filter:
        expenses_query = expenses_query.filter_by(category=category_filter)
    if start_date:
        expenses_query = expenses_query.filter(Expense.date >= start_date)
    if end_date:
        expenses_query = expenses_query.filter(Expense.date <= end_date)

    expenses = expenses_query.order_by(Expense.date.desc()).all()
    total = sum(e.amount for e in expenses)

    income_obj = Income.query.filter_by(user_id=current_user.id).first()
    income = income_obj.amount if income_obj else 0
    remaining = income - total

    # Generate CSV
    si = StringIO()
    writer = csv.writer(si)

    # Header summary
    writer.writerow(['Income:', income])
    writer.writerow(['Remaining:', remaining])
    writer.writerow([])

    # Expense table
    writer.writerow(["Date", "Amount ($)", "Category", "Description"])
    for e in expenses:
        writer.writerow([e.date.strftime('%Y-%m-%d'), e.amount, e.category, e.description or ""])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=expenses.csv"
    output.headers["Content-type"] = "text/csv"
    return output

