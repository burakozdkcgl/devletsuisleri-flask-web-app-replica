from flask import Blueprint, render_template, request, redirect, url_for, flash
from logic.entity import Branch, User, Role
from logic.db import db
from logic.context import require_admin

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@require_admin
def admin_index():
    return render_template("admin.html")


@admin_bp.route("/branches", methods=["GET", "POST"])
@require_admin
def branch_settings():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Şube adı boş olamaz.", "error")
        elif Branch.query.filter_by(name=name).first():
            flash("Bu isimde bir şube zaten var.", "error")
        else:
            db.session.add(Branch(name=name))
            db.session.commit()
            flash("Şube başarıyla eklendi.", "success")
        return redirect(url_for("admin.branch_settings"))

    branches = Branch.query.order_by(Branch.name).all()
    return render_template("admin_branches.html", branches=branches)


@admin_bp.route("/branches/update/<int:branch_id>", methods=["POST"])
@require_admin
def update_branch(branch_id):
    branch = Branch.query.get(branch_id)
    new_name = request.form.get("name", "").strip()

    if not branch:
        flash("Şube bulunamadı.", "error")
    elif not new_name:
        flash("Şube adı boş olamaz.", "error")
    elif Branch.query.filter(Branch.name == new_name, Branch.id != branch_id).first():
        flash("Bu isimde başka bir şube zaten var.", "error")
    else:
        branch.name = new_name
        db.session.commit()
        flash("Şube güncellendi.", "success")

    return redirect(url_for("admin.branch_settings"))


@admin_bp.route("/branches/delete/<int:branch_id>", methods=["POST"])
@require_admin
def delete_branch(branch_id):
    branch = Branch.query.get(branch_id)
    if not branch:
        flash("Şube bulunamadı.", "error")
    else:
        db.session.delete(branch)
        db.session.commit()
        flash("Şube silindi.", "info")
    return redirect(url_for("admin.branch_settings"))


@admin_bp.route("/users", methods=["GET", "POST"])
@require_admin
def user_settings():
    roles = Role.query.all()
    branches = Branch.query.order_by(Branch.name).all()
    users = User.query.order_by(User.full_name).all()
    return render_template("admin_users.html", users=users, roles=roles, branches=branches)

@admin_bp.route("/users/update/<int:user_id>", methods=["POST"])
@require_admin
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        flash("Kullanıcı bulunamadı.", "error")
        return redirect(url_for("admin.user_settings"))

    try:
        user.role_id = int(request.form.get("role_id"))
        branch_id = request.form.get("branch_id")
        user.branch_id = int(branch_id) if branch_id else None
        user.internal_phone = request.form.get("internal_phone", "").strip()  # EKLENDİ
        db.session.commit()
        flash("Kullanıcı güncellendi.", "success")
    except Exception:
        db.session.rollback()
        flash("Güncelleme sırasında hata oluştu.", "error")

    return redirect(url_for("admin.user_settings"))

@admin_bp.route("/users/delete/<int:user_id>", methods=["POST"])
@require_admin
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        flash("Kullanıcı bulunamadı.", "error")
    else:
        db.session.delete(user)
        db.session.commit()
        flash("Kullanıcı silindi.", "info")
    return redirect(url_for("admin.user_settings"))
    

@admin_bp.route("/users/new", methods=["GET", "POST"])
@require_admin
def create_user():
    if request.method == "POST":
        full_name = request.form["full_name"]
        username = request.form["username"]
        email = request.form.get("email")
        internal_phone = request.form.get("internal_phone")
        role_id = int(request.form["role_id"])
        branch_id = request.form.get("branch_id") or None

        if User.query.filter_by(username=username).first():
            flash("Bu kullanıcı adı zaten mevcut.", "error")
            return redirect(url_for("admin.create_user"))

        new_user = User(
            full_name=full_name,
            username=username,
            email=email,
            internal_phone=internal_phone,
            role_id=role_id,
            branch_id=branch_id
        )
        db.session.add(new_user)
        db.session.flush()  # user.id gelsin diye

        # Şifre bilgisi NULL
        db.session.commit()
        flash("Kullanıcı başarıyla oluşturuldu.", "success")
        return redirect(url_for("admin.user_settings"))

    roles = Role.query.all()
    branches = Branch.query.order_by(Branch.name).all()
    return render_template("admin_new_user.html", roles=roles, branches=branches)
