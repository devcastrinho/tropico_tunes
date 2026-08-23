from datetime import date, timedelta
from decimal import Decimal

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Cart, Coupon, Order, OrderItem, Payment, Shipment
from app.services.payment import SimulatedPaymentGateway
from app.services.shipping import SimulatedShippingService


orders_bp = Blueprint("orders", __name__)


def active_cart():
    return Cart.query.filter_by(user_id=current_user.id, active=True).first()


@orders_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    cart = active_cart()
    if not cart or not cart.items:
        flash("Seu carrinho está vazio.", "info")
        return redirect(url_for("shop.catalog"))
    if not current_user.addresses:
        flash("Cadastre um endereço antes de continuar.", "info")
        return redirect(url_for("auth.profile"))

    address_id = request.form.get("address_id", current_user.addresses[0].id, type=int)
    address = next((a for a in current_user.addresses if a.id == address_id), current_user.addresses[0])
    shipping = SimulatedShippingService().quote(address.zip_code, cart.subtotal)
    coupon = None
    discount = Decimal("0.00")
    coupon_code = request.form.get("coupon", "").strip().upper()
    if coupon_code:
        coupon = Coupon.query.filter_by(code=coupon_code, active=True).first()
        if coupon and (coupon.max_uses is None or coupon.used_count < coupon.max_uses):
            discount = coupon.discount_for(cart.subtotal)
        else:
            coupon = None
            flash("Cupom inválido ou esgotado.", "error")
    total = cart.subtotal - discount + shipping.price

    if request.method == "POST" and request.form.get("action") == "finish":
        for item in cart.items:
            if item.quantity > item.variant.stock:
                flash(f"Estoque insuficiente para {item.variant.product.name}.", "error")
                return redirect(url_for("cart.view_cart"))
        method = request.form.get("payment_method", "")
        result = SimulatedPaymentGateway().charge(method)
        if not result.approved:
            flash("Forma de pagamento inválida.", "error")
            return redirect(url_for("orders.checkout"))
        order = Order(
            user_id=current_user.id,
            address_text=address.formatted,
            status="pagamento aprovado",
            subtotal=cart.subtotal,
            discount=discount,
            shipping_cost=shipping.price,
            total=total,
        )
        db.session.add(order)
        db.session.flush()
        for item in cart.items:
            variant = item.variant
            variant.stock -= item.quantity
            db.session.add(OrderItem(order_id=order.id, variant_id=variant.id, product_name=variant.product.name, size_name=variant.size.name, color_name=variant.color.name, quantity=item.quantity, unit_price=variant.product.price))
        db.session.add(Payment(order_id=order.id, method=method, status=result.status, transaction_reference=result.reference, installments=max(1, request.form.get("installments", 1, type=int))))
        db.session.add(Shipment(order_id=order.id, estimated_delivery=date.today() + timedelta(days=shipping.business_days)))
        if coupon:
            coupon.used_count += 1
        cart.active = False
        db.session.commit()
        flash("Pagamento aprovado e pedido confirmado!", "success")
        return redirect(url_for("orders.order_detail", order_id=order.id))

    return render_template("orders/checkout.html", cart=cart, address=address, shipping=shipping, coupon=coupon, discount=discount, total=total)


@orders_bp.get("/pedidos")
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template("orders/list.html", orders=orders)


@orders_bp.get("/pedidos/<int:order_id>")
@login_required
def order_detail(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template("orders/detail.html", order=order)

