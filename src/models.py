from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    user_favorites_people = db.relationship("FavoritesPeople", backref="user", lazy=True)
    user_favorites_planets = db.relationship("FavoritesPlanets", backref="user", lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
    def __repr__(self):
        return '<User %r>' % self.email

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    hair_color = db.Column(db.String(50), nullable=False)
    eye_color = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    favorites_people = db.relationship("FavoritesPeople", backref="people", lazy=True)
    
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "gender": self.gender
        }
    def __repr__(self):
        return '<People %r>' % self.name
    
    
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.String(50), nullable=False)
    terrain = db.Column(db.String(50), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    favorites_planets = db.relationship("FavoritesPlanets", backref="planets", lazy=True)
    
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population
        }
    
    def __repr__(self):
        return '<Planets %r>' % self.name

class FavoritesPeople(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    

    def serialize(self):
        return{
            "id": self.id,
            "user": self.user_id,
            "people": self.people_id
        }
    
    def __repr__(self):
        return f'<FavoritesPeople user: {self.user_id} people: {self.people_id}>'

class FavoritesPlanets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    
    

    def serialize(self):
        return{
            "id": self.id,
            "user": self.user_id,
            "planets": self.planets_id
        }
    
    def __repr__(self):
        return f'<FavoritesPlanets user: {self.user_id} planets: {self.planets_id}>'