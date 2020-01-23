# pylint: disable=missing-function-docstring
from flask import Flask, make_response, request, abort
from config import Config
app = Flask(__name__)
app.config.from_object(Config)


from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)
from models import Product
from schemas import product_schema, products_schema

@app.route('/hello')
def hello():
    return "Hello World!"

def init_product_list():
    skello = Product()
    skello.name = "Skello"
    socialive = Product()
    socialive.name = "Socialive.tv"
    db.session.query(Product).delete()
    db.session.add(skello)
    db.session.add(socialive)
    db.session.commit()

@app.route('/products')
def products_list():
    products = db.session.query(Product).all()
    response = make_response(products_schema.jsonify(products), 200)
    return response

@app.route('/products/<int:product_id>', methods=['Get'])
def get_product(product_id):
    products = db.session.query(Product).get(product_id)
    response = make_response(product_schema.jsonify(products), 200)
    return response

@app.route('/products', methods=['Post'])
def create_product():
    body = request.get_json()
    if not "name" in body or body["name"] is None:
        abort(422)
    new_product = Product()
    new_product.name = body["name"]
    db.session.add(new_product)
    db.session.commit()
    response = make_response("", 204)
    return response

@app.route('/products/<int:product_id>', methods=['Patch'])
def update_product(product_id):
    body = request.get_json()
    product = db.session.query(Product).get(product_id)
    if not product:
        abort(404)
    if not "name" in body or body["name"] is None:
        abort(422)
    product.name = body["name"]
    db.session.commit()
    response = make_response("", 204)
    return response

@app.route('/products/<int:product_id>', methods=['Delete'])
def delete_product(product_id):
    product = db.session.query(Product).get(product_id)
    if not product:
        abort(404)
    db.session.delete(product)
    db.session.commit()
    response = make_response("", 204)
    return response
