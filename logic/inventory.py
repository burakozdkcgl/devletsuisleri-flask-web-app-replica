from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from logic.entity import Product, Inventory, User
from logic.db import db
from logic.context import require_login

inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.route("/inventory", methods=["GET"])
@require_login
def inventory_view():
    # Ürün özetleri
    summary = []
    products = Product.query.order_by(Product.name).all()
    for product in products:
        total = Inventory.query.filter_by(product_id=product.id).count()
        assigned = Inventory.query.filter_by(product_id=product.id).filter(Inventory.user_id.isnot(None)).count()
        unassigned = total - assigned
        summary.append({
            "product": product,
            "total": total,
            "assigned": assigned,
            "unassigned": unassigned
        })

    inventory = Inventory.query.all()
    users = User.query.order_by(User.full_name).all()
    return render_template("inventory.html", summary=summary, inventory=inventory, products=products, users=users)


@inventory_bp.route("/inventory/assign", methods=["POST"])
@require_login
def assign_inventory():
    product_id = request.form.get("product_id")
    user_id = request.form.get("user_id")

    item = Inventory.query.filter_by(product_id=product_id, user_id=None).first()
    if not item:
        flash("Stokta boş ürün yok.", "error")
    else:
        item.user_id = user_id
        db.session.commit()
        flash("Ürün başarıyla zimmetlendi.", "success")
    return redirect(url_for("inventory.inventory_view"))


@inventory_bp.route("/inventory/unassign/<int:item_id>", methods=["POST"])
@require_login
def unassign_inventory(item_id):
    item = Inventory.query.get(item_id)
    if item:
        item.user_id = None
        db.session.commit()
        flash("Zimmet kaldırıldı.", "info")
    return redirect(url_for("inventory.inventory_view"))


@inventory_bp.route("/inventory/add_stock", methods=["POST"])
@require_login
def add_stock():
    product_id = request.form.get("product_id")
    quantity = int(request.form.get("quantity", 0))

    if quantity <= 0:
        flash("Geçerli bir miktar giriniz.", "error")
    else:
        items = [Inventory(product_id=product_id, user_id=None) for _ in range(quantity)]
        db.session.add_all(items)
        db.session.commit()
        flash(f"{quantity} adet ürün eklendi.", "success")

    return redirect(url_for("inventory.inventory_view"))

@inventory_bp.route("/inventory/remove_stock", methods=["POST"])
@require_login
def remove_stock():
    product_id = request.form.get("product_id")
    quantity = int(request.form.get("quantity", 0))

    if quantity <= 0:
        flash("Geçerli bir miktar giriniz.", "error")
        return redirect(url_for("inventory.inventory_view"))

    unassigned_items = Inventory.query.filter_by(product_id=product_id, user_id=None).limit(quantity).all()

    if len(unassigned_items) < quantity:
        flash("Yeterli stok yok.", "error")
    else:
        for item in unassigned_items:
            db.session.delete(item)
        db.session.commit()
        flash(f"{quantity} adet ürün stoktan çıkarıldı.", "success")

    return redirect(url_for("inventory.inventory_view"))
