from flask import Flask, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, ItemForm
import secrets
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(10), nullable=True)
    description = db.Column(db.String(), nullable = False)
    image =  db.Column (db.String(60), default='default.jpg')
    trending = db.Column (db.Boolean, default = False)
    # user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    
def __repr__(self): 
    return'<Item %r>' % self.name

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), nullable = False)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(15))

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


@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items = items)

@app.route('/preview/<int:itemid>')
def preview(itemid):
    item = Item.query.filter_by(id=itemid).first()
    return render_template('preview.html',item=item)

@app.route('/additem', methods=['POST','GET'])
def additem():
    form = ItemForm()
    if form.validate_on_submit():
        pic = 'default.png'
        if form.picture.data:
            print('YO!!!!!!!!! IT IS OVER HERE!!!')
            pic = save_picture(form.picture.data)
        new_item = Item(name = form.name.data, price = form.price.data, image=pic, description = form.description.data)
        db.session.add(new_item)
        db.session.commit()
        flash(f'New Item has been added', 'success')
    return render_template('addpost.html', form=form)


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

if __name__ == '__main__':
    app.run(debug=True)