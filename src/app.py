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
from models import db, User, People, PeopleFavorites

# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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


@app.route('/users', methods=['GET'])
def handle_hello():
    users = User.query.all()
    print(type(users[0].serialize()))
    # ---------- Opcion 1 ----------------
    users_serialized = []
    for user in users:
        users_serialized.append(user.serialize())
    # ---------- Opcion 2 ----------------
    users_serialized = list(map(lambda user: user.serialize(), users))

    # -----------------------------------------

    print(users_serialized)
    response_body = {
        "data": users_serialized
    }

    return jsonify(response_body), 200


@app.route('/user', methods=['POST'])
def create_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400
    if 'email' not in body:
        return jsonify({'msg': 'El campo "email" es obligatorio'}), 400
    if 'password' not in body:
        return jsonify({'msg': 'El campo "password" es obligatorio'}), 400
    new_user = User()
    new_user.email = body['email']
    new_user.password = body['password']
    new_user.is_active = True

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'msg': 'OK', 'data': new_user.serialize()})


@app.route('/user/favorites/<int:user_id>', methods=['GET'])
def get_favorites(user_id):
    # traer usuario con id 5
    user = User.query.get(user_id)
    print(user.favorites)  # esto es una lista con los registros de los likes
    favorites_serialized = []
    for favorite in user.favorites:
        print(favorite.people)
        favorites_serialized.append(favorite.people.serialize())
    return jsonify({'msg': 'ok', 'favorites': favorites_serialized})


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
