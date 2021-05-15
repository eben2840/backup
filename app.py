import secrets
import os
import urllib.request, urllib.parse
import urllib
from flask import Flask, render_template, redirect, flash, url_for, request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, ItemForm, LoginForm, Search
from flask_login import UserMixin, login_user, current_user, logout_user
from flask_login import LoginManager

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']='postgres://mdbmveudctmurf:a15c90f420dc141c4190c0572ec9af402b5acb13113a72578fab7d57e49aa4ac@ec2-52-205-3-3.compute-1.amazonaws.com:5432/ddn4isnkf5f11b'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
# app.config['SQLALCHEMY_DATABASE_URI']='postgres://mdbmveudctmurf:a15c90f420dc141c4190c0572ec9af402b5acb13113a72578fab7d57e49aa4ac@ec2-52-205-3-3.compute-1.amazonaws.com:5432/ddn4isnkf5f11b'
app.config['SECRET_KEY'] = '5791628b21sb13ce0c676dfde280ba245'
db = SQLAlchemy(app)
login_manager = LoginManager(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(10), nullable=True)
    description = db.Column(db.String(), nullable = False)
    image =  db.Column (db.String(60), default='default.jpg')
    trending = db.Column (db.Boolean, default = False)
    category = db.Column(db.String(), nullable=False)
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


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

def __repr__(self):
    return '<Category %r' % self.name


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


@app.route("/searchal/<string:search>", methods=['POST','GET'])
def searchal(search):
    search = search
    items = Item.query.filter_by(name = search).all()
    print(items)
    return render_template('searchal.html', search=search, items=items)

# def replace_all(text, dic):
#     for i, j in dic.iteritems():
#         text = text.replace(i, j)
#     return text


def search(searchquery):
    items = Item.query.all()
    search = searchquery.split()
    foundItems = []
    print(items)
    print(search)
    for s in range(len(search)):
        # This is the word in the search bar
        print(search[s])
        for i in range(len(items)):
            print("Searching for " + search[s] + " in " + items[i].name)
            # Picks a specific item from the Database
            item_string = str(items[i].name.split()).lower()
            itemsArray = items[i].name.split()
            print(item_string)
            # Counts how many words are in that list
            item_string_count = len(items[i].name.split())
            print(item_string_count)
            # Good Code
            if item_string_count != 1:
                print("More than 1 word: " + str(item_string))
                for c in range(item_string_count):
                    item_sub_string = itemsArray[c].lower()
                    item_sub_string = item_sub_string.replace("[", "")
                    item_sub_string = item_sub_string.replace("'", "")
                    item_sub_string = item_sub_string.replace("]", "")
                    print("Item Sub String: " + item_sub_string)
                    if search[s] == item_sub_string:
                        print("found")
                        print(items[i].id)
                        foundItems.append(items[i].id)
            else:
                print("It is one word")
                item_string = item_string.replace("[", "")
                item_string = item_string.replace("'", "")
                item_string = item_string.replace("]", "")
                if search[s] == item_string:
                    print("found")
                    print(items[i].id)
                    foundItems.append(items[i].id)
                    print("We found the ff:" + str(foundItems))
            # End of Good code

            # else:
            #     print(type(search[s]))
            #     print(len(search[s]))
            #     print(type(str(items[i].name.split())))
            #     print(len(str(items[i].name.split())))
            #     res = str(items[i].name.split())    
            #     x = res.replace("[", "")
            #     y = x.replace("'", "")
            #     z = y.replace("]", "")
            #     print("Not found")
                # print(items[i].name.split())
    return foundItems

searchResults = []
queryResult = search('iphone')
print("Found" + str(queryResult))
for f in queryResult:
    item = Item.query.get_or_404(f)
    searchResults.append(item)
    print(searchResults)





@app.route('/', methods=['POST','GET'])
def index():
    form = Search()
    items = Item.query.order_by(Item.id.desc()).all()
    # items = Item.query.all().order_by()
    user = current_user
    home = 'home'
    if form.validate_on_submit():
        search = form.search.data
        return redirect(url_for('searchal', search = search))
    return render_template('index.html', items = items, home=home, form=form)


@app.route('/testing')
def testing():
    return render_template('grid.html')


@app.route('/preview/<int:itemid>')
def preview(itemid):
    item = Item.query.filter_by(id=itemid).first()
    vendor = User.query.filter_by(id = item.vendor).first()
    vendorname = vendor.username
    return render_template('preview.html', item=item, vendorname=vendorname, vendor=vendor)

@app.route('/show/<string:category>')
def show(category):
    items = Item.query.filter_by(category = category).all()
    print(items)
    return render_template('show.html', items=items)


@app.route('/additem', methods=['POST','GET'])
def additem():
    form = ItemForm()
    if form.validate_on_submit():
        pic = 'default.png'
        pictures = 'default.png'
        if form.picture.data:
            print('YO!!!!!!!!! IT IS OVER HERE!!!')
            pic = save_picture(form.picture.data)
        # if form.other_pictures.data:
        #     for picture in form.other_pictures.data:
        #         pictures = []
        #         picture = save_picture(form.picture.data)
        #         pictures.append(picture)
        #         print (pictures)
        new_item = Item(name = form.name.data, category=form.category.data, price = form.price.data, image=pic, description = form.description.data, vendor = current_user.id)
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

@app.route('/categories')
def categories():
    return render_template('cat.html')

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
    return redirect(url_for('login'))

@app.route('/myitems')
def myitems():
    items = Item.query.filter_by(vendor = current_user.id).all()
    print(items)
    user = current_user
    return render_template('myitems.html' ,items = items, user=user)

@app.route('/update/<string:itemid>', methods=['POST','GET'])
def update(itemid):
    form = ItemForm()
    item = Item.query.filter_by(id = itemid).first()
    update = True
    print(item)
    if request.method == 'GET':
        form.name.data = item.name
        form.price.data = item.price
        form.description.data = item.description
        form.picture.data = item.image  
    if request.method == 'POST':
        if form.validate_on_submit():
            prevPicture = item.image
            print(prevPicture)
            item = Item(name = form.name.data, description = form.description.data, price = form.price.data, image = form.picture.data)
            print(item)
            db.session.commit()
            flash(f'Your Item has been updated', 'success')
            return redirect(url_for('account'))
        else:
            flash(f'There is a problem', 'danger')
                 
    return render_template('addpost.html', form=form, item=item, update=update)

@app.route('/delete/<string:itemid>', methods=['POST','GET'])
def delete(itemid):
    Item.query.filter_by(id = itemid).delete()
    db.session.commit()
    return redirect(url_for('myitems'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/sendmessage')
def sendmessage():
    api_key = "aniXLCfDJ2S0F1joBHuM0FcmH" #Remember to put your own API Key here
    phone = "0592865541" #SMS recepient"s phone number
    message = "You have been verified. You can now sell on ineruu.com"
    sender_id = "Tnsghana" #11 Characters maximum
    send_sms(api_key,phone,message,sender_id)
    flash (f'Account has been verified','success')
    return redirect('dashboard')

def send_sms(api_key,phone,message,sender_id):
    params = {"key":api_key,"to":phone,"msg":message,"sender_id":sender_id}
    url = 'https://apps.mnotify.net/smsapi?'+ urllib.parse.urlencode(params)
    content = urllib.request.urlopen(url).read()
    print (content)
    print (url)


@app.route('/verify')
def verify():
    return render_template('verify.html')

@app.route('/users')
def users():
    users = User.query.all()
    return render_template("users.html", users = users)

if __name__ == '__main__':
    app.run(debug=True)