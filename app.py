from flask import Flask,session
from route import init_routes

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "secret123"
@app.context_processor
def cart_processor():
    cart = session.get("cart", [])
    return dict(cart_count=len(cart))
# register routes
init_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
