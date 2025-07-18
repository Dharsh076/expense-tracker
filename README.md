# 💸 Expense Tracker Web App

A full-featured personal finance management system built with Flask. This web application helps users track daily expenses, set income targets, visualize spending by category, and compare expenses with income — all through a secure and responsive dashboard.

---

## 📌 Features

- 🔐 **User Authentication** – Register, login, and logout using secure password hashing and session management via Flask-Login.
- 💰 **Income Entry** – Input monthly income to calculate remaining budget.
- 🧾 **Expense Management** – Add, view, filter, and delete expenses (CRUD operations).
- 📊 **Visual Dashboard** – Interactive pie chart (Chart.js) of expenses by category.
- 🔍 **Smart Filtering** – Filter expenses by date range and category.
- ✅ **CSRF Protection** – Secure all forms using Flask-WTF CSRF tokens.
- 🎯 **Budget Comparison** – Compare total expenses with set income to calculate remaining balance.
- 📱 **Responsive UI** – Clean, mobile-friendly layout with Bootstrap 5.

---

## 🛠 Tech Stack

| Technology      | Purpose                        |
|----------------|----------------------------------|
| Python (Flask) | Web server and backend routing  |
| SQLite         | Lightweight relational database |
| SQLAlchemy     | ORM for DB interactions         |
| Flask-WTF      | Form rendering and CSRF security|
| Flask-Login    | User session/authentication     |
| Chart.js       | Pie chart for expense breakdown |
| Bootstrap 5    | Responsive frontend styling     |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Dharsh076/expense-tracker.git
cd expense-tracker
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # or on Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> If you don't have a `requirements.txt`, create one with:
> `pip freeze > requirements.txt`

### 4. Initialize the database

```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> app.app_context().push()
>>> db.create_all()
>>> exit()
```

### 5. Run the application

```bash
python run.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 🧪 Sample Use Case

1. Register a new user.
2. Enter your monthly income.
3. Add various expenses under categories like Food, Utilities, etc.
4. Use filters to track specific time periods or categories.
5. View the total spent vs income and pie chart summary.
6. Delete individual expenses securely.

---

## 🧷 Folder Structure

```
expense-tracker/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── add_expense.html
│   │   └── view_expenses.html
│   └── static/
│       └── style.css
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

---

## 🔐 Security Notes

- Passwords are hashed using Werkzeug before storing in the database.
- CSRF tokens are applied to all user-facing forms.
- Deletion is restricted to expense owners and requires POST confirmation.

---

## 📦 Future Improvements

- Export expenses to CSV
- Monthly savings goals
- Email reports and reminders
- Multi-user dashboards with admin roles
- Dark mode theme toggle

---

## 🧑‍💻 Author

**Dharshini Vasudevan**  
🔗 [LinkedIn](https://www.linkedin.com/in/dharshiniv/)  
📧 dharshinivasudevan99@gmail.com

---

## 🌟 Star the Repo

If you found this project helpful, consider giving it a ⭐ on GitHub — it really helps!