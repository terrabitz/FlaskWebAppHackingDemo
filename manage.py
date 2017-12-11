from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server, prompt, prompt_bool

from app.main import app, db, user_datastore

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server())


@manager.command
def create_user():
    def create_and_add_user(email):
        password = prompt('Enter password')
        user = user_datastore.create_user(email=email, password=password)
        super_user = prompt_bool('Should user be admin?')
        if super_user:
            super_user_role = user_datastore.find_role('superuser')
            user_datastore.add_role_to_user(user, super_user_role)
        else:
            user_role = user_datastore.find_role('user')
            user_datastore.add_role_to_user(user, user_role)
        db.session.add(user)
        db.session.commit()
        print('New credentials are admin/{}'.format(password))

    with app.app_context():
        email = prompt('Enter email')
        user = user_datastore.get_user(email)
        if user:
            if prompt_bool('User already exists. Override?'):
                user_datastore.delete_user(user)
                db.session.commit()
                create_and_add_user(email)
            else:
                print('Exiting...')
                exit(0)
        else:
            create_and_add_user(email)


if __name__ == '__main__':
    manager.run()
