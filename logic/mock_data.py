from logic.entity import User, Role, Branch, UserCredential, Product, Inventory
from werkzeug.security import generate_password_hash

def insert_mock_data(db):
    if User.query.first() or Role.query.first() or Branch.query.first():
        return

    # Roller
    roles = [Role(name=r) for r in ["Admin", "Şube Müdürü", "Personel"]]
    db.session.add_all(roles)
    db.session.commit()

    # Şubeler
    branches = [Branch(name=n) for n in ["İnşaat", "Makine", "Elektrik", "Personel", "Destek"]]
    db.session.add_all(branches)
    db.session.commit()

    # Ürünler
    products = [Product(name=n) for n in ["Monitör", "Klavye", "Fare", "Yazıcı", "Tarayıcı"]]
    db.session.add_all(products)
    db.session.commit()

     # Kullanıcılar
    users = []
    creds = []
    for i in range(7):
        user = User(
            username=f"kullanici{i+1}",
            full_name=f"Kullanıcı {i+1}",
            role_id=roles[i % len(roles)].id,
            branch_id=branches[i % len(branches)].id,
            internal_phone=f"1234{i+1}",
            email=f"kullanici{i+1}@example.com"
        )
        users.append(user)
        db.session.add(user)

    db.session.commit()

    # Şifreler
    for user in users:
        creds.append(UserCredential(
            user_id=user.id,
            password_hash=generate_password_hash("1234")
        ))

    db.session.add_all(creds)
    db.session.commit()


     # Envanter – her üründen 3 adet stokta (boşta)
    inventory = []
    for product in products:
        for _ in range(3):
            inventory.append(Inventory(product_id=product.id, user_id=None))
    db.session.add_all(inventory)
    db.session.commit()

    # Bazı zimmetli örnekler – ilk 3 kullanıcıya bazı ürünler zimmetlenmiş olsun
    db.session.add_all([
        Inventory(product_id=products[0].id, user_id=users[0].id),  # monitör → kullanıcı 1
        Inventory(product_id=products[1].id, user_id=users[1].id),  # klavye → kullanıcı 2
        Inventory(product_id=products[2].id, user_id=users[2].id),  # fare → kullanıcı 3
    ])
    db.session.commit()
