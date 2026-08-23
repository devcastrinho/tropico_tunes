from datetime import datetime, timezone
from decimal import Decimal

from flask_login import UserMixin
from sqlalchemy import CheckConstraint, Index, UniqueConstraint
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


def utcnow():
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(30))
    role = db.Column(db.String(20), nullable=False, default="customer")
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    addresses = db.relationship("Address", backref="user", cascade="all, delete-orphan")
    orders = db.relationship("Order", backref="customer", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == "admin"


class Address(db.Model):
    __tablename__ = "addresses"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    label = db.Column(db.String(50), default="Principal")
    street = db.Column(db.String(180), nullable=False)
    number = db.Column(db.String(20), nullable=False)
    complement = db.Column(db.String(100))
    neighborhood = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)

    @property
    def formatted(self):
        return f"{self.street}, {self.number} — {self.neighborhood}, {self.city}/{self.state}"


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    slug = db.Column(db.String(90), unique=True, nullable=False, index=True)
    products = db.relationship("Product", backref="category", lazy=True)


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    slug = db.Column(db.String(170), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    featured = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    images = db.relationship("ProductImage", backref="product", cascade="all, delete-orphan", order_by="ProductImage.position")
    variants = db.relationship("ProductVariant", backref="product", cascade="all, delete-orphan")
    reviews = db.relationship("Review", backref="product", cascade="all, delete-orphan")

    @property
    def main_image(self):
        return self.images[0].url if self.images else "https://placehold.co/900x1100/f0ede5/17231c?text=TRÓPICO"

    @property
    def stock(self):
        return sum(v.stock for v in self.variants)


class ProductImage(db.Model):
    __tablename__ = "product_images"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False, index=True)
    url = db.Column(db.String(500), nullable=False)
    alt_text = db.Column(db.String(180))
    position = db.Column(db.Integer, default=0)


class Size(db.Model):
    __tablename__ = "sizes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    sort_order = db.Column(db.Integer, default=0)


class Color(db.Model):
    __tablename__ = "colors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    hex_code = db.Column(db.String(7), nullable=False, default="#000000")


class ProductVariant(db.Model):
    __tablename__ = "product_variants"
    __table_args__ = (
        UniqueConstraint("product_id", "size_id", "color_id", name="uq_product_size_color"),
        CheckConstraint("stock >= 0", name="ck_variant_stock_nonnegative"),
        Index("ix_variant_stock", "stock"),
    )
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False, index=True)
    size_id = db.Column(db.Integer, db.ForeignKey("sizes.id"), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey("colors.id"), nullable=False)
    sku = db.Column(db.String(80), unique=True, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    restock_date = db.Column(db.Date)
    size = db.relationship("Size")
    color = db.relationship("Color")


class Review(db.Model):
    __tablename__ = "reviews"
    __table_args__ = (UniqueConstraint("user_id", "product_id", name="uq_review_user_product"),)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    author = db.relationship("User")


class Cart(db.Model):
    __tablename__ = "carts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    items = db.relationship("CartItem", backref="cart", cascade="all, delete-orphan")

    @property
    def subtotal(self):
        return sum((item.subtotal for item in self.items), Decimal("0.00"))


class CartItem(db.Model):
    __tablename__ = "cart_items"
    __table_args__ = (UniqueConstraint("cart_id", "variant_id", name="uq_cart_variant"),)
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=False, index=True)
    variant_id = db.Column(db.Integer, db.ForeignKey("product_variants.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    variant = db.relationship("ProductVariant")

    @property
    def subtotal(self):
        return self.variant.product.price * self.quantity


class Coupon(db.Model):
    __tablename__ = "coupons"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(40), unique=True, nullable=False, index=True)
    discount_type = db.Column(db.String(20), nullable=False, default="percent")
    value = db.Column(db.Numeric(10, 2), nullable=False)
    valid_until = db.Column(db.DateTime(timezone=True))
    active = db.Column(db.Boolean, default=True, nullable=False)
    max_uses = db.Column(db.Integer)
    used_count = db.Column(db.Integer, default=0, nullable=False)

    def discount_for(self, subtotal):
        if self.discount_type == "percent":
            return (subtotal * self.value / Decimal("100")).quantize(Decimal("0.01"))
        return min(subtotal, self.value)


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    address_text = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(40), default="aguardando pagamento", nullable=False, index=True)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    shipping_cost = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False, index=True)
    items = db.relationship("OrderItem", backref="order", cascade="all, delete-orphan")
    payment = db.relationship("Payment", backref="order", uselist=False, cascade="all, delete-orphan")
    shipment = db.relationship("Shipment", backref="order", uselist=False, cascade="all, delete-orphan")

    @property
    def number(self):
        return f"TRP-{self.id:06d}"


class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False, index=True)
    variant_id = db.Column(db.Integer, db.ForeignKey("product_variants.id"), nullable=False)
    product_name = db.Column(db.String(150), nullable=False)
    size_name = db.Column(db.String(20), nullable=False)
    color_name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    variant = db.relationship("ProductVariant")


class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), unique=True, nullable=False)
    method = db.Column(db.String(40), nullable=False)
    status = db.Column(db.String(30), nullable=False, default="aprovado")
    transaction_reference = db.Column(db.String(100), unique=True, nullable=False)
    installments = db.Column(db.Integer, default=1)
    paid_at = db.Column(db.DateTime(timezone=True), default=utcnow)


class Shipment(db.Model):
    __tablename__ = "shipments"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), unique=True, nullable=False)
    carrier = db.Column(db.String(80), nullable=False, default="Entrega TRÓPICO")
    tracking_code = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(40), default="preparando pedido", nullable=False)
    estimated_delivery = db.Column(db.Date)

