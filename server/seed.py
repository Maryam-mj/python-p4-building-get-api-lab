from app import app
from models import db, Bakery, BakedGood

with app.app_context():
    # Clear any existing data
    BakedGood.query.delete()
    Bakery.query.delete()

    # Create bakeries
    b1 = Bakery(name="Sweet Treats")
    b2 = Bakery(name="Golden Crust")
    db.session.add_all([b1, b2])
    db.session.commit()

    # Create baked goods
    g1 = BakedGood(name="Chocolate Cake", price=15.0, bakery_id=b1.id)
    g2 = BakedGood(name="Blueberry Muffin", price=5.0, bakery_id=b1.id)
    g3 = BakedGood(name="Croissant", price=7.5, bakery_id=b2.id)

    db.session.add_all([g1, g2, g3])
    db.session.commit()

    print("✅ Database seeded with bakeries and baked goods!")
