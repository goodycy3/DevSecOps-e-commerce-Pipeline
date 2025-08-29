from flask import Flask, render_template, request
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

# Demo product data (prices as numbers; images are filenames only)
products = [
    {
        "id": 1,
        "name": "Stylish Camera",
        "price": 299.99,
        "image": "Men_cloth.png",
        "badge": "New",
        "rating": 4.8,
    },
    {
        "id": 2,
        "name": "Wireless Headphones",
        "price": 149.99,
        "image": "Headset.png",
        "badge": "Top",
        "rating": 4.6,
    },
    {
        "id": 3,
        "name": "Smart Watch",
        "price": 199.99,
        "image": "Watch.png",
        "badge": "Sale",
        "rating": 4.7,
    },
]

@app.route("/")
def index():
    # templates/index.html reads request.args for the training vulns (welcome/msg/next)
    return render_template("index.html", products=products)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # debug=True left on intentionally for training (do not use in prod)
    app.run(debug=True, host="0.0.0.0", port=port)
