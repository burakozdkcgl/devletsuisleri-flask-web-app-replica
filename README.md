# DSI Web App Clone (Flask)

This project is a simplified clone of an internal web system used by a government institution. It includes user login, inventory tracking, issue reporting, and a role-based admin panel. Designed for internal use with a clean and minimal interface.


## Installation

- Install dependencies:

```bash
pip install -r requirements.txt
```

- Configure the database in `config.py`:

```python
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:yourpassword@localhost/dsi_clone"
```

- Run `app.py`

## Screenshots

![ScreenShot](/screenshots/ss1.png)
![ScreenShot](/screenshots/ss2.png)
![ScreenShot](/screenshots/ss3.png)
![ScreenShot](/screenshots/ss4.png)
![ScreenShot](/screenshots/ss5.png)
![ScreenShot](/screenshots/ss6.png)

---

## Features

- User authentication with session-based login
- Role-based access control (Admin, Branch Manager, Employee)
- New users can log in without a password and set it from their account
- Add and remove stock items for each product type
- Assign items to users and revoke assignments
- Report and approve technical issues with comments
- Admin panel for managing users, branches, and products
- Homepage with slider and quick access buttons
- Staff directory with user and branch information