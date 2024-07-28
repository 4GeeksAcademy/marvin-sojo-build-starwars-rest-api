"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, FavoritesPeople, FavoritesPlanets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# CRUD User
@app.route('/users', methods=['GET']) #Lista todos los usuarios
def get_all_users():
    users = User.query.all()
    serialized_user = [user.serialize() for user in users]
    return jsonify({"users": serialized_user}), 200



# CRUD People
@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    serialize_people = [person.serialize() for person in people]
    return jsonify({"people": serialize_people}), 200

@app.route('/people', methods=['POST'])
def create_person():
    body = request.json
    name = body.get("name", None)
    height = body.get("height", None)
    hair_color = body.get("hair_color", None)
    eye_color = body.get("eye_color", None)
    gender = body.get("gender", None)

    if name is None or height is None or hair_color is None or eye_color is None or gender is None:
        return jsonify({"error": "Todos los valores son requeridos"}), 400
    
    person = People(name=name, height=height, hair_color=hair_color, eye_color=eye_color, gender=gender)
    
    try:
        db.session.add(person)
        db.session.commit()
        db.session.refresh(person)

        return jsonify({"message": f"Person created {person.name}!"}), 201
    
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500
    
@app.route('/people/<int:id>', methods=["GET"])
def get_person(id):
    try:
        person = People.query.get(id)
        if person is None:
            return jsonify({"error": "Person not found"}), 404
        return jsonify({"person": person.serialize()}), 200
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500


# CRUD Planets
@app.route('/planets', methods=["GET"])
def get_all_planets():
    try:
        planets = Planets.query.all()
        serialize_planets = [planet.serialize() for planet in planets]
        return jsonify({"planets": serialize_planets}), 200
    except Exception as error:
        return jsonify({"error":f"{error}"}), 500

@app.route('/planets', methods=['POST'])
def create_planet():
    body = request.json
    name = body.get("name", None)
    diameter = body.get("diameter", None)
    climate = body.get("climate", None)
    terrain = body.get("terrain", None)
    population = body.get("population", None)

    if name is None or diameter is None or climate is None or terrain is None or population is None:
        return jsonify({"error": "Todos los valores son requeridos"}), 400
    
    planet = Planets(name=name, diameter=diameter, climate=climate, terrain=terrain, population=population)
    
    try:
        db.session.add(planet)
        db.session.commit()
        db.session.refresh(planet)

        return jsonify({"message": f"Planet created {planet.name}!"}), 201
    
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500
    
@app.route('/planets/<int:id>', methods=["GET"])
def get_planet(id):
    try:
        planet = Planets.query.get(id)
        if planet is None:
            return jsonify({"error": "Planet not found"}), 404
        return jsonify({"planet": planet.serialize()}), 200
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500

# CRUD Favorites 
@app.route('/users/favorites', methods=["GET"])
def get_all_favotites():
    try:
        favorites_people = FavoritesPeople.query.all()
        serialize_favorites_people = [favorite_person.serialize() for favorite_person in favorites_people]
        favorites_planets = FavoritesPlanets.query.all()
        serialize_favorites_planets = [favorite_planet.serialize() for favorite_planet in favorites_planets]
        return jsonify({"people": serialize_favorites_people}, {"planets": serialize_favorites_planets}), 200
    except Exception as error:
        return jsonify({"error":f"{error}"}), 500

@app.route('/favorite/planet/<int:planets_id>', methods=["POST"])
def create_favorite_planet(planets_id):
    body = request.json
    user_id = body.get("user_id", None)
    planet_exist = Planets.query.get(planets_id)
    if planet_exist is None:
        return jsonify({"error":f"Planet not found"}), 404

    planet_favorite = FavoritesPlanets(user_id=user_id, planets_id=planets_id)

    try:
        db.session.add(planet_favorite)
        db.session.commit()
        db.session.refresh(planet_favorite)

        return jsonify({"planet_favorite": planet_favorite.serialize()}), 201
    
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500
    
@app.route('/favorite/people/<int:people_id>', methods=["POST"])
def create_favorite_people(people_id):
    body = request.json
    user_id = body.get("user_id", None)
    people_exist = People.query.get(people_id)
    if people_exist is None:
        return jsonify({"error": f"People not found"}), 404
    
    people_favorite = FavoritesPeople(user_id=user_id, people_id=people_id)

    try:
        db.session.add(people_favorite)
        db.session.commit()
        db.session.refresh(people_favorite)

        return jsonify({"people_favorite": people_favorite.serialize()}), 201
    
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500

@app.route('/favorite/people/<int:people_id>', methods=["DELETE"])
def delete_favorite_people(people_id):
    try:
        people = FavoritesPeople.query.get(people_id)
        if people is None:
            return jsonify({"error":"People not found"}), 404
        db.session.delete(people)
        db.session.commit()

        return jsonify({"message":"people deleted"}), 200
    
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": f"{error}"}), 500

@app.route('/favorite/planet/<int:planets_id>', methods=["DELETE"])
def delete_favorite_planet(planets_id):
    try:
        planet = FavoritesPlanets.query.get(planets_id)
        if planet is None:
            return jsonify({"error": "Planet not found"}), 404
        db.session.delete(planet)
        db.session.commit()

        return jsonify({"message":"planet deleted"}), 200
    
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": f"{error}"}), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
