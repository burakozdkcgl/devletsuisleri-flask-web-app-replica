from logic.db import db  # SQLAlchemy nesnesini alıyoruz

# ────────────────────────────────
# ROL TABLOSU (Admin, Personel vs.)
# Sabit veri: Kullanıcıların yetki seviyesi
# ────────────────────────────────
class Role(db.Model):
    __tablename__ = "roles"  # veritabanında tablo adı
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  # örnek: 'Admin', 'Personel'

    # Bu role ait tüm kullanıcılar (ters ilişki)
    users = db.relationship("User", backref="role", lazy=True)
    # → user.role.name şeklinde bu veriye erişilebilir


# ────────────────────────────────
# ŞUBE TABLOSU
# Dinamik veri: Eklenip silinebilir
# ────────────────────────────────
class Branch(db.Model):
    __tablename__ = "branches"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    # Bu şubeye ait tüm kullanıcılar
    users = db.relationship("User", backref="branch", lazy=True)
    # → user.branch.name şeklinde erişim sağlanır


# ────────────────────────────────
# KULLANICI TABLOSU
# Kullanıcı bilgileri burada tutulur
# ────────────────────────────────
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)

    # KULLANICI ADI → benzersiz ve zorunlu
    username = db.Column(db.String(50), nullable=False, unique=True)

    # AD SOYAD
    full_name = db.Column(db.String(100), nullable=False)

    # E POSTA
    email = db.Column(db.String(100), nullable=True)

    # DAHILI TELEFON
    internal_phone = db.Column(db.String(20), nullable=True)

    # Rol (zorunlu) → her kullanıcı bir role sahip olmalı
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)

    # Şube (isteğe bağlı) → bazı kullanıcıların şubesi olmayabilir
    branch_id = db.Column(db.Integer, db.ForeignKey("branches.id", ondelete="SET NULL"), nullable=True)

    # One-to-one ilişki: Kullanıcının şifresi (UserCredential)
    credentials = db.relationship("UserCredential", backref="user", uselist=False, cascade="all, delete-orphan")
    # → user.credentials.password_hash ile erişilir


# ────────────────────────────────
# ŞİFRE TABLOSU
# Şifre bilgileri ayrı bir tabloda tutulur (güvenlik için)
# ────────────────────────────────
class UserCredential(db.Model):
    __tablename__ = "user_credentials"
    id = db.Column(db.Integer, primary_key=True)

    # Hangi kullanıcıya ait olduğunu belirten foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)

    # Şifrenin hashlenmiş hali
    password_hash = db.Column(db.String(255), nullable=True)


# Ürün tablosu
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    inventories = db.relationship("Inventory", backref="product", lazy=True, cascade="all, delete-orphan", passive_deletes=True)


#Envanter tablosu
class Inventory(db.Model):
    __tablename__ = "inventory"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    user = db.relationship("User", backref="inventory_items")
