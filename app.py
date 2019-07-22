## Use this as our entry-point
from flask import Flask, request,render_template_string, jsonify #Jsonify allows us to take python dicts into json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
import os 

#init our app
app = Flask(__name__)

#Get our DB file/URI
basedir= os.path.abspath(os.path.dirname(__file__)) #This is our base/current directory from this file
#Configs the app to have the DB attached that will be looked for in the base dir and named 'db.sqlite' 
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///'+os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Stop the console yelling about modifications

#Initialize the DB
db = SQLAlchemy(app)

#Init Marsh
ma = Marshmallow(app)

#Make a Model/Class #db  is our SQLAlchemy and Model that gives us some predefined methods
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True) #Making a id field using db.Column(dataType, PrimaryKey?, Autoincrement?, Limit?...)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    #Our initializer/constructor
    #When the params are passed in, ass it to the instance
    def __init__(self, name, description, price,qty):
        self.name=name
        self.description=description
        self.price=price
        self.qty=qty

# Product Schema:Blueprint specifying what fields will be present
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name','description','price','qty')
# Init our schema               #Avoid warning
product_schema = ProductSchema(strict=True) #Single product
products_schema = ProductSchema(many=True, strict=True)

# Create a Product
@app.route('/product',methods=['POST'])
#Grab the data that is being sent int (ie react or postman etc)
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty) #Instantiate the product

    db.session.add(new_product) #Add the product to this session

    db.session.commit() #Commit this session to our db to store the new record
    print(product_schema)
    print(new_product) #
    result = product_schema.dump(new_product)
    return jsonify(result.data) #Send back a json representation of our new product!
    
# Get all products

@app.route('/product', methods=["GET"])
def get_products():
    all_products= Product.query.all() #This gives us back all the Products (thank you SQLAlchemy)
    result = products_schema.dump(all_products) #Dump all the products, raw parsing
    return jsonify(result.data) #Json representation of the result's data


# Get single product, angle bracket gives us a var
@app.route('/product/<id>', methods=["GET"])
def get_product(id):
    product= Product.query.get(id) #This gives us back the product that matches the id given (thank you SQLAlchemy)
    return product_schema.jsonify(product) #Json representation of the result's data


# Update a product
#We need to know what product, so we need the ID 
# Use the PUT verb for updating
@app.route('/product/<id>',methods=['PUT'])
def update_product(id):
    product = Product.query.get(id) #Get the product by id

    #Grab the request's data
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    #Build out the product with updated info
    product.name=name
    product.description=description
    product.price=price
    product.qty=qty

    db.session.commit() #Commit this session to our db to store the new record

    return product_schema.jsonify(product) #Send back a json representation of our new product!
    

# Delete a product/record
@app.route('/product/<id>', methods=["DELETE"])
def delete_product(id):
    product= Product.query.get(id) #This gives us back the product that matches the id given (thank you SQLAlchemy)
    db.session.delete(product) #delete the product
    db.session.commit() #Save the actions taken
    return product_schema.jsonify(product) #Json representation of the result's data


@app.route('/', methods=['GET'])
def get():
    return jsonify({'msg':'hello, world'})

#Run the server --> Uncomment if you want to run the module directly via a `python app.py` command
# if __name__ =='__main__':
#     app.run(debug=True)