"""
Omnify Store – Система управления заказами
==========================================
Паттерны: Factory Method, Abstract Factory, Singleton, Builder,
          Prototype, Adapter, Observer, Strategy, Decorator
+ Auth: регистрация / вход / admin panel
"""

import uuid
from functools import wraps
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash

from patterns.factory_method import create_cloneable_product
from patterns.abstract_factory import get_payment_factory, PAYMENT_FACTORIES
from patterns.singleton import CartManager
from patterns.builder import OrderBuilder, save_order, get_order, get_all_orders, validate_coupon
from patterns.observer import EmailObserver, SMSObserver, PushObserver, notification_service
from patterns.strategy import get_delivery_strategy, DELIVERY_STRATEGIES
from patterns.adapter import get_payment_adapter
from patterns.decorator import BaseOrder, apply_decorators
from patterns.auth import (
    register_user, login_user, get_user, get_all_users, set_admin, delete_user
)

app = Flask(__name__)
app.secret_key = "omnify-secret-2026"

# ── Каталог товаров ───────────────────────────
CATALOG = [
    create_cloneable_product("physical", "p1", "Смартфон Samsung Galaxy S25", 999, weight_kg=0.2),
    create_cloneable_product("physical", "p2", "Ноутбук ASUS ROG", 1449, weight_kg=2.5),
    create_cloneable_product("physical", "p3", "Беспроводные наушники Sony", 279, weight_kg=0.3),
    create_cloneable_product("physical", "p4", "Умные часы Apple Watch", 449, weight_kg=0.05),
    create_cloneable_product("digital",  "d1", "Adobe Photoshop (1 год)", 89,  download_url="/download/photoshop"),
    create_cloneable_product("digital",  "d2", "Курс Python для профессионалов", 55, download_url="/download/python-course"),
    create_cloneable_product("digital",  "d3", "Антивирус Kaspersky (1 год)", 28, download_url="/download/kaspersky"),
    create_cloneable_product("subscription", "s1", "Подписка Netflix Premium", 11,  period_days=30),
    create_cloneable_product("subscription", "s2", "Подписка Spotify Family",  4,  period_days=30),
    create_cloneable_product("subscription", "s3", "Облако 1 ТБ (Яндекс Диск)", 2,  period_days=30),
]
CATALOG_DICT = {p.product_id: p for p in CATALOG}

cart_manager = CartManager()


# ── Helpers ──────────────────────────────────

def get_cart_user_id() -> str:
    if "auth_user_id" in session:
        return session["auth_user_id"]
    if "guest_id" not in session:
        session["guest_id"] = "guest_" + str(uuid.uuid4())[:8]
    return session["guest_id"]


def get_current_user() -> dict | None:
    uid = session.get("auth_user_id")
    return get_user(uid) if uid else None


# ── Auth decorators ───────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("auth_user_id"):
            flash("Необходимо войти в систему", "error")
            return redirect(url_for("login", next=request.path))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user or not user.get("is_admin"):
            flash("Доступ запрещён", "error")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated


# ── Context processor ─────────────────────────

@app.context_processor
def inject_globals():
    user = get_current_user()
    uid = get_cart_user_id()
    return {
        "current_user": user,
        "cart_count": cart_manager.cart_count(uid),
    }


# ═══════════════════════════════════════
#  AUTH ROUTES
# ═══════════════════════════════════════

