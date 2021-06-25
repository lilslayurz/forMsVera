from flask import Flask, render_template, redirect, url_for, session, request, g, session
from Forms import createSupplierForm, CreateRewardsForm, LoginStaffForm, CreateStaffForm, userchangeinfo, \
    CreateUserForm, UpdateForm, LoginForm, CreateQuestionForm, UpdateQuestionForm, CreateProductForm, CreateCheckoutForm
import os
import shelve, Supplier, Rewards, Staff, User, Question, Checkout
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename

# Instantiate Flask Object
app = Flask(__name__)
auth = HTTPBasicAuth
app.secret_key = 'any_random_string'

app.secret_key = os.urandom(24)

path = os.path.abspath(os.path.dirname(__file__))
Uploads = path + "/static/img/"
app.config["IMAGE_UPLOADS"] = Uploads
CSRF_ENABLED = True
SECRET_KEY = 'your-secret-key'


@app.route("/product_page")
def product_page():
    return render_template('Amri/product_page.html')


@app.route("/")
def main():
    supplier_dict = {}
    db = shelve.open('amri.db', 'r')
    supplier_dict = db['Suppliers']
    db.close()

    supplier_list = []
    for key in supplier_dict:
        supplier = supplier_dict.get(key)
        supplier_list.append(supplier)
    return render_template('home.html', supplier_list=supplier_list)


# Add to Cart
@app.route('/catalogue', methods=["POST", "GET"])
def catalogue():
    supplier_dict = {}
    db = shelve.open('amri.db', 'r')
    supplier_dict = db['Suppliers']
    db.close()

    supplier_list = []
    for key in supplier_dict:
        supplier = supplier_dict.get(key)
        supplier_list.append(supplier)
    return render_template('Amri/catalogue.html', count=len(supplier_list), supplier_list=supplier_list)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


# supplier login
@app.route("/supplier_login/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session.pop('user', None)

        if request.form['password'] == 'password':
            session['user'] = request.form['username']
            return redirect(url_for('protected_route'))
    return render_template("Amri/supplier_login.html")


# protected directory for supplier
@app.route('/supplier_portal/')
def protected_route():
    if g.user:
        return render_template('Amri/supplier_portal.html', user=session['user'])
    return redirect(url_for('index'))


# session
@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']


# Amri - Supplier Portal
@app.route('/supplier_portal/')
def supplier_portal():
    return render_template('Amri/supplier_portal.html')


# Amri -Supplier Logout
@app.route('/supplier_logout/')
def supplier_logout():
    return render_template('Amri/supplier_logout.html')


# Amri - Create Supplier under Portal

@app.route('/supplier_create/', methods=['GET', 'POST'])
def create_supplier():
    create_supplier_form = createSupplierForm(request.form)
    if request.method == 'POST' and create_supplier_form.validate():
        supplier_dict = {}
        db = shelve.open('amri.db', 'c')
        supplier_dict = db['Suppliers']
        image = request.files['note']
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['IMAGE_UPLOADS'], str(filename)))
        # file.save(os.path.join(UPLOAD, str(current_user.email)) + '.jpg')
        # try:
        #     Print("inside try")
        #     supplier_dict = db['Suppliers']
        #     image_name = ""
        #     if request.files:
        #         image = request.files["image"]
        #         image_name = image.filename
        #         image.save(os.path.join(app.config["IMAGE_UPLOADS"], image_name))
        # except:
        #     print("inside except")
        #     print("Error in retrieving Supplier from amri.db")

        supplier = Supplier.Supplier(create_supplier_form.full_name.data, create_supplier_form.email.data,
                                     create_supplier_form.category.data, create_supplier_form.membership.data,
                                     filename, create_supplier_form.quantity.data,
                                     create_supplier_form.description.data, create_supplier_form.price.data)
        supplier_dict[supplier.get_supplier_id()] = supplier
        db['Suppliers'] = supplier_dict

        db.close()
        return redirect(url_for('supplier_retrieve'))
    return render_template('Amri/supplier_create.html', form=create_supplier_form)


# Amri - Supplier Retrieval
@app.route('/supplier_retrieve')
def supplier_retrieve():
    supplier_dict = {}
    db = shelve.open('amri.db', 'r')
    supplier_dict = db['Suppliers']  # {
    db.close()

    supplier_list = []
    for key in supplier_dict:
        supplier = supplier_dict.get(key)
        supplier_list.append(supplier)
    return render_template('Amri/supplier_retrieve.html', count=len(supplier_list), supplier_list=supplier_list)


