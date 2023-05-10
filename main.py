import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##Connect to Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return f"<Cafe {self.name}>"

    def to_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


## HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():
    random_id = random.randint(1, Cafe.query.count())
    print(random_id)
    # cafes = db.session.query(Cafe).all()
    random_cafe = Cafe.query.get(random_id)
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all_cafes():
    all_cafes = db.session.query(Cafe).all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route("/search")
def search_cafe():
    query_location = request.args.get("loc")
    cafe_list = Cafe.query.filter_by(location=query_location).all()
    if cafe_list:
        return jsonify(cafes=[cafe.to_dict() for cafe in cafe_list])
    else:
        return jsonify(
            error={
                "Not Found": "Sorry, we don't have a cafe at that location.",
                "code": 404,
            }
        )
    pass


## HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_cafe():
    cafe_data = request.form.to_dict()
    new_cafe = Cafe(
        name=cafe_data["name"],
        map_url=cafe_data["map_url"],
        img_url=cafe_data["img_url"],
        location=cafe_data["location"],
        seats=cafe_data["seats"],
        has_toilet=bool(cafe_data["has_toilet"]),
        has_wifi=bool(cafe_data["has_wifi"]),
        has_sockets=bool(cafe_data["has_sockets"]),
        can_take_calls=bool(cafe_data["can_take_calls"]),
        coffee_price=cafe_data["coffee_price"],
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == "__main__":
    app.run(debug=True)
