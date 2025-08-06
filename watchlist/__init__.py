import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# SQLite URI compatible
WIN = sys.platform.startswith('win') # win32 or win64
if WIN:
    prefix = 'sqlite:///' # Windows
else:
    prefix = 'sqlite:////' # Unix/Linux/MacOS

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) # SQLAlchemy管理sqlite数据库
login_manager = LoginManager(app) # login auth manager

# 导入user 
@login_manager.user_loader # Flask-Login装饰器
def load_user(user_id):
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'login' # 当用户访问login_required装饰的视图时，Flask-Login会自动重定向到login_view指定的视图
# login_manager.login_message = 'Your custom message'


@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)


from watchlist import views, errors, commands