# Amri - Supplier Update
@app.route('/supplier_update/<int:id>/', methods=['GET', 'POST'])
def supplier_update(id):
    update_supplier_form = createSupplierForm(request.form)
    if request.method == 'POST' and update_supplier_form.validate():
        supplier_dict = {}
        db = shelve.open('amri.db', 'w')
        supplier_dict = db['Suppliers']

        # save
        if request.files:
            image = request.files['note']
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['IMAGE_UPLOADS'], str(filename)))

        supplier = supplier_dict.get(id)
        supplier.set_full_name(update_supplier_form.full_name.data)
        supplier.set_email(update_supplier_form.email.data)
        supplier.set_description(update_supplier_form.description.data)
        supplier.set_category(update_supplier_form.category.data)
        supplier.set_membership(update_supplier_form.membership.data)
        supplier.set_note(update_supplier_form.note.data)
        supplier.set_quantity(update_supplier_form.quantity.data)
        supplier.set_price(update_supplier_form.price.data)

        db['Suppliers'] = supplier_dict
        db.close()
        return redirect(url_for('supplier_retrieve'))
    else:
        supplier_dict = {}
        db = shelve.open('amri.db', 'r')
        supplier_dict = db['Suppliers']
        db.close()

        supplier = supplier_dict.get(id)
        update_supplier_form.full_name.data = supplier.get_full_name()
        update_supplier_form.email.data = supplier.get_email()
        update_supplier_form.category.data = supplier.get_category()
        update_supplier_form.membership.data = supplier.get_membership()
        update_supplier_form.description.data = supplier.get_description()
        update_supplier_form.note.data = supplier.get_note()
        update_supplier_form.quantity.data = supplier.get_quantity()
        update_supplier_form.price.data = supplier.get_price()
        return render_template('Amri/supplier_update.html', form=update_supplier_form)


@app.route('/supplier_delete/<int:id>', methods=['POST'])
def delete_supplier(id):
    supplier_dict = {}
    db = shelve.open('amri.db', 'w')
    supplier_dict = db['Suppliers']

    supplier_dict.pop(id)

    db['Suppliers'] = supplier_dict
    db.close()

    return redirect(url_for('supplier_retrieve'))


# Amri - to exit session of supplier portal
@app.route('/dropsession')
def drop_session():
    session.pop('user', None)
    session.clear()
    return render_template('Amri/supplier_logout.html')


@app.route('/staff_portal', methods=['GET', 'POST'])
def staff_portal():
    if request.method == 'POST':
        return render_template('Staff/staff_portal.html')
    elif request.method == 'POST':
        return render_template('Staff/staff_portal.html')
    else:
        return render_template('Staff/staff_portal.html')


# Create Staff Rewards
@app.route('/staff_create_rewards', methods=['GET', 'POST'])
def create_reward():
    create_rewards_form = CreateRewardsForm(request.form)
    if request.method == 'POST' and create_rewards_form.validate():
        rewards_dict = {}
        db = shelve.open('rewards.db', 'c')

        try:
            rewards_dict = db['Rewards']
        except:
            print("Error in retrieving Rewards from rewards.db")

        reward = Rewards.Rewards(create_rewards_form.reward_code.data, create_rewards_form.description.data)
        rewards_dict[reward.get_reward_id()] = reward
        db['Rewards'] = rewards_dict

        db.close()
        return redirect(url_for('rewards_retrieval'))
    return render_template('Staff/staff_create_rewards.html', form=create_rewards_form)



@app.route('/rewards_retrieval')
def rewards_retrieval():
    rewards_dict = {}
    db = shelve.open('rewards.db', 'r')
    rewards_dict = db['Rewards']
    db.close()

    rewards_list = []
    for key in rewards_dict:
        user = rewards_dict.get(key)
        rewards_list.append(user)

    return render_template('Staff/staff_rewards_retrieval.html', count=len(rewards_list), rewards_list=rewards_list)


