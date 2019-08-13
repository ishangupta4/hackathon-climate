from datetime import datetime
from flaskapp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class NGO(db.Model):
    address = db.Column(db.String(400), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    contact_number = db.Column(db.Integer, nullable=False)
    contact_email = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    history = db.relationship('Transfer_history', backref='NGO', lazy=True)

    def __repr__(self):
        return f"NGO('{self.name}','{self.address}','{self.contact_email}','{self.contact_number}')"

    def is_NGO(current_user_id):
        if current_user_id == user_id:
            return True
        else:
            return False

class Donor(db.Model):
    name = db.Column(db.String(40), nullable=False)
    contact_number = db.Column(db.Integer, nullable=False)
    contact_email = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    history = db.relationship('Transfer_history', backref='donor', lazy=True)

    def is_Donor(current_user_id):
        if current_user_id == user_id:
            return True
        else:
            return False

    def __repr__(self):
        return f"Donor('{self.name}','{self.contact_email}','{self.contact_number}')"

class Carrier(db.Model):
    name = db.Column(db.String(40), nullable=False)
    contact_number = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    history = db.relationship('Transfer_history', backref='carrier', lazy=True)

    def is_carrier(current_user_id):
        if current_user_id == user_id:
            return True
        else:
            return False

    def __repr__(self):
        return f"Carrier('{self.name}','{self.contact_number}')"

class Transfer_history(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_of_delivery = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    NGO_id = db.Column(db.Integer, db.ForeignKey('NGO.user_id'), nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('donor.user_id'), nullable=False)
    carrier_id = db.Column(db.Integer, db.ForeignKey('carrier.user_id'), nullable=False)

    def __repr__(self):
        return f"Transfer_history('{self.NGO_id}','{self.donor_id}','{self.carrier_id}')"