from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import MultipleFileField

class RegistrationForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


# Form validation for item name
class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=24)])
    price = IntegerField('Price', validators=[DataRequired()])
    description = StringField('Description', widget=TextArea(), validators=[DataRequired()])
    picture = FileField('Add a picture', validators=[ FileAllowed(['jpg', 'png','jpeg'])])
    category = SelectField('Category', choices=[('Fashion', 'Fashion'), ('Tech','Tech'), ('Medicine','Medicine'),('Jobs','Jobs'),('Vehicles','Vehicles'),('Animals','Animals'),('Food','Food'),('Pets','Pets'),('Others','Others')])
    other_pictures = MultipleFileField('Choose your other pictures',  validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add Item')

class LoginForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class Search(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')
