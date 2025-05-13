from flask import Flask , render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from flask_bootstrap import Bootstrap5
import os

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.secret_key = os.environ.get("SECRET_KEY")


class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'

db = SQLAlchemy(app)
# db.init_app(app)

class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    location: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    has_sockets: Mapped[int] = mapped_column(Integer)
    has_toilet: Mapped[int] = mapped_column(Integer)
    has_wifi: Mapped[int] = mapped_column(Integer)
    can_take_calls: Mapped[int] = mapped_column(Integer)
    seats: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)


with app.app_context():
    db.create_all()  



class Form(FlaskForm):
    cafe_name = StringField(label="Name")
    map_url = StringField(label="Map URL")
    img_url = StringField(label="Image URL")
    location = StringField(label="Location")
    socket = SelectField(label="Socket", choices=[0, 1])
    toilet = SelectField(label="Toilet", choices=[0, 1])
    wifi = SelectField(label="Wifi", choices=[0, 1])
    calls = SelectField(label="Can Make a Call", choices=[0, 1])
    seats = StringField(label="Number of Seats")
    coffee_price = StringField(label="Coffee's Price")
    submit = SubmitField(label="Submit")






@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cafes", methods=["POST", "GET"])
def cafes():
    all_cafes = db.session.execute(db.select(Cafe)).scalars().all()

    return render_template("cafes.html", cafes=all_cafes)


@app.route("/add", methods=["POST", "GET"])
def add():
    form = Form()
    if form.validate_on_submit():
        new_cafe = Cafe(name=form.cafe_name.data, map_url=form.map_url.data,
                        img_url=form.img_url.data, location=form.location.data,
                        has_sockets= form.socket.data, has_toilet=form.toilet.data,
                        has_wifi=form.wifi.data, can_take_calls=form.calls.data,
                        seats=form.seats.data, coffee_price=form.coffee_price.data)
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('cafes'))
    
    return render_template("add.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)