from wtforms import Form, StringField, SelectField, TextAreaField, validators, IntegerField, FileField, PasswordField, \
    RadioField, BooleanField, DateField, DecimalField, FloatField
import email_validator
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileAllowed

# Amri --------------------------------------------------------------------------------
# creating class
from wtforms.validators import DataRequired


class createSupplierForm(Form):
    full_name = StringField('Full Name', [validators.Length(min=1, max=150), validators.DataRequired()],
                            render_kw={"placeholder": "Enter your name"})
    email = EmailField('E-mail', [validators.Email()],
                       render_kw={"placeholder": "Enter your email"})
    category = SelectField(u'Category',
                           choices=[('Clothing', 'Clothing'), ('Shoes', 'Shoes'), ('Accessories', 'Accessories'),
                                    ('Bags', 'Bags'),
                                    ('Sports', 'Sports'), ('Miscellaneous', 'Miscellaneous')])
    membership = StringField('Member Status')
    quantity = IntegerField('Quantity of Product')
    note = FileField('Insert Image', validators=[FileAllowed(['jpg', 'png'])])
    description = StringField('Description', [validators.DataRequired()],
                            render_kw={"placeholder": "Describe items briefly, for example, (T-Shirts, Pants, etc)"})
    price = IntegerField('Price', [validators.DataRequired(message='Please enter suggested pricing')],
                         render_kw={"placeholder": "Please enter suggested pricing"})


class CreateRewardsForm(Form):
    reward_code = IntegerField('Code:', [validators.DataRequired(message='Please Enter Integers only')])
    description = StringField('Type Description')