@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("auth_user_id"):
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        if password != confirm:
            flash("Пароли не совпадают", "error")
            return render_template("register.html")
        user, error = register_user(username, email, password)
        if error:
            flash(error, "error")
            return render_template("register.html")
        session["auth_user_id"] = user["user_id"]
        flash(f"Добро пожаловать, {user['username']}!", "success")
        return redirect(url_for("index"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("auth_user_id"):
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user, error = login_user(username, password)
        if error:
            flash(error, "error")
            return render_template("login.html", next=request.form.get("next", ""))
        session["auth_user_id"] = user["user_id"]
        flash(f"Добро пожаловать, {user['username']}!", "success")
        next_url = request.form.get("next") or url_for("index")
        return redirect(next_url)
    return render_template("login.html", next=request.args.get("next", ""))


@app.route("/logout")
def logout():
    session.pop("auth_user_id", None)
    flash("Вы вышли из системы", "success")
    return redirect(url_for("index"))


# ═══════════════════════════════════════
#  ADMIN ROUTES
# ═══════════════════════════════════════

@app.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    users = get_all_users()
    orders = get_all_orders()
    stats = {
        "total_users": len(users),
        "total_orders": len(orders),
        "total_revenue": sum(o.get("total", 0) for o in orders),
        "paid_orders": sum(1 for o in orders if o.get("status") == "paid"),
    }
    return render_template("admin/dashboard.html", users=users, orders=orders, stats=stats)


@app.route("/admin/users/<user_id>/toggle_admin", methods=["POST"])
@login_required
@admin_required
def admin_toggle_admin(user_id):
    current = get_current_user()
    if user_id == current["user_id"]:
        return jsonify({"error": "Нельзя изменить свои права"}), 400
    target = get_user(user_id)
    if not target:
        return jsonify({"error": "Пользователь не найден"}), 404
    new_val = not target["is_admin"]
    set_admin(user_id, new_val)
    return jsonify({"success": True, "is_admin": new_val, "username": target["username"]})


@app.route("/admin/users/<user_id>/delete", methods=["POST"])
@login_required
@admin_required
def admin_delete_user(user_id):
    current = get_current_user()
    if user_id == current["user_id"]:
        return jsonify({"error": "Нельзя удалить себя"}), 400
    ok = delete_user(user_id)
    if ok:
        return jsonify({"success": True})
    return jsonify({"error": "Нельзя удалить этого пользователя"}), 400


@app.route("/admin/orders/<order_id>/status", methods=["POST"])
@login_required
@admin_required
def admin_update_order_status(order_id):
    from patterns.builder import _orders_store
    new_status = request.get_json().get("status")
    allowed = ["pending", "paid", "shipped", "delivered", "cancelled"]
    if new_status not in allowed:
        return jsonify({"error": "Недопустимый статус"}), 400
    if order_id not in _orders_store:
        return jsonify({"error": "Заказ не найден"}), 404
    _orders_store[order_id]["status"] = new_status
    return jsonify({"success": True, "status": new_status})


# ═══════════════════════════════════════
#  ROUTES – Каталог
# ═══════════════════════════════════════

@app.route("/")
def index():
    products = [p.to_dict() for p in CATALOG]
    return render_template("index.html", products=products)


# ═══════════════════════════════════════
#  ROUTES – Корзина
# ═══════════════════════════════════════

@app.route("/cart")
def cart():
    uid = get_cart_user_id()
    items = cart_manager.get_cart(uid)
    total = cart_manager.cart_total(uid)
    return render_template("cart.html", items=items, total=total, items_json=items)


@app.route("/cart/add/<product_id>", methods=["POST"])
def cart_add(product_id):
    uid = get_cart_user_id()
    product = CATALOG_DICT.get(product_id)
    if not product:
        return jsonify({"error": "Товар не найден"}), 404
    cloned = product.clone()
    cart_manager.add_item(uid, cloned.to_dict())
    return jsonify({
        "message": f"«{product.name}» добавлен в корзину",
        "cart_count": cart_manager.cart_count(uid),
    })


@app.route("/cart/remove/<product_id>", methods=["POST"])
def cart_remove(product_id):
    uid = get_cart_user_id()
    cart_manager.remove_item(uid, product_id)
    return jsonify({
        "cart_count": cart_manager.cart_count(uid),
        "total": int(cart_manager.cart_total(uid)),
    })


@app.route("/cart/update", methods=["POST"])
def cart_update():
    uid = get_cart_user_id()
    data = request.get_json()
    product_id = data["product_id"]
    qty = int(data["quantity"])
    cart_manager.update_quantity(uid, product_id, qty)
    items = cart_manager.get_cart(uid)
    line_total = next(
        (int(i["price"] * i["quantity"]) for i in items if i["product_id"] == product_id), 0
    )
    return jsonify({
        "cart_count": cart_manager.cart_count(uid),
        "total": int(cart_manager.cart_total(uid)),
        "line_total": line_total,
    })


@app.route("/cart/clear", methods=["POST"])
def cart_clear():
    uid = get_cart_user_id()
    cart_manager.clear_cart(uid)
    return redirect(url_for("cart"))


# ═══════════════════════════════════════
#  ROUTES – Оформление заказа
# ═══════════════════════════════════════

@app.route("/checkout")
def checkout():
    uid = get_cart_user_id()
    items = cart_manager.get_cart(uid)
    if not items:
        return redirect(url_for("cart"))

    subtotal = cart_manager.cart_total(uid)

    payment_options = []
    for key, factory in PAYMENT_FACTORIES.items():
        payment_options.append({
            "key": key,
            "name": factory.get_name(),
            "icon": factory.get_icon(),
            "form": factory.create_form().render(),
        })

    total_weight = sum(i.get("weight_kg", 0.5) * i["quantity"] for i in items)
    delivery_options = []
    for key, strategy in DELIVERY_STRATEGIES.items():
        cost = strategy.calculate_cost(total_weight, 15)
        delivery_options.append({
            "key": key,
            "name": strategy.get_name(),
            "description": strategy.get_description(),
            "days": strategy.get_days(),
            "icon": strategy.get_icon(),
            "cost": cost,
        })

    current_user = get_current_user()
    prefill = {}
    if current_user:
        prefill = {"name": current_user["username"], "email": current_user["email"]}

    return render_template(
        "checkout.html",
        items=items,
        subtotal=subtotal,
        payment_options=payment_options,
        delivery_options=delivery_options,
        prefill=prefill,
    )


@app.route("/checkout/validate_coupon", methods=["POST"])
def checkout_validate_coupon():
    code = request.get_json().get("code", "")
    discount = validate_coupon(code)
    if discount:
        return jsonify({"valid": True, "discount_pct": discount, "code": code.upper()})
    return jsonify({"valid": False, "discount_pct": 0})


@app.route("/checkout/submit", methods=["POST"])
def checkout_submit():
    uid = get_cart_user_id()
    data = request.get_json()

    items = cart_manager.get_cart(uid)
    if not items:
        return jsonify({"error": "Корзина пуста"}), 400

    delivery_key = data.get("delivery_method", "courier")
    strategy = get_delivery_strategy(delivery_key)
    total_weight = sum(i.get("weight_kg", 0.5) * i["quantity"] for i in items)
    delivery_cost = strategy.calculate_cost(total_weight, 15)

    extras = data.get("extras", [])
    coupon_code = data.get("coupon_code", "")
    discount_pct = validate_coupon(coupon_code) if coupon_code else 0.0

    base_order_component = BaseOrder(items, delivery_cost)
    decorated = apply_decorators(base_order_component, extras, discount_pct)
    final_total = decorated.get_total()
    order_extras = decorated.get_extras()

    builder = (
        OrderBuilder()
        .set_items(items)
        .set_customer(
            name=data.get("name", "Гость"),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
        )
        .set_delivery(method=delivery_key, address=data.get("address", ""), cost=delivery_cost)
        .set_payment(method=data.get("payment_method", "card"))
    )
    if coupon_code and discount_pct:
        builder.apply_coupon(coupon_code, discount_pct)
    for extra in extras:
        builder.add_decoration(extra)

    order = builder.build()
    order.total = final_total

    payment_method = data.get("payment_method", "card")
    adapter = get_payment_adapter(payment_method)
    payment_result = adapter.process_payment(final_total, data)
    order.status = "paid" if payment_result["success"] else "payment_failed"

    save_order(order)

    notification_service.clear()
    if data.get("email"):
        notification_service.subscribe(EmailObserver(data["email"]))
    if data.get("phone"):
        notification_service.subscribe(SMSObserver(data["phone"]))
    notification_service.subscribe(PushObserver(uid))
    notifications = notification_service.notify("order_placed", {
        "order_id": order.order_id,
        "total": f"{final_total:.2f}",
    })

    cart_manager.clear_cart(uid)

    return jsonify({
        "success": True,
        "order_id": order.order_id,
        "total": final_total,
        "payment": payment_result,
        "notifications": notifications,
        "extras": order_extras,
    })


# ═══════════════════════════════════════
#  ROUTES – Заказы
# ═══════════════════════════════════════

@app.route("/orders")
def orders():
    all_orders = get_all_orders()
    return render_template("orders.html", orders=all_orders)


@app.route("/orders/<order_id>")
def order_detail(order_id):
    order = get_order(order_id)
    if not order:
        return render_template("404.html"), 404
    return render_template("order_detail.html", order=order)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