@app.route('/rewards_update/<int:id>/', methods=['GET', 'POST'])
def rewards_update(id):
    update_rewards_form = CreateRewardsForm(request.form)
    if request.method == "POST" and update_rewards_form.validate():
        rewards_dict = {}
        db = shelve.open('rewards.db', 'w')
        rewards_dict = db['Rewards']

        reward = rewards_dict.get(id)
        reward.set_reward_code(update_rewards_form.reward_code.data)
        reward.set_description(update_rewards_form.description.data)

        db['Rewards'] = rewards_dict
        db.close()

        return redirect(url_for('rewards_retrieval'))
    else:
        rewards_dict = {}
        db = shelve.open('rewards.db', 'r')
        rewards_dict = db['Rewards']
        db.close()

        reward = rewards_dict.get(id)
        update_rewards_form.reward_code.data = reward.get_reward_code()
        return render_template('Staff/staff_updateRewards.html', form=update_rewards_form)


@app.route('/rewards_delete/<int:id>', methods=['POST'])
def delete_rewards(id):
    rewards_dict = {}
    db = shelve.open('rewards.db', 'w')
    rewards_dict = db['Rewards']

    rewards_dict.pop(id)

    db['Rewards'] = rewards_dict
    db.close()

    return redirect(url_for('rewards_retrieval'))


@app.route('/display_rewards')
def display_rewards():
    rewards_dict = {}
    db = shelve.open('rewards.db', 'r')
    rewards_dict = db['Rewards']
    db.close()

    rewards_list = []
    for key in rewards_dict:
        user = rewards_dict.get(key)
        rewards_list.append(user)

    return render_template("Amri/display_rewards.html", count=len(rewards_list), rewards_list=rewards_list)


# Create Staff Register
@app.route('/staff_register', methods=['GET', 'POST'])
def create_staff():
    create_staff_form = CreateStaffForm(request.form)
    if request.method == 'POST' and create_staff_form.validate():
        staff_dict = {}
        db = shelve.open('staff.db', 'c')

        try:
            staff_dict = db['Staff']
        except:
            print("Error in retrieving Users from staff.db.")
        staff = Staff.Staff(create_staff_form.username.data, create_staff_form.password.data,
                            create_staff_form.confirm.data, create_staff_form.first_name.data,
                            create_staff_form.last_name.data, create_staff_form.email.data)
        staff_dict[staff.get_username()] = staff
        db['Staff'] = staff_dict

        print(staff_dict)

        db.close()

        return render_template('home.html')
    return render_template('Staff/staff_register.html', form=create_staff_form)


@app.route('/staff_login', methods=['GET', 'POST'])
def staff_login():
    msg = ''
    login_staff_form = LoginStaffForm(request.form)

    if request.method == "POST":

        staff_dict = {}
        db = shelve.open('staff.db', 'c')

        try:
            staff_dict = db['Staff']

        except:
            print("Error in retrieving Users from staff.db.")

        db.close()

        staff_username = login_staff_form.username.data

        if staff_username in staff_dict:

            session['logged_name'] = staff_username
            return redirect(url_for('staff_portal'))

        else:
            msg = "Wrong username or password"

    return render_template('Staff/staff_login.html', msg=msg, form=login_staff_form)


# test codes


# ===============================================================================================================================================================================
# Danish
@app.route('/FAQ/', methods=['GET', 'POST'])
def question():
    create_q_form = CreateQuestionForm(request.form)
    if request.method == 'POST' and create_q_form.validate():
        questions_dict = {}
        db = shelve.open('questions.db', 'c')

        try:
            questions_dict = db['Questions']

        except:
            print("Error in retrieving Users from danish.db.")
        question = Question.Question(create_q_form.name.data, create_q_form.email.data, create_q_form.feedback.data,
                                     create_q_form.remark.data)
        questions_dict[question.get_question_id()] = question
        db['Questions'] = questions_dict
        return redirect(url_for('successfully'))

        db.close()

    return render_template('Danish/CQuestions.html', form=create_q_form)


@app.route('/form_submission/')
def successfully():
    return render_template("Danish/form_submission.html")


@app.route('/Queries/')
def retrieve_questions():
    questions_dict = {}
    db = shelve.open('questions.db', 'r')
    questions_dict = db['Questions']
    db.close()

    questions_list = []
    for key in questions_dict:
        question = questions_dict.get(key)
        questions_list.append(question)

    return render_template('Danish/SQuestions.html', count=len(questions_list), questions_list=questions_list)


