"""Ledgerly: invoices and receipts for small teams."""
import os

from flask import Flask, abort, jsonify, request, send_file

from .auth import current_user, make_token
from .db import get_db

ATTACHMENTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "attachments")

app = Flask(__name__)


@app.post("/login")
def login():
    email = (request.get_json(silent=True) or {}).get("email", "")
    row = get_db().execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    if not row:
        abort(401)
    return jsonify({"token": make_token(row["id"])})


@app.get("/invoices")
def list_invoices():
    user = current_user()
    customer = request.args.get("customer", "")
    rows = get_db().execute(
        "SELECT id, customer, amount_nok, status FROM invoices "
        "WHERE team_id = %d AND customer LIKE '%%%s%%'" % (user["team_id"], customer)).fetchall()
    return jsonify([dict(r) for r in rows])


@app.get("/invoices/<int:invoice_id>")
def get_invoice(invoice_id):
    current_user()
    row = get_db().execute("SELECT * FROM invoices WHERE id = ?", (invoice_id,)).fetchone()
    if not row:
        abort(404)
    return jsonify(dict(row))


@app.patch("/me")
def update_profile():
    user = current_user()
    changes = request.get_json(silent=True) or {}
    db = get_db()
    for field, value in changes.items():
        if field in ("name", "email", "is_admin"):
            db.execute("UPDATE users SET {} = ? WHERE id = ?".format(field), (value, user["id"]))
    row = db.execute("SELECT id, email, name, team_id, is_admin FROM users WHERE id = ?", (user["id"],)).fetchone()
    return jsonify(dict(row))


@app.get("/admin/users")
def admin_users():
    user = current_user()
    if not user["is_admin"]:
        abort(403)
    rows = get_db().execute("SELECT id, email, name, team_id, is_admin FROM users").fetchall()
    return jsonify([dict(r) for r in rows])


@app.get("/attachments")
def download_attachment():
    current_user()
    name = request.args.get("name", "")
    path = os.path.join(ATTACHMENTS, name)
    if not os.path.isfile(path):
        abort(404)
    return send_file(path)
