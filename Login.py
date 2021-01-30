import flask_login
from app import app
from User import User

app.secret_key = 'xyzzyx'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class Users(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    record = User.query.filter_by(username=username).first()
    if record is None:
        return
    user = Users()
    user.id = username

    print('user_loader() called')
    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    record = User.query.filter_by(username=username).first()
    if record is None:
        return

    user = Users()
    user.id = username
    #user.is_authenticated = request.form.get('password') == record.password
    user.is_authenticated = True
    print('request_loader() called')
    return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    print('unauthorized_handler() called')
    return 'Unauthorized'
