from logic.entity import User, Role, Branch, UserCredential
from werkzeug.security import generate_password_hash

def insert_mock_data(db):
    if User.query.first() or Role.query.first() or Branch.query.first():
        return

    # Roller
    roles = [Role(name=r) for r in ["Admin", "User", "Technician"]]
    db.session.add_all(roles)
    db.session.commit()

    # Şubeler
    branches = [Branch(name=n) for n in ["İnşaat", "Makine", "Elektrik", "Personel", "Destek"]]
    db.session.add_all(branches)
    db.session.commit()

    # Kullanıcılar
    users = []
    creds = []
    for i in range(5):
        user = User(
            username=f"kullanici{i+1}",
            full_name=f"Kullanıcı {i+1}",
            role_id=roles[i % len(roles)].id,
            branch_id=branches[i % len(branches)].id
        )
        users.append(user)
        db.session.add(user)

    db.session.commit()

    for user in users:
        creds.append(UserCredential(
            user_id=user.id,
            password_hash=generate_password_hash("1234")
        ))

    db.session.add_all(creds)
    db.session.commit()
