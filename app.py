from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from migrations.models import *
from flask_login import LoginManager, login_user, logout_user, login_required

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b']\xaa<\x91\xfe\xe95\x94'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

# initialize the app with the extension
db.init_app(app)


with app.app_context():
    db.create_all()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



#  ================== Authentication ======================

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    try:
        if request.method == 'POST':
            name = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(name=name).first()

            if user:
                if check_password_hash(user.password, password):
                    login_user(user)
                    return redirect(url_for('admin_panel'))
                else:
                    flash('Please check your login details and try again.')
                    return redirect(url_for('admin'))
            else:
                flash('User Does not exist \n Create an account')
                return redirect(url_for('register_admin'))
    except Exception as e:
        return render_template("error.html", error=e)
    return render_template("admin-views/admin.html")


@app.route("/subscribers")
@login_required
def subscribers():
    list_subscriber = Subcriber.query.all()
    return render_template("admin-views/subscriber.html", list_subscriber=list_subscriber)


@app.route("/admin-panel", methods=['GET', 'POST'])
@login_required
def admin_panel():
    contact_list = Contact.query.all()

    return render_template("admin-views/admin-panel.html", contact=contact_list)


@app.route("/register-subscribe", methods=['POST'])
def add_subscribe():
    try:
        if not request.form['email']:
            flash('Please enter Email Address to Subscribe', 'error')
            return redirect(url_for('contact'))
        else:
            subscriber = Subcriber(email=request.form['email'])

            db.session.add(subscriber)
            db.session.commit()

            flash('Subscribe Successfully! you will be notify about new updates.')
            return redirect(url_for('contact'))
    except Exception as e:
        return render_template("error.html", error=e)


@app.route("/register-admin", methods=['GET', 'POST'])
def register_admin():
    try:
        if request.method == 'POST':
            user = User.query.filter_by(email=request.form['username']).first()
            # if this returns a user, then the email already exists in database
            if user:
                # if a user is found, we want to redirect back to signup page so user can try again
                flash('User Already Register with this username try other')
                return redirect(url_for('auth.signup'))

            if not request.form['username'] or not request.form['email'] or not request.form['password']:
                flash('Please enter all the fields', 'error')
            else:
                admin = User(
                    name=request.form['username'],
                    email=request.form['email'],
                    password=generate_password_hash(
                        request.form['password'], method='sha256'),
                )
                db.session.add(admin)
                db.session.commit()

                flash('Account Created Login Here with username')
                return redirect(url_for('admin'))

        return render_template("admin-views/register-admin.html")
    except Exception as e:
        return render_template("error.html", error=e)


@app.route("/logout")
@login_required
def logout():
    try:
        logout_user()
        flash("Logout Successfully!")
        return redirect(url_for('admin'))
    except Exception as e:
        return render_template("error.html", error=e)

#  ================== Services ======================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/error")
def error():
    return render_template("error.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/client")
def client():
    return render_template("client.html")


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        if not request.form['Name'] or not request.form['Email'] or not request.form['Phone'] or not request.form['Message']:
            flash('Please enter all the fields', 'error')
        else:      
            contact = Contact(
                name=request.form['Name'],
                email=request.form['Email'],
                phone=request.form['Phone'],
                message=request.form['Message'])

            db.session.add(contact)
            db.session.commit()

        flash('Record was successfully added')
        return redirect(url_for('contact'))
    return render_template("contact.html")


@app.route("/service")
def service():
    return render_template("service.html")


@app.route("/team")
def team():
    return render_template("team.html")


# main driver function
if __name__ == '__main__':
    app.run(debug=True)
