from app import app, db
from flask import render_template, request, redirect, url_for
from sqlalchemy import func
from app.models import Product,Location,ProductMovement

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# View all products
@app.route('/products')
def view_products():
    products = Product.query.all()
    return render_template('products.html', products=products)

# Add a new product
@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_id = request.form['product_id']
        name = request.form['name']
        new_product = Product(product_id=product_id, name=name)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('view_products'))
    return render_template('add_product.html')

# ---- Edit Product ----
@app.route('/products/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return "Product not found", 404
    
    if request.method == 'POST':
        product.name = request.form['name']
        db.session.commit()
        return redirect(url_for('view_products'))
    
    return render_template('edit_product.html', product=product)


# ---- Delete Product ----
@app.route('/products/delete/<product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return "Product not found", 404
    
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('view_products'))

@app.route('/locations')
def view_locations():
    locations = Location.query.all()
    return render_template('locations.html', locations=locations)

# Add a new location
@app.route('/locations/add', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        location_id = request.form['location_id']
        name = request.form['name']
        new_location = Location(location_id=location_id, name=name)
        db.session.add(new_location)
        db.session.commit()
        return redirect(url_for('view_locations'))
    return render_template('add_location.html')

@app.route('/locations/edit/<location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    location = Location.query.get(location_id)
    if not location:
        return "Location not found", 404
    
    if request.method == 'POST':
        location.name = request.form['name']
        db.session.commit()
        return redirect(url_for('view_locations'))
    
    return render_template('edit_location.html', location=location)


@app.route('/locations/delete/<location_id>', methods=['POST'])
def delete_location(location_id):
    location = Location.query.get(location_id)
    if not location:
        return "Location not found", 404
    
    db.session.delete(location)
    db.session.commit()
    return redirect(url_for('view_locations'))

@app.route('/movements')
def view_movements():
    movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    return render_template('movements.html', movements=movements)

# Add a new product movement
@app.route('/movements/add', methods=['GET', 'POST'])
def add_movement():
    from app.models import Product, Location

    products = Product.query.all()
    locations = Location.query.all()

    if request.method == 'POST':
        product_id = request.form['product_id']
        from_location = request.form.get('from_location') or None
        to_location = request.form.get('to_location') or None
        qty = int(request.form['qty'])

        movement = ProductMovement(
            product_id=product_id,
            from_location=from_location,
            to_location=to_location,
            qty=qty
        )
        db.session.add(movement)
        db.session.commit()
        return redirect(url_for('view_movements'))

    return render_template('add_movement.html', products=products, locations=locations)

@app.route('/movements/delete/<int:movement_id>', methods=['POST'])
def delete_movement(movement_id):
    movement = ProductMovement.query.get(movement_id)
    db.session.delete(movement)
    db.session.commit()
    return redirect(url_for('view_movements'))


@app.route('/report')
def inventory_report():
    products = Product.query.all()
    locations = Location.query.all()

    # Dictionary to store balance
    balance = {}

    for product in products:
        for location in locations:
            # Total incoming quantity
            incoming = db.session.query(
                func.coalesce(func.sum(ProductMovement.qty), 0)
            ).filter(
                ProductMovement.product_id == product.product_id,
                ProductMovement.to_location == location.location_id
            ).scalar()

            # Total outgoing quantity
            outgoing = db.session.query(
                func.coalesce(func.sum(ProductMovement.qty), 0)
            ).filter(
                ProductMovement.product_id == product.product_id,
                ProductMovement.from_location == location.location_id
            ).scalar()

            qty = incoming - outgoing
            balance[(product.name, location.name)] = qty

    return render_template('report.html', balance=balance, products=products, locations=locations)

# Edit a product movement
@app.route('/movements/edit/<int:movement_id>', methods=['GET', 'POST'])
def edit_movement(movement_id):
    from app.models import Product, Location, ProductMovement

    movement = ProductMovement.query.get_or_404(movement_id)
    products = Product.query.all()
    locations = Location.query.all()

    if request.method == 'POST':
        movement.product_id = request.form['product_id']
        movement.from_location = request.form.get('from_location') or None
        movement.to_location = request.form.get('to_location') or None
        movement.qty = int(request.form['qty'])

        db.session.commit()
        return redirect(url_for('view_movements'))

    return render_template('edit_movement.html', movement=movement, products=products, locations=locations)
