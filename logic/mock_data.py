from logic.entity import User, Role, Branch, UserCredential, Product, Inventory, Issue
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def insert_mock_data(db):
    if User.query.first() or Role.query.first() or Branch.query.first():
        return

    # Roller
    roles = [Role(name=r) for r in ["Admin", "Şube Müdürü", "Personel"]]
    db.session.add_all(roles)
    db.session.commit()
    role_map = {r.name: r.id for r in roles}

    # Şubeler
    branch_names = ["İnşaat", "Makine", "Elektrik", "Personel", "Destek"]
    branches = [Branch(name=n) for n in branch_names]
    db.session.add_all(branches)
    db.session.commit()
    branch_map = {b.name: b.id for b in branches}

    # Ürünler
    product_names = ["Monitör", "Klavye", "Fare", "Yazıcı", "Tarayıcı"]
    products = [Product(name=n) for n in product_names]
    db.session.add_all(products)
    db.session.commit()

    # Kullanıcılar
    user_data = [
        ("admin", "Polat Alemdar", "Admin", "İnşaat"),
        ("laziya", "Laz Ziya", "Şube Müdürü", "Makine"),
        ("mematibas", "Memati Baş", "Personel", "Makine"),
        ("necmi", "Testere Necmi", "Personel", "Elektrik"),
        ("abdulhey", "Abdülhey Çoban", "Personel", "İnşaat"),
        ("cakir", "Süleyman Çakır", "Personel", "Personel"),
        ("iskender", "İskender Büyük", "Personel", "Destek"),
        ("cahit", "Cahit Kaya", "Personel", "Elektrik"),
        ("tombalaci", "Tombalacı Mehmet", "Personel", "Makine"),
    ]

    users = []
    for username, fullname, role, branch in user_data:
        user = User(
            username=username,
            full_name=fullname,
            role_id=role_map[role],
            branch_id=branch_map[branch],
            email=f"{username}@example.com",
            internal_phone=str(random.randint(1000, 9999)),
        )
        db.session.add(user)
        users.append(user)
    db.session.commit()

    # Şifreler
    for user in users:
        db.session.add(UserCredential(user_id=user.id, password_hash=generate_password_hash("admin" if user.username == "admin" else "123")))
    db.session.commit()

    # Envanter: stoklar (her üründen 3-5 adet boşta)
    for product in products:
        for _ in range(random.randint(3, 5)):
            db.session.add(Inventory(product_id=product.id, user_id=None))
    db.session.commit()

    # Zimmetli envanter: rastgele 5 zimmet
    for _ in range(5):
        db.session.add(Inventory(
            product_id=random.choice(products).id,
            user_id=random.choice(users[2:]).id  # admin ve müdür harici
        ))
    db.session.commit()

    # Arıza kayıtları (gerçekçi açıklamalarla)
    ariza_listesi = [
        "Monitör ekranı aniden kararıyor, görüntü gidip geliyor.",
        "Klavye bazı tuşlara basmıyor, özellikle Q ve W.",
        "Yazıcı çıktı almıyor, kağıt almıyor hatası veriyor.",
        "Tarayıcı programı açılmıyor, sürücü güncellemesi gerekebilir.",
        "Fare çift tıklama sorunu yaşıyor, sağ tuş çalışmıyor.",
        "Monitörde yatay çizgiler belirdi, ekran bozuk olabilir.",
        "Yazıcıdan çıkan belgeler silik ve çizgili.",
        "Elektrik panosunda kıvılcım çıktı, acil kontrol gerekli."
    ]

    talep_sonuclari = [
        "Monitör değiştirildi.",
        "Yeni klavye temin edildi.",
        "Yazıcıya müdahale edildi, sorun çözüldü.",
        "Sürücü güncellendi, tarayıcı açılıyor.",
        "Yeni fare verildi.",
        "Monitör servise gönderildi.",
        "Toner değiştirildi, baskı düzeldi.",
        "Elektrikçi yönlendirildi, güvenlik sağlandı."
    ]

    for content, result in zip(ariza_listesi, talep_sonuclari):
        creator = random.choice(users[2:])  # personeller
        approver = random.choice(users[:2])  # admin veya müdür
        db.session.add(Issue(
            creator_id=creator.id,
            content=content,
            created_at=datetime.now() - timedelta(days=random.randint(1, 30)),
            approver_id=approver.id,
            approver_content=result,
            approved_at=datetime.now() - timedelta(days=random.randint(0, 5))
        ))
    db.session.commit()
