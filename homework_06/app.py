from flask import Flask, render_template
from flask_migrate import Migrate

from views.products import products_bp
from models.database import db

app = Flask(__name__)
app.register_blueprint(products_bp, url_prefix="/products")

app.config.update(
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./products.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
db.init_app(app)

# https://flask-migrate.readthedocs.io/en/latest/
migrate = Migrate(app, db)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about/")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
