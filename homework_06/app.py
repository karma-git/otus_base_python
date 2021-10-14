from flask import Flask, render_template
from views.products import products_bp

app = Flask(__name__)
app.register_blueprint(products_bp, url_prefix="/products")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about/")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
