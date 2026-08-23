from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Cart, CartItem, ProductVariant


cart_bp = Blueprint("cart", __name__, url_prefix="/carrinho")


def get_cart():
    cart = Cart.query.filter_by(user_id=current_user.id, active=True).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
    return cart


@cart_bp.get("")
@login_required
def view_cart():
    return render_template("cart/cart.html", cart=get_cart())


@cart_bp.post("/adicionar")
@login_required
def add():
    variant = db.session.get(ProductVariant, request.form.get("variant_id", type=int))
    quantity = max(1, request.form.get("quantity", 1, type=int))
    if not variant or not variant.product.active:
        flash("Variação inválida.", "error")
    elif variant.stock < quantity:
        flash("Quantidade indisponível em estoque.", "error")
    else:
        cart = get_cart()
        item = CartItem.query.filter_by(cart_id=cart.id, variant_id=variant.id).first()
        desired = quantity + (item.quantity if item else 0)
        if desired > variant.stock:
            flash("Não há estoque suficiente para essa quantidade.", "error")
        else:
            if item:
                item.quantity = desired
            else:
                db.session.add(CartItem(cart_id=cart.id, variant_id=variant.id, quantity=quantity))
            db.session.commit()
            flash("Produto adicionado ao carrinho.", "success")
    return redirect(request.referrer or url_for("cart.view_cart"))


@cart_bp.post("/item/<int:item_id>/atualizar")
@login_required
def update(item_id):
    item = CartItem.query.join(Cart).filter(CartItem.id == item_id, Cart.user_id == current_user.id, Cart.active.is_(True)).first_or_404()
    quantity = request.form.get("quantity", 1, type=int)
    if quantity <= 0:
        db.session.delete(item)
    elif quantity <= item.variant.stock:
        item.quantity = quantity
    else:
        flash("Quantidade maior que o estoque disponível.", "error")
        return redirect(url_for("cart.view_cart"))
    db.session.commit()
    flash("Carrinho atualizado.", "success")
    return redirect(url_for("cart.view_cart"))


@cart_bp.post("/item/<int:item_id>/remover")
@login_required
def remove(item_id):
    item = CartItem.query.join(Cart).filter(CartItem.id == item_id, Cart.user_id == current_user.id, Cart.active.is_(True)).first_or_404()
    db.session.delete(item)
    db.session.commit()
    flash("Item removido.", "info")
    return redirect(url_for("cart.view_cart"))