@app.route('/UpdateQuestion/<int:id>/', methods=['GET', 'POST'])
def update_questions(id):
    update_q_form = CreateQuestionForm(request.form)
    if request.method == 'POST' and update_q_form.validate():
        questions_dict = {}
        db = shelve.open('questions.db', 'w')
        questions_dict = db['Questions']
        question = questions_dict.get(id)
        question.set_name(update_q_form.name.data)
        question.set_email(update_q_form.email.data)
        question.set_feedback(update_q_form.feedback.data)
        question.set_remark(update_q_form.remark.data)
        db['Questions'] = questions_dict
        db.close()

        return redirect(url_for('retrieve_questions'))
    else:
        questions_dict = {}
        db = shelve.open('questions.db', 'r')
        questions_dict = db['Questions']
        db.close()

        question = questions_dict.get(id)
        update_q_form.name.data = question.get_name()
        update_q_form.email.data = question.get_email()
        update_q_form.feedback.data = question.get_feedback()
        update_q_form.remark.data = question.get_remark()

        return render_template('Danish/UpdateQuestion.html', form=update_q_form)


@app.route('/DeleteQuestion/<int:id>', methods=['POST'])
def delete_question(id):
    questions_dict = {}
    db = shelve.open('questions.db', 'w')
    questions_dict = db['Questions']
    questions_dict.pop(id)
    db['Questions'] = questions_dict
    db.close()
    return redirect(url_for('retrieve_questions'))


@app.route('/Answers')
def answers():
    questions_dict = {}
    db = shelve.open('questions.db', 'r')
    questions_dict = db['Questions']
    db.close()

    questions_list = []
    for key in questions_dict:
        question = questions_dict.get(key)
        questions_list.append(question)

    return render_template('Danish/uAnswers.html', count=len(questions_list), questions_list=questions_list)


# danish
@app.route('/inventory/', methods=["GET"])
def retrieve_products():
    supplier_dict = {}
    db = shelve.open('amri.db', 'r')
    supplier_dict = db['Suppliers']
    db.close()

    supplier_list = []
    for key in supplier_dict:
        supplier = supplier_dict.get(key)
        supplier_list.append(supplier)

    return render_template('Danish/Inventory.html', count=len(supplier_list), supplier_list=supplier_list)


@app.route('/product_update/<int:id>/', methods=['GET', 'POST'])
def product_update(id):
    update_supplier_form = createSupplierForm(request.form)
    if request.method == 'POST' and update_supplier_form.validate():
        supplier_dict = {}
        db = shelve.open('amri.db', 'w')
        supplier_dict = db['Suppliers']
        supplier = supplier_dict.get(id)
        supplier.set_price(update_supplier_form.price.data)

        db['Suppliers'] = supplier_dict
        db.close()

        return redirect(url_for('retrieve_products'))
    else:
        supplier_dict = {}
        db = shelve.open('Amri.db', 'r')
        supplier_dict = db['Suppliers']
        db.close()

        supplier = supplier_dict.get(id)
        update_supplier_form.price.data = supplier.get_price()

        return render_template('Danish/product_update.html', form=update_supplier_form)


@app.route('/checkout/', methods=['GET', 'POST'])
def c_checkout():
    create_c_form = CreateCheckoutForm(request.form)
    if request.method == 'POST' and create_c_form.validate():
        checkouts_dict = {}
        db = shelve.open('checkouts.db', 'c')

        try:
            checkouts_dict = db['Checkouts']

        except:
            print("Error in retrieving Users from danish.db.")
        checkout = Checkout.Checkout(create_c_form.name.data, create_c_form.email.data, create_c_form.country.data,
                                     create_c_form.address.data, create_c_form.card.data,  create_c_form.date.data,
                                     create_c_form.cvv.data, create_c_form.status.data)
        checkouts_dict[checkout.get_order_id()] = checkout
        db['Checkouts'] = checkouts_dict
        return redirect(url_for('successful'))

        db.close()

    return render_template('Danish/checkout.html', form=create_c_form)


@app.route('/orders/', methods=['GET'])
def retrieve_orders():
    checkouts_dict = {}
    db = shelve.open('checkouts.db', 'r')
    checkouts_dict = db['Checkouts']
    db.close()

    checkouts_list = []
    for key in checkouts_dict:
        checkout = checkouts_dict.get(key)
        checkouts_list.append(checkout)

    return render_template('Danish/Order.html', count=len(checkouts_list), checkouts_list=checkouts_list)