class CreateStaffForm(Form):
    username = StringField('Staff Username', [validators.Length(min=6, max=24), validators.DataRequired()])
    password = PasswordField('Password',
                             [validators.DataRequired(),
                              validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('Email Address', [validators.Length(min=6, max=150), validators.DataRequired()])


class LoginStaffForm(Form):
    username = StringField('Username', [validators.Length(min=6, max=24), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])


class checkoutuserchangeinfo(Form):
    firstName = StringField('First Name',
                            [validators.Length(min=1, max=150), validators.DataRequired()])
    lastName = StringField('Last Name',
                           [validators.Length(min=1, max=150), validators.DataRequired()])

    email = StringField("Email Address", [validators.Length(min=5, max=50), validators.DataRequired()])
    accounttype = SelectField('Type', [validators.Optional()],
                              choices=[('Admin', 'Admin'), ('Staff', 'Staff'), ('User', 'User')], default='User')
    phone = StringField("Phone Number: ", validators=[
        validators.Regexp(r'^(?:\+?65)?[689]\d{7}$', message='Phone number needs to start with 6,8 or 9'),
        validators.Length(min=8, max=8), DataRequired()])
    city = SelectField('City:', choices=[('Singapore', 'Singapore')])
    address = StringField('Address:', [validators.data_required()])
    unit = StringField('Unit number:', [validators.data_required()])

    postal = IntegerField('Postal code:', [validators.data_required(message='Please Enter Integers only')])


class createStaffOrder(Form):
    style = {'class': 'form-control'}
    Name = StringField("Product Name:", [validators.DataRequired()], render_kw=style)

    Brand = SelectField('Brand:', [validators.DataRequired()],
                        choices=[('', 'Select'), ('Nike', 'Nike'), ('Adidas', 'Adidas'),
                                 ('UnderArmour', 'Under Armour')],
                        render_kw=style)

    Category = SelectField('Category:', [validators.DataRequired()],
                           choices=[('', 'Select'), ('Shoes', 'Shoes')],
                           render_kw=style)

    RetailPrice = FloatField('Retail Price:', [validators.DataRequired(message='Please Enter Integers only')],
                             render_kw=style)

    Quantity = IntegerField("Quantity:", [validators.DataRequired(message='Please Enter Integers only')],
                            render_kw=style)

    ListPrice = FloatField('List Price:', [validators.DataRequired(message='Please Enter Integers only')],
                           render_kw=style)

    Sale = BooleanField("Sale:", [validators.Optional()])

    SalePrice = IntegerField("Sale Price:", [validators.Optional()], render_kw=style)

    SaleStartDate = DateField('Sale Start Date:', [validators.Optional()], render_kw=style)

    SaleEndDate = DateField('Sale End Date:', [validators.Optional()], render_kw=style)

    Member = BooleanField("Membership:", [validators.Optional()])


class userchangeinfo(Form):
    firstName = StringField('First Name',
                            [validators.Length(min=1, max=150), validators.DataRequired()])
    lastName = StringField('Last Name',
                           [validators.Length(min=1, max=150), validators.DataRequired()])

    gender = RadioField('Gender', [validators.DataRequired()],
                        choices=[('female', 'Female'), ('male', 'Male')],
                        default='female')
    email = StringField("Email Address", [validators.Length(min=5, max=50), validators.DataRequired()])
    accounttype = SelectField('Type', [validators.Optional()],
                              choices=[('Admin', 'Admin'), ('Staff', 'Staff'), ('User', 'User')], default='User')
    phone = StringField("Phone Number: ", validators=[
        validators.Regexp(r'^(?:\+?65)?[689]\d{7}$', message='Phone number needs to start with 6,8 or 9'),
        validators.Length(min=8, max=8), DataRequired()])
    city = SelectField('City:', choices=[('Singapore', 'Singapore')])
    address = StringField('Address:', [validators.data_required()])
    unit = StringField('Unit number:', [validators.data_required()])

    postal = IntegerField('Postal code:', [validators.data_required(message='Please Enter Integers only')])

    # Donavon ---------------------------------------------------------------------------------------------------


class CreateUserForm(Form):
    username = StringField('Username', [validators.Length(min=6, max=24), validators.DataRequired()])
    password = PasswordField('Password',
                             [validators.DataRequired(),
                              validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('Email Address', [validators.Length(min=6, max=150), validators.DataRequired()])


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=6, max=24), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])


class UpdateForm(Form):
    username = StringField('Username', [validators.Length(min=6, max=24), validators.DataRequired()])
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('Email Address', [validators.Length(min=6, max=150), validators.DataRequired()])


# Danish ----------------------------------------------------------------------------------------------
class CreateQuestionForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('Email Address', [validators.Length(min=1, max=150), validators.DataRequired()])
    feedback = TextAreaField('Feedback(max = 150 characters)',
                             [validators.Length(min=1, max=150), validators.DataRequired()])
    remark = StringField('remark')


class UpdateQuestionForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('Email Address', [validators.Length(min=1, max=150), validators.DataRequired()])
    feedback = TextAreaField('Feedback(max = 150 characters)',
                             [validators.Length(min=1, max=150), validators.DataRequired()])
    remark = StringField('remark')


class CreateProductForm(Form):
    product = FileField('Product Image')
    product_name = StringField('Product Name', [validators.length(min=1, max=150), validators.DataRequired()])
    category = SelectField('Category', choices=[('Outerwear', 'Outerwear'), ('Shirt', 'Shirt'), ('Pants', 'Pants'),
                                                ('Shoes', 'Shoes')])
    quantity = IntegerField('Quantity', [validators.DataRequired()])
    price = IntegerField('Price', [validators.DataRequired()])


class CreateCheckoutForm(Form):
    name = StringField('Name(max = 20 characters', [validators.DataRequired(), validators.Length(min=1, max=150)])
    email = EmailField('Email Address', [validators.DataRequired()])
    country = StringField('Country', [validators.DataRequired()])
    address = StringField('Address', [validators.DataRequired()])
    card = IntegerField('Credit Card Number', [validators.DataRequired()])
    date = DateField('Expiry Date Of Credit Card(MM/YYYY)', format='%m/%Y')
    cvv = IntegerField('CVV(Enter the 3 digit number at the back of your card)',
                       [validators.DataRequired()])
    status = StringField('status', [validators.Optional()], default='processing')
