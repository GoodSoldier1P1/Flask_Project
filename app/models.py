from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from sqlalchemy.sql.expression import func


# create instance of database
db = SQLAlchemy()


added_to_team = db.Table(
    'added_to_team',
    db.Column('poke_id', db.String, db.ForeignKey('pokemon.poke_id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    team = db.relationship('Pokemon',
                           secondary = (added_to_team),
                           backref = 'trainer',
                           lazy = 'dynamic'
                           )

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)





class Pokemon(db.Model):
    poke_id = db.Column(db.String, primary_key=True)
    sprite = db.Column(db.String)
    poke_type = db.Column(db.String)
    ability = db.Column(db.String)
    ability_description = db.Column(db.String)
    hp = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    base_xp = db.Column(db.Integer)

    def __init__(self, poke_id, sprite, poke_type, ability, ability_description, hp, defense, attack, base_xp):
        self.poke_id = poke_id
        self.sprite = sprite
        self.poke_type = poke_type
        self.ability = ability
        self.ability_description = ability_description
        self.hp = hp
        self.defense = defense
        self.attack = attack
        self.base_xp = base_xp

