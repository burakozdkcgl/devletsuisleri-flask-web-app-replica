from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from logic.context import require_login
from logic.entity import Issue, User
from logic.db import db
from datetime import datetime

issue_bp = Blueprint("issue", __name__)

@issue_bp.route("/issues")
@require_login
def issues():
    from logic.entity import User
    user = User.query.get(session["user_id"])
    issues = Issue.query.order_by(Issue.created_at.desc()).all()
    unresolved = [i for i in issues if not i.approved_at]
    resolved = [i for i in issues if i.approved_at]
    return render_template("issues.html", issues=issues, unresolved=unresolved, resolved=resolved, user=user)

@issue_bp.route("/issues/create", methods=["POST"])
@require_login
def create_issue():
    content = request.form.get("content", "").strip()
    if not content:
        flash("Arıza içeriği boş olamaz.", "warning")
        return redirect(url_for("issue.issues"))

    issue = Issue(
        creator_id=session["user_id"],
        content=content,
        created_at=datetime.utcnow()
    )
    db.session.add(issue)
    db.session.commit()
    flash("Arıza başarıyla bildirildi.", "success")
    return redirect(url_for("issue.issues"))

@issue_bp.route("/issues/approve/<int:issue_id>", methods=["POST"])
@require_login
def approve_issue(issue_id):
    user = User.query.get(session["user_id"])
    if user.role.name.lower() not in ["admin", "şube müdürü"]:
        flash("Bu işlemi yapmaya yetkiniz yok.", "error")
        return redirect(url_for("issue.issues"))

    issue = Issue.query.get_or_404(issue_id)
    comment = request.form.get("approver_content", "").strip()
    issue.approver_id = user.id
    issue.approver_content = comment
    issue.approved_at = datetime.utcnow()
    db.session.commit()
    flash("Arıza onaylandı.", "success")
    return redirect(url_for("issue.issues"))

@issue_bp.route("/issues/<int:issue_id>")
@require_login
def issue_detail(issue_id):
    from logic.entity import User
    issue = Issue.query.get_or_404(issue_id)
    user = User.query.get(session["user_id"])
    return render_template("issue_detail.html", issue=issue, user=user)
