from flask import Flask, render_template, redirect, flash, url_for, request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, ItemForm, LoginForm
from flask_login import UserMixin, login_user, current_user, logout_user
import secrets
import os

from flask_login import LoginManager

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']='postgres://mdbmveudctmurf:a15c90f420dc141c4190c0572ec9af402b5acb13113a72578fab7d57e49aa4ac@ec2-52-205-3-3.compute-1.amazonaws.com:5432/ddn4isnkf5f11b'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
db = SQLAlchemy(app)
login_manager = LoginManager(app)



class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(10), nullable=True)
    description = db.Column(db.String(), nullable = False)
    image =  db.Column (db.String(60), default='default.jpg')
    images =  db.Column (db.PickleType, nullable=True)
    trending = db.Column (db.Boolean, default = False)
    # user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    vendor = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
def __repr__(self): 
    return'<Item %r>' % self.name

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), nullable = False)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(15))
    stock = db.relationship('Item', backref='author', lazy=True)

def __repr__(self):
    return '<User %r' % self.username



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    print(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/items', picture_fn)
    form_picture.save(picture_path)
    print ("The picture name is" + picture_fn)

    return picture_fn



@app.route('/search', methods=['POST'])
def search():
    piw = request.args.get('q')
    print(piw)
    items = Item.query.all()
    # totalitems = Item.query.all().count()
    results = []
    # for i in items:
        # words = i.split()
        # for word in splits:
            # print(word)
    return render_template('results.html', items = items, search = 'iPhone')


@app.route('/', methods=['POST','GET'])
def index():
    items = Item.query.order_by(Item.id.desc()).all()
    user = current_user
    home = 'home'
    return render_template('index.html', items = items, home=home)


@app.route('/preview/<int:itemid>')
def preview(itemid):
    item = Item.query.filter_by(id=itemid).first()
    vendor = User.query.filter_by(id = item.vendor).first()
    vendorname = vendor.username
    images = item.images
    print(images)
    return render_template('preview.html', item=item, vendorname=vendorname, vendor=vendor, images=images)

@app.route('/additem', methods=['POST','GET'])
def additem():
    form = ItemForm()
    if form.validate_on_submit():
        pic = 'default.png'
        if form.picture.data:
            print('YO!!!!!!!!! IT IS OVER HERE!!!')
            pic = save_picture(form.picture.data)
        if form.other_pictures.data:
            for picture in form.other_pictures.data:
                pictures = []
                picture = save_picture(form.picture.data)
                pictures.append(picture)
                print (pictures)
        new_item = Item(name = form.name.data, price = form.price.data, image=pic, description = form.description.data, vendor = current_user.id, images = pictures)
        db.session.add(new_item)
        db.session.commit()
        flash(f'New Item has been added', 'success')
        return redirect(url_for('account'))
    return render_template('addpost.html', form=form)

@app.route('/test', methods=['POST','GET'])
def test():
    return render_template('asdf.html')

# @app.route('/myitems')
# def myitems():

@app.route('/register', methods=['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username = form.username.data, phone = form.phone.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash (f'Account for ' + form.username.data + ' has been created.', 'error') 
        return redirect (url_for('index'))
    return render_template('register.html',  form=form)

@app.route('/account')
def account():
    user = current_user
    return render_template('account.html', user=user)

@app.route('/allusers')
def allusers():
    allusers = User.query.all()
    return render_template('allusers.html', allusers=allusers)

@app.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
         # Login and validate the user.
        # user should be an instance of your `User` class
        user = User.query.filter_by(phone=form.phone.data).first()
        if user and user.password==form.password.data:
            login_user(user)
            print ("Logged in:" + user.username + " " + user.phone)
            print(form.password.data)
            return redirect(url_for('index'))
        else:
            flash(f'Incorrect details, please try again', 'danger')
    return render_template('login.html', form=form)


@app.route('/bookmarks')
def bookmarks():
    return 'Done'

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('/login'))

@app.route('/myitems')
def myitems():
    items = Item.query.filter_by(vendor = current_user.id).all()
    print(items)
    user = current_user
    return render_template('myitems.html' ,items = items, user=user)

if __name__ == '__main__':
    app.run(debug=True)