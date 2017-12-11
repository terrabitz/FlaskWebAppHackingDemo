from flask import Flask, session, request, render_template, g, redirect, url_for, abort
from flask_security import Security, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .models import db, user_datastore, User, Role

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Keep it secret, keep it safe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['EXPLAIN_TEMPLATE_LOADING'] = True
app.config['DEBUG'] = True
db.init_app(app)


def add_jinja_functions(app):
    """Adds desired python functions to be accessible from Jinja templates"""
    app.jinja_env.globals.update(
        hasattr=hasattr,
        enumerate=enumerate,
        len=len
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


def init_security_extension_db(app):
    security = Security(app, user_datastore)
    user_datastore.create_role(name='superuser')
    user_datastore.create_role(name='user')


@app.before_request
def before_request():
    g.user = current_user
    g.session = session
    g.path = request.path


demo_pages = {

}


@app.route('/')
def index():
    return render_template('index.html', pages=demo_pages)


add_jinja_functions(app)
init_admin_extension(app)
init_security_extension_db(app)

if __name__ == '__main__':
    app.run()
