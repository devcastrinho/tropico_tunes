import unittest
from decimal import Decimal

from app import create_app
from app.cli import sync_catalog
from app.extensions import db
from app.models import Category, Product, ProductImage, User
from config import TestConfig


class CatalogSyncTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def test_updates_catalog_without_removing_users(self):
        category = Category(name="Moletons", slug="moletons")
        user = User(name="Cliente", email="cliente@example.com")
        user.set_password("senha-segura")
        product = Product(
            name="Moletom Horizonte",
            slug="moletom-horizonte",
            category=category,
            description="Descrição antiga.",
            price=Decimal("329.90"),
            featured=True,
        )
        product.images.append(ProductImage(url="https://example.com/antiga.jpg", alt_text=product.name))
        db.session.add_all([user, product])
        db.session.commit()

        updated = sync_catalog()
        db.session.commit()

        synced = Product.query.filter_by(slug="moletom-horizonte").one()
        self.assertEqual(updated, 1)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(synced.name, "Moletom Preto TROPICO")
        self.assertEqual(synced.main_image, "/static/images/products/moletom-horizonte.png")


if __name__ == "__main__":
    unittest.main()
