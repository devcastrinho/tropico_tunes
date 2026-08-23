from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

import click

from .extensions import db
from .models import Address, Category, Color, Coupon, Product, ProductImage, ProductVariant, Size, User


PRODUCTS = [
    ("Camiseta Sol Nascente", "camiseta-sol-nascente", "Camisetas", "Algodão premium, modelagem ampla e estampa solar.", "149.90", True, "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=900&q=80"),
    ("Camiseta Mata Atlântica", "camiseta-mata-atlantica", "Camisetas", "Malha encorpada com tingimento verde profundo.", "159.90", True, "https://images.unsplash.com/photo-1503341504253-dff4815485f1?auto=format&fit=crop&w=900&q=80"),
    ("Moletom Horizonte", "moletom-horizonte", "Moletons", "Moletom felpado oversized para noites tropicais.", "329.90", True, "https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=900&q=80"),
    ("Calça Cargo Cerrado", "calca-cargo-cerrado", "Calças", "Sarja resistente e bolsos utilitários.", "289.90", True, "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?auto=format&fit=crop&w=900&q=80"),
    ("Short Orla", "short-orla", "Shorts", "Leve, funcional e pronto para o calor.", "189.90", False, "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?auto=format&fit=crop&w=900&q=80"),
    ("Jaqueta Chuva de Verão", "jaqueta-chuva-verao", "Jaquetas", "Corta-vento compacto com acabamento repelente.", "399.90", False, "https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?auto=format&fit=crop&w=900&q=80"),
    ("Boné Brisa", "bone-brisa", "Acessórios", "Boné de seis painéis com bordado minimalista.", "119.90", False, "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?auto=format&fit=crop&w=900&q=80"),
    ("Camisa Amazônia", "camisa-amazonia", "Camisas", "Viscose fluida com padronagem botânica discreta.", "249.90", False, "https://images.unsplash.com/photo-1603252109303-2751441dd157?auto=format&fit=crop&w=900&q=80"),
    ("Regata Maré", "regata-mare", "Camisetas", "Regata canelada de algodão brasileiro.", "109.90", False, "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?auto=format&fit=crop&w=900&q=80"),
    ("Ecobag Raízes", "ecobag-raizes", "Acessórios", "Lona de algodão com alças reforçadas.", "79.90", False, "https://images.unsplash.com/photo-1597484662317-9bd7bdda2907?auto=format&fit=crop&w=900&q=80"),
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

