# pylint: disable=missing-function-docstring
from flask import Flask, make_response, request, abort, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import Config
app = Flask(__name__)
app.config.from_object(Config)


from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)
from models import Product
from schemas import product_schema, products_schema

admin = Admin(app, template_mode='bootstrap3')
admin.add_view(ModelView(Product, db.session))

@app.route('/')
def home():
    products = db.session.query(Product).all()
    return render_template('home.html', products=products)

@app.route('/products')
def products():
    products = db.session.query(Product).all()
    return render_template('home.html', products=products)

@app.route('/<int:id>')
def product_html(id):
    product = db.session.query(Product).get(id)
    return render_template('product.html', product=product)

@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/api/v1/products')
def products_list():
    products = db.session.query(Product).all()
    response = make_response(products_schema.jsonify(products), 200)
    return response

@app.route('/api/v1/products/<int:product_id>', methods=['Get'])
def get_product(product_id):
    product = db.session.query(Product).get(product_id)
    if not product:
        abort(404)
    response = make_response(product_schema.jsonify(product), 200)
    return response

@app.route('/api/v1/products', methods=['Post'])
def create_product():
    body = request.get_json()
    if not "name" in body or body["name"] is None:
        abort(422)
    new_product = Product()
    new_product.name = body["name"]
    db.session.add(new_product)
    db.session.commit()
    response = make_response(product_schema.jsonify(new_product), 201)
    return response

@app.route('/api/v1/products/<int:product_id>', methods=['Patch'])
def update_product(product_id):
    body = request.get_json()
    product = db.session.query(Product).get(product_id)
    if not product:
        abort(404)
    if not "name" in body or body["name"] is None or body["name"] == "":
        abort(422)
    product.name = body["name"]
    db.session.commit()
    response = make_response("", 204)
    return response

@app.route('/api/v1/products/<int:product_id>', methods=['Delete'])
def delete_product(product_id):
    product = db.session.query(Product).get(product_id)
    if not product:
        abort(404)
    db.session.delete(product)
    db.session.commit()
    response = make_response("", 204)
    return response
