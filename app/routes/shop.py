from sqlalchemy import or_
from flask import Blueprint, render_template, request

from app.models import Category, Product


shop_bp = Blueprint("shop", __name__)


@shop_bp.get("/")
def home():
    featured = Product.query.filter_by(active=True, featured=True).limit(4).all()
    newest = Product.query.filter_by(active=True).order_by(Product.created_at.desc()).limit(4).all()
    return render_template("shop/home.html", featured=featured, newest=newest, categories=Category.query.all())


@shop_bp.get("/produtos")
def catalog():
    query = Product.query.filter_by(active=True)
    search = request.args.get("q", "").strip()
    category = request.args.get("categoria", "").strip()
    if search:
        query = query.filter(or_(Product.name.ilike(f"%{search}%"), Product.description.ilike(f"%{search}%")))
    if category:
        query = query.join(Category).filter(Category.slug == category)
    order = request.args.get("ordem", "recentes")
    if order == "menor-preco":
        query = query.order_by(Product.price.asc())
    elif order == "maior-preco":
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.created_at.desc())
    return render_template("shop/catalog.html", products=query.all(), categories=Category.query.all(), search=search)


@shop_bp.get("/produto/<slug>")
def product_detail(slug):
    product = Product.query.filter_by(slug=slug, active=True).first_or_404()
    related = Product.query.filter(Product.category_id == product.category_id, Product.id != product.id, Product.active.is_(True)).limit(4).all()
    return render_template("shop/product.html", product=product, related=related)

