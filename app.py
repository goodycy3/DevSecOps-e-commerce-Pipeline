from flask import Flask, render_template
import os

app = Flask(__name__)

# Product data
products = [
    {
        "id": 1,
        "name": "Stylish Camera",
        "price": "299.99",
        "image": "static/images/Men_cloth.png"
    },
    {
        "id": 2,
        "name": "Wireless Headphones",
        "price": "149.99",
        "image": "static/images/Headset.png"
    },
    {
        "id": 3,
        "name": "Smart Watch",
        "price": "199.99",
        "image": "static/images/Watch.png"
    }
]

@app.route('/')
def index():
    return render_template('index.html', products=products)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
