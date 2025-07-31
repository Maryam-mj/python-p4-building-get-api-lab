#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'


# -------------------------
# GET /bakeries
# -------------------------
@app.route('/bakeries', methods=['GET'])
def bakeries():
    """Return all bakeries as JSON"""
    all_bakeries = Bakery.query.all()
    bakery_list = [bakery.to_dict() for bakery in all_bakeries]
    return jsonify(bakery_list), 200


# -------------------------
# GET /bakeries/<int:id>
# Returns a single bakery with its baked goods nested
# -------------------------
@app.route('/bakeries/<int:id>', methods=['GET'])
def bakery_by_id(id):
    """Return a single bakery and its baked goods"""
    bakery = Bakery.query.get_or_404(id)

    # Convert to dict and include baked goods list
    bakery_data = bakery.to_dict()
    bakery_data['baked_goods'] = [bg.to_dict() for bg in bakery.baked_goods]

    return jsonify(bakery_data), 200


# -------------------------
# GET /baked_goods/by_price
# Returns baked goods sorted by price (descending)
# -------------------------
@app.route('/baked_goods/by_price', methods=['GET'])
def baked_goods_by_price():
    """Return baked goods sorted by price descending"""
    goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    goods_list = [good.to_dict() for good in goods]
    return jsonify(goods_list), 200


# -------------------------
# GET /baked_goods/most_expensive
# Returns the single most expensive baked good
# -------------------------
@app.route('/baked_goods/most_expensive', methods=['GET'])
def most_expensive_baked_good():
    """Return the single most expensive baked good"""
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()

    # Handle case if no baked goods exist
    if most_expensive:
        return jsonify(most_expensive.to_dict()), 200
    return jsonify({'message': 'No baked goods found'}), 404


if __name__ == '__main__':
    app.run(port=5555, debug=True)
