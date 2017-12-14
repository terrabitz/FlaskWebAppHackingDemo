import random

from flask import Flask, session, request, render_template, g, redirect, url_for, abort, make_response
from flask_security import Security, current_user, SQLAlchemyUserDatastore
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import desc

from app.models import db, User, Role, SuperSecureData, Orders, SessionDemo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Keep it secret, keep it safe'
app.config['SECURITY_PASSWORD_SALT'] = 'asdfasdfasdfasdfasdf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['EXPLAIN_TEMPLATE_LOADING'] = True
app.config['DEBUG'] = True
db.init_app(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)


def add_jinja_functions(app):
    """Adds desired python functions to be accessible from Jinja templates"""
    app.jinja_env.globals.update(
        hasattr=hasattr,
        enumerate=enumerate,
        len=len,
        str=str
    )


# Create customized model view class
class SecurityModelView(ModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


def init_admin_extension(app):
    admin = Admin(app, name='Web App Demo', template_mode='bootstrap3')
    admin.add_view(SecurityModelView(User, db.session))
    admin.add_view(SecurityModelView(Role, db.session))
    admin.add_view(SecurityModelView(SuperSecureData, db.session))
    admin.add_view(SecurityModelView(Orders, db.session))


def init_security_extension_db(app):
    security = Security(app, user_datastore)
    with app.app_context():
        user_datastore.create_role(name='superuser')
        user_datastore.create_role(name='user')


@app.before_first_request
def initial_setup():
    init_security_extension_db(app)
    add_jinja_functions(app)
    init_admin_extension(app)


@app.before_request
def before_request():
    g.user = current_user
    g.session = session
    g.path = request.path


@app.route('/spider/<int:id>')
def spider(id):
    return render_template('spider.html', id=id, page_title='Page ' + str(id),
                           page_description='This page is to help demonstrate spidering')


@app.route('/shop', methods=['GET', 'POST'])
def shop():
    if request.method == 'GET':
        return render_template('shop.html', page_title='Shop',
                               page_description='This is to showcase client-side bypass techniques')
    elif request.method == 'POST':
        quantity = request.form.get('quantity')
        cost = request.form.get('cost')
        return render_template(
            'order.html',
            page_title='Order Confirmed',
            page_description='This is to showcase client-side bypass technique',
            cost=float(cost),
            quantity=int(quantity)
        )


@app.route('/shipping_order', methods=['GET', 'POST'])
def sqli():
    results = []
    error = ''
    order_id = request.form.get('order_id')
    if request.method == 'POST' and order_id:
        connection = db.engine.connect()
        rows = connection.execute(
            'select * from orders where id = \'{}\' and user_id={}'.format(order_id, current_user.id))
        for row in rows:
            order = {}
            for key, value in row.items():
                order[key] = value
            results.append(order)
        if not results:
            error = 'Could not find order {}'.format(order_id)

    return render_template(
        'shipping_order.html',
        page_title='Shipping Order Lookup',
        page_description='This is to demonstrate basic SQL injection attacks',
        results=results,
        error=error
    )



@app.route('/login_demo', methods=['GET', 'POST'])
def login_demo():
    page_title = 'Login Page'
    page_description = 'This is page to demonstrate weak session cookies'
    session_num = request.cookies.get('session_demo')
    username = ''
    cookies_to_set = {}
    error = ''
    if session_num:
        session_demo = SessionDemo.query.filter_by(session_num=session_num).first()
        if not session_demo:
            return redirect(url_for('login_demo_logout'))
        username = session_demo.username

    elif request.method == 'POST':
        username = request.form.get('username')
        if not username:
            error = 'Please enter a valid user'
        elif not SessionDemo.query.filter_by(username=username).first():
            session_demo = SessionDemo.query.order_by(SessionDemo.session_num.desc()).first()
            if not session_demo:
                max_session_num = random.randint(100000000, 999999999)
            else:
                max_session_num = session_demo.session_num + 1
            new_session_demo = SessionDemo(username=username, session_num=max_session_num)
            db.session.add(new_session_demo)
            db.session.commit()
            cookies_to_set['session_demo'] = max_session_num

    response = make_response(render_template(
        'login_demo.html',
        page_title=page_title,
        page_description=page_description,
        username=username,
        error=error
    ))

    if cookies_to_set:
        for key, value in cookies_to_set.items():
            key = str(key).encode()
            value = str(value).encode()
            response.set_cookie(key, value)
    return response


@app.route('/login_demo/logout', methods=['GET'])
def login_demo_logout():
    session_num = request.cookies.get('session_demo')
    response = make_response(
        redirect(url_for('login_demo'))
    )
    if session_num:
        session_demo = SessionDemo.query.filter_by(session_num=session_num).first()
        if session_demo:
            db.session.delete(session_demo)
            db.session.commit()
        response.set_cookie('session_demo', '', expires=0)

    return response


demo_pages = {
    'Spidering': '/spider/1',
    'Shop': '/shop',
    'Shipping Order': '/shipping_order',
    'Login': '/login_demo'
}


@app.route('/')
def index():
    return render_template('index.html', pages=demo_pages)


if __name__ == '__main__':
    app.run()
