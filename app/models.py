from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), nullable=False, unique=True)
    total_debtors: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    address: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    phone_number: so.Mapped[str] = so.mapped_column(sa.String(15), nullable=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))
    total_amount_due: so.Mapped[float] = so.mapped_column(sa.Float, default=0.0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Debtor(db.Model):
    __tablename__ = 'debtors'
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)
    amount_due: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.String(255))

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'), nullable=False)
    user: so.Mapped[User] = so.relationship('User', back_populates='debtors')

    def __repr__(self):
        return f'<Debtor {self.username}>'

User.debtors = so.relationship('Debtor', order_by=Debtor.id, back_populates='user')