@app.route('/UpdateOrder/<int:id>/', methods=['GET', 'POST'])
def update_order(id):
    update_c_form = CreateCheckoutForm(request.form)
    if request.method == 'POST' and update_c_form.validate():
        checkouts_dict = {}
        db = shelve.open('checkouts.db', 'w')
        checkouts_dict = db['Checkouts']
        checkout = checkouts_dict.get(id)
        checkout.set_status(update_c_form.status.data)
        db['Checkouts'] = checkouts_dict
        db.close()

        return redirect(url_for('retrieve_orders'))
    else:
        checkout_dict = {}
        db = shelve.open('checkouts.db', 'r')
        checkouts_dict = db['Checkouts']
        db.close()

        checkout = checkouts_dict.get(id)
        update_c_form.status.data = checkout.get_status()

        return render_template('Danish/Updateorder.html', form=update_c_form)


@app.route('/DeleteOrder/<int:id>', methods=['POST'])
def delete_order(id):
    checkout_dict = {}
    db = shelve.open('checkout.db', 'w')
    checkout_dict = db['checkouts']
    checkout_dict.pop(id)
    db['Checkouts'] = checkout_dict
    db.close()
    return redirect(url_for('retrieve_orders'))


@app.route('/form_submitted/')
def successful():
    return render_template("Danish/submit.html")


@app.route('/Order/', methods=['GET'])
def retrieve_order():
    checkouts_dict = {}
    db = shelve.open('checkouts.db', 'r')
    checkouts_dict = db['Checkouts']
    db.close()

    checkouts_list = []
    for key in checkouts_dict:
        checkout = checkouts_dict.get(key)
        checkouts_list.append(checkout)

    return render_template('Danish/c_orders.html', count=len(checkouts_list), checkouts_list=checkouts_list)

# Donavon --------------------------------------------------------------------------------------------------------------------------------------------------

# Donavon - Create User
@app.route('/register', methods=['GET', 'POST'])
def create_user():
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from storage.db.")

        user = User.User(create_user_form.username.data, create_user_form.password.data, create_user_form.confirm.data,
                         create_user_form.first_name.data, create_user_form.last_name.data, create_user_form.email.data)
        users_dict[user.get_username()] = user
        db['Users'] = users_dict

        print(users_dict)

        db.close()
        # extra line of codes
        session['logged_name'] = user.get_username()

        return render_template('home.html')
    return render_template('Donavon/register.html', form=create_user_form)


# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    login_user_form = LoginForm(request.form)

    if request.method == "POST":

        users_dict = {}
        db = shelve.open('user.db', 'c')

        try:
            users_dict = db['Users']

        except:
            print("Error in retrieving Users from storage.db.")

        db.close()

        user_username = login_user_form.username.data

        if user_username in users_dict:

            session['logged_name'] = user_username
            return redirect(url_for('main'))

        else:
            msg = "Wrong username or password"

    return render_template('Donavon/login.html', msg=msg, form=login_user_form)


# User Profile
@app.route('/profile')
def profile():
    users_dict = {}
    db = shelve.open('user.db', 'c')
    try:
        users_dict = db['Users']
    except:
        print("Error in retrieving Users from storage.db.")
    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    user = users_dict.get(session['logged_name'])
    print(user)

    print(key)
    print(users_list)
    return render_template("Donavon/profile.html", count=len(users_list), usersList=users_list, user=user)


# User logout
@app.route('/logout')
def logout():
    session.clear()
    return render_template("home.html")


# User update
@app.route('/update', methods=['GET', 'POST'])
def update():
    update_user_form = UpdateForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(session['logged_name'])
        user.set_username(update_user_form.username.data)
        user.set_first_name(update_user_form.first_name.data)
        user.set_last_name(update_user_form.last_name.data)
        user.set_email(update_user_form.email.data)

        db['Users'] = users_dict
        db.close()
        session['user_updated'] = user.get_username() + ' ' + user.get_password()

        return redirect(url_for('profile'))

    else:
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(session['logged_name'])
        update_user_form.username.data = user.get_username()
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.email.data = user.get_email()

    return render_template('Donavon/update.html', form=update_user_form)


@app.route('/Users_page')
def admin():
    users_dict = {}
    db = shelve.open('user.db', 'c')
    try:
        users_dict = db['Users']
    except:
        print("Error in retrieving Users from storage.db.")
    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template("Donavon/staffpage.html", count=len(users_list), usersList=users_list, user=user)


# Delete user account
@app.route('/delete/<string:username>', methods=["POST"])
def delete_user(username):
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Users']

    users_dict.pop(username)

    db['Users'] = users_dict
    db.close()
    session.clear()

    return render_template("home.html")


# initialise web
if __name__ == "__main__":
    app.run(debug=True)
