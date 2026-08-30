from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

import click

from .extensions import db
from .models import Address, Category, Color, Coupon, Product, ProductImage, ProductVariant, Size, User


PRODUCTS = [
    ("Camiseta Preta TROPICO", "camiseta-sol-nascente", "Camisetas", "Camiseta preta em algodão, com logo TROPICO aplicado no peito.", "149.90", True, "/static/images/products/camiseta-sol-nascente.jpeg"),
    ("Camiseta Branca TROPICO", "camiseta-mata-atlantica", "Camisetas", "Camiseta branca em algodão, com logo TROPICO aplicado no peito.", "159.90", True, "/static/images/products/camiseta-mata-atlantica.jpeg"),
    ("Moletom Preto TROPICO", "moletom-horizonte", "Moletons", "Moletom preto felpado com capuz, bolso canguru e logo TROPICO.", "329.90", True, "/static/images/products/moletom-horizonte.png"),
    ("Calça Cargo Preta", "calca-cargo-cerrado", "Calças", "Calça cargo preta de modelagem ampla, com bolsos utilitários.", "289.90", True, "/static/images/products/calca-cargo-cerrado.jpeg"),
    ("Short Street", "short-orla", "Shorts", "Short leve e funcional para o dia a dia.", "189.90", False, "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?auto=format&fit=crop&w=900&q=80"),
    ("Corta-Vento Preto TROPICO", "jaqueta-chuva-verao", "Jaquetas", "Corta-vento preto com capuz, acabamento repelente e logo TROPICO.", "399.90", False, "/static/images/products/jaqueta-chuva-verao.jpeg"),
    ("Boné Preto", "bone-brisa", "Acessórios", "Boné preto de seis painéis com acabamento estonado.", "119.90", False, "/static/images/products/bone-brisa.jpeg"),
    ("Camisa Casual", "camisa-amazonia", "Camisas", "Camisa casual em viscose leve e confortável.", "249.90", False, "https://images.unsplash.com/photo-1603252109303-2751441dd157?auto=format&fit=crop&w=900&q=80"),
    ("Regata Branca TROPICO", "regata-mare", "Camisetas", "Regata branca em algodão, com logo TROPICO aplicado no peito.", "109.90", False, "/static/images/products/regata-mare.jpeg"),
    ("Ecobag TROPICO", "ecobag-raizes", "Acessórios", "Ecobag em lona de algodão cru, com estampa frontal TROPICO.", "79.90", False, "/static/images/products/ecobag-raizes.jpeg"),
]


def register_commands(app):
    @app.cli.command("seed")
    @click.option("--reset", is_flag=True, help="Recria todas as tabelas.")
    def seed(reset):
        if reset:
            db.drop_all()
        db.create_all()
        if User.query.first():
            click.echo("O banco já possui dados.")
            return
        admin = User(name="Admin TRÓPICO", email="admin@tropico.com.br", role="admin", phone="11999990000")
        admin.set_password("Admin@123")
        customer = User(name="Cliente Demo", email="cliente@tropico.com.br", phone="11988887777")
        customer.set_password("Cliente@123")
        db.session.add_all([admin, customer])
        db.session.flush()
        db.session.add(Address(user_id=customer.id, street="Rua das Palmeiras", number="100", neighborhood="Jardins", city="São Paulo", state="SP", zip_code="01400-000"))
        categories = {}
        for name in sorted({row[2] for row in PRODUCTS}):
            category = Category(name=name, slug=name.lower().replace("ó", "o").replace("é", "e").replace(" ", "-"))
            db.session.add(category)
            categories[name] = category
        sizes = [Size(name=name, sort_order=i) for i, name in enumerate(["P", "M", "G", "GG"])]
        colors = [Color(name="Preto", hex_code="#171717"), Color(name="Off-white", hex_code="#EDE9DF"), Color(name="Verde Mata", hex_code="#244A35")]
        db.session.add_all(sizes + colors)
        db.session.flush()
        for index, (name, slug, category_name, description, price, featured, image) in enumerate(PRODUCTS):
            product = Product(name=name, slug=slug, category_id=categories[category_name].id, description=description, price=Decimal(price), featured=featured)
            product.images.append(ProductImage(url=image, alt_text=name))
            db.session.add(product)
            db.session.flush()
            for size in sizes:
                for color in colors:
                    product.variants.append(ProductVariant(size_id=size.id, color_id=color.id, sku=f"TRP-{index+1:02d}-{size.name}-{color.id}", stock=3 + ((index + size.id + color.id) % 12)))
        db.session.add(Coupon(code="BEMVINDO10", discount_type="percent", value=10, active=True, max_uses=500, valid_until=datetime.now(timezone.utc) + timedelta(days=365)))
        db.session.commit()
        click.echo("Dados criados. Admin: admin@tropico.com.br / Admin@123")
