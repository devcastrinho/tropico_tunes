from decimal import Decimal

from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import func

from app.extensions import db
from app.models import Category, Coupon, Order, Product, ProductVariant, User
from app.utils.decorators import admin_required


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
ORDER_STATUSES = ["aguardando pagamento", "pagamento aprovado", "preparando pedido", "enviado", "entregue", "cancelado"]


@admin_bp.get("")
@admin_required
def dashboard():
    revenue = db.session.query(func.coalesce(func.sum(Order.total), 0)).filter(Order.status != "cancelado").scalar()
    stats = {
        "products": Product.query.count(),
        "low_stock": ProductVariant.query.filter(ProductVariant.stock <= 5).count(),
        "orders": Order.query.count(),
        "pending": Order.query.filter(Order.status.in_(["aguardando pagamento", "pagamento aprovado"])).count(),
        "customers": User.query.filter_by(role="customer").count(),
        "revenue": revenue,
    }
    recent = Order.query.order_by(Order.created_at.desc()).limit(8).all()
    status_data = db.session.query(Order.status, func.count(Order.id)).group_by(Order.status).all()
    return render_template("admin/dashboard.html", stats=stats, recent=recent, status_data=status_data)


@admin_bp.get("/produtos")
@admin_required
def products():
    return render_template("admin/products.html", products=Product.query.order_by(Product.created_at.desc()).all())


@admin_bp.route("/produtos/novo", methods=["GET", "POST"])
@admin_required
def new_product():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        slug = request.form.get("slug", "").strip().lower()
        category = db.session.get(Category, request.form.get("category_id", type=int))
        if not name or not slug or not category:
            flash("Nome, slug e categoria são obrigatórios.", "error")
        elif Product.query.filter_by(slug=slug).first():
            flash("Este slug já está em uso.", "error")
        else:
            product = Product(name=name, slug=slug, description=request.form.get("description", "").strip(), price=Decimal(request.form.get("price", "0")), category_id=category.id, featured=bool(request.form.get("featured")))
            db.session.add(product)
            db.session.commit()
            flash("Produto criado. Cadastre as variantes de estoque pelo banco ou seed inicial.", "success")
            return redirect(url_for("admin.products"))
    return render_template("admin/product_form.html", categories=Category.query.all())


@admin_bp.post("/produtos/<int:product_id>/status")
@admin_required
def toggle_product(product_id):
    product = db.get_or_404(Product, product_id)
    product.active = not product.active
    db.session.commit()
    flash("Status do produto atualizado.", "success")
    return redirect(url_for("admin.products"))


@admin_bp.get("/estoque")
@admin_required
def inventory():
    variants = ProductVariant.query.join(Product).order_by(Product.name, ProductVariant.stock).all()
    return render_template("admin/inventory.html", variants=variants)


@admin_bp.post("/estoque/<int:variant_id>")
@admin_required
def update_inventory(variant_id):
    variant = db.get_or_404(ProductVariant, variant_id)
    stock = request.form.get("stock", type=int)
    if stock is None or stock < 0:
        flash("Informe uma quantidade válida.", "error")
    else:
        variant.stock = stock
        db.session.commit()
        flash("Estoque atualizado.", "success")
    return redirect(url_for("admin.inventory"))


@admin_bp.get("/pedidos")
@admin_required
def orders():
    return render_template("admin/orders.html", orders=Order.query.order_by(Order.created_at.desc()).all(), statuses=ORDER_STATUSES)


@admin_bp.post("/pedidos/<int:order_id>/status")
@admin_required
def update_order(order_id):
    order = db.get_or_404(Order, order_id)
    status = request.form.get("status")
    if status in ORDER_STATUSES:
        order.status = status
        if order.shipment:
            order.shipment.status = status
        db.session.commit()
        flash("Pedido atualizado.", "success")
    return redirect(url_for("admin.orders"))


@admin_bp.get("/clientes")
@admin_required
def customers():
    return render_template("admin/customers.html", customers=User.query.filter_by(role="customer").order_by(User.created_at.desc()).all())


@admin_bp.get("/cupons")
@admin_required
def coupons():
    return render_template("admin/coupons.html", coupons=Coupon.query.all())


@admin_bp.get("/relatorios")
@admin_required
def reports():
    best_sellers = db.session.query(Product.name, func.coalesce(func.sum(ProductVariant.stock), 0).label("stock")).join(ProductVariant).group_by(Product.id).order_by(func.sum(ProductVariant.stock)).limit(10).all()
    return render_template("admin/reports.html", best_sellers=best_sellers)

