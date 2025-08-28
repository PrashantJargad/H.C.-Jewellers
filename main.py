from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String, Integer, Float
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, EmailField, TextAreaField, FloatField, PasswordField
from wtforms.validators import DataRequired
import os
from dotenv import load_dotenv

load_dotenv()


class Base(DeclarativeBase):
    pass


app = Flask(__name__)


# login_manager = LoginManager()
# login_manager.init_app(app)

db = SQLAlchemy(model_class=Base)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URI')
db.init_app(app)


class Contact_Form(FlaskForm):
    first_name = StringField(label="First Name")
    last_name = StringField(label="Last Name")
    email = EmailField(label="Email")
    mobile_no = IntegerField(label="Phone", validators=[DataRequired()])
    particular_item = TextAreaField(label="Anything Particular you are looking for?")
    submit = SubmitField(label="Submit")


class Add_Data(FlaskForm):
    password = PasswordField(label="Enter Password", validators=[DataRequired()])
    length = FloatField(label="Length")
    width = FloatField(label="Width (MM)")
    height = FloatField(label="Height (MM)")
    weight = FloatField(label="Carat")
    color = StringField(label="Color")
    clarity = StringField(label="Clarity")
    shape = StringField(label="Shape")
    cut = StringField(label="Cut")
    enhancements = StringField(label="Enhancements")
    pcs = StringField(label="Total Pieces")
    img_count = IntegerField(label="Total Image")
    submit = SubmitField(label="Submit")


class Emeralds(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    length: Mapped[float] = mapped_column(Float)
    width: Mapped[float] = mapped_column(Float)
    height: Mapped[float] = mapped_column(Float)
    weight: Mapped[float] = mapped_column(Float)
    color: Mapped[str] = mapped_column(String(50))
    clarity: Mapped[str] = mapped_column(String(100))
    shape: Mapped[str] = mapped_column(String(50))
    cut: Mapped[str] = mapped_column(String(50))
    enhancements: Mapped[str] = mapped_column(String(50))
    pcs: Mapped[str] = mapped_column(String(2000))
    img_count: Mapped[int] = mapped_column(Integer)


class Contact(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    phone_no: Mapped[int] = mapped_column(Integer, nullable=False)
    particular_item: Mapped[str] = mapped_column(String, nullable=True)


# with app.app_context():
#     db.create_all()

@app.route("/add-data", methods=["GET", "POST"])
def add_data():
    emerald_data = Add_Data()
    if emerald_data.validate_on_submit():
        user_password = emerald_data.password.data
        correct_password = os.getenv("ADMIN_PASSWORD")
        if user_password != correct_password:
            return "Unauthorized", 403

        new_data = Emeralds(
            length=emerald_data.length.data,
            width=emerald_data.width.data,
            height=emerald_data.height.data,
            weight=emerald_data.weight.data,
            color=emerald_data.color.data,
            clarity=emerald_data.clarity.data,
            shape=emerald_data.shape.data,
            cut=emerald_data.cut.data,
            enhancements=emerald_data.enhancements.data,
            pcs=emerald_data.pcs.data,
            img_count=emerald_data.img_count.data
        )
        db.session.add(new_data)
        db.session.commit()

        return redirect(url_for("add_data"))

    # 🔹 Always fetch fresh data from DB
    product = db.session.query(Emeralds).all()

    return render_template(
        "post.html",
        emerald_data_form=emerald_data,
        product=product
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/product")
def product():
    # Always query fresh data from DB
    products = db.session.execute(db.select(Emeralds)).scalars().all()
    return render_template("product.html", product=products)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    contact_form = Contact_Form()
    if contact_form.validate_on_submit():
        first_name = contact_form.first_name.data
        last_name = contact_form.last_name.data
        email = contact_form.email.data
        mobile_no = contact_form.mobile_no.data
        particular_item = contact_form.particular_item.data

        contact_detail = Contact(first_name=first_name, last_name=last_name, email=email, phone_no=mobile_no, particular_item=particular_item)
        db.session.add(contact_detail)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template("contact.html", contact=contact_form)


if __name__ == "__main__":
    app.run(debug=False)
