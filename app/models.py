from app import db
from datetime import datetime

class Product(db.Model):
    product_id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Product {self.name}>"

class Location(db.Model):
    location_id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Location {self.name}>"

class ProductMovement(db.Model):
    movement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    from_location = db.Column(db.String(20), db.ForeignKey('location.location_id'), nullable=True)
    to_location = db.Column(db.String(20), db.ForeignKey('location.location_id'), nullable=True)
    product_id = db.Column(db.String(20), db.ForeignKey('product.product_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    product = db.relationship('Product', backref='movements')
    from_loc = db.relationship('Location', foreign_keys=[from_location])
    to_loc = db.relationship('Location', foreign_keys=[to_location])

    def __repr__(self):
        return f"<Movement {self.product_id} ({self.qty})>"
