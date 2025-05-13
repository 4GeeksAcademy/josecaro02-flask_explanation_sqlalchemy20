import os
from flask_admin import Admin
from models import db, User, People, PeopleFavorites
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import class_mapper, RelationshipProperty


class PeopleFavoritesModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla PeopleFavorites
    column_list = ['id', 'user', 'people', 'user_id', 'people_id']


class PeopleModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla PeopleFavorites
    column_list = ['id', 'name', 'email', 'height', 'favorite_by']


class UserModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla PeopleFavorites
    column_list = ['id', 'email', 'password', 'favorites', 'is_active']


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(PeopleModelView(People, db.session))
    admin.add_view(PeopleFavoritesModelView(PeopleFavorites, db.session))
    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
