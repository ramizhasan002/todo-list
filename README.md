# Todo List — Web App

A clean, minimal task management web app built with Flask. Designed to help you stay organised without the clutter — just add your tasks, track them, and get things done.

**Live demo → [arden002.pythonanywhere.com](https://arden002.pythonanywhere.com)**

---

## Features

- **User accounts** — register, log in, and log out securely
- **Add tasks** — with optional description and date & time
- **Edit tasks** — update title, description, or due date anytime
- **Complete tasks** — mark tasks as done with a single click
- **Recycle bin** — deleted tasks go to a bin, not gone forever
- **Restore or permanently delete** — full control over deleted tasks
- **Empty bin** — clear everything in the recycle bin at once
- **Delete all tasks** — move all active tasks to the bin in one go

---

## Tech Stack

| Layer            | Technology                    |
|------------------|-------------------------------|
| Backend          | Python, Flask                 |
| Database         | SQLite, Flask-SQLAlchemy      |
| Authentication   | Flask-Login, Flask-Bcrypt     |
| Forms & Security | Flask-WTF, CSRF protection    |
| Frontend         | HTML, CSS, JavaScript         |
| Fonts            | DM Sans, DM Serif Display     |
| Hosting          | PythonAnywhere                |

---

## Project Structure

```
todo_list_app/
├── app/
│   ├── __init__.py         # App factory
│   ├── extensions.py       # db, bcrypt, login_manager
│   ├── models.py           # User and Task models
│   ├── form.py             # WTForms form classes
│   ├── routes/
│   │   ├── auth.py         # Register, login, logout
│   │   └── tasks.py        # All task CRUD routes
│   ├── static/
│   │   ├── css/            # Page stylesheets
│   │   └── js/             # JavaScript files
│   └── templates/
│       ├── base.html       # Shared layout
│       ├── home.html       # Task list page
│       ├── edit.html       # Edit task page
│       ├── login.html      # Login page
│       ├── register.html   # Register page
│       ├── recycle.html    # Recycle bin page
│       └── about.html      # About page
├── run.py
└── requirements.txt
```


## Author
**Ramiz Hasan**
GitHub → [@ramizhasan002](https://github.com/ramizhasan002)

