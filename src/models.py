from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=True)
    password: Mapped[str] = mapped_column(String(16), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorites: Mapped[list['PeopleFavorites']] = relationship(
        back_populates='user', cascade='all, delete-orphan', lazy='joined')

    def __repr__(self):
        return f'Usuario con id {self.id} y email: {self.email}'

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'is_active': self.is_active
        }


class People(db.Model):
    __tablename__ = 'people'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    height: Mapped[int] = mapped_column(Integer, nullable=True)
    favorite_by: Mapped[list['PeopleFavorites']] = relationship(
        back_populates='people', cascade='all, delete-orphan', lazy='joined')

    def __repr__(self):
        return f'Personaje de nombre {self.name}'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'height': self.height
        }


class PeopleFavorites(db.Model):
    __tablename__ = 'people_favorites'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(
        back_populates='favorites', lazy='joined')
    people_id: Mapped[int] = mapped_column(ForeignKey('people.id'))
    people: Mapped['People'] = relationship(
        back_populates='favorite_by', lazy='joined')

    def __repr__(self):
        return f'Al usuario {self.user_id} le gusta el personaje {self.people_id}'
