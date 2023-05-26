from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(15), unique=False, nullable=False)
    
    
     # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self): # line 37
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    # Required for administrative interface
    def __unicode__(self):
        return self.username


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=False, nullable=False)
    phone = db.Column(db.String(15), unique=False, nullable=False)
    message = db.Column(db.String(250), unique=False, nullable=False)



class Subcriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), unique=False, nullable=False)