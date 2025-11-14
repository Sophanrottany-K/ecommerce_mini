from flask import flash,render_template, session, redirect, url_for, request
import requests
from telegram.telegrambot import sendMessage, token
# -------------------- Helper Functions --------------------
def get_products():
    """Fetch all products from FakeStore API"""
    response = requests.get("https://fakestoreapi.com/products")
    return response.json() if response.status_code == 200 else []

def get_single_product(product_id):
    """Fetch single product by ID from FakeStore API"""
    response = requests.get(f"https://fakestoreapi.com/products/{product_id}")
    return response.json() if response.status_code == 200 else None

# -------------------- Initialize Routes --------------------
def init_routes(app):

    @app.route("/")
    def index():
        search_query = request.args.get("q", "").lower().strip()
        data = get_products()
        if search_query:
            # Filter products whose title contains the search keyword
            data = [p for p in data if search_query in p["title"].lower()]

        return render_template("index.html",products=data, search_query=search_query)

    # ---------------- Products Listing with Search ----------------

    @app.route("/about")
    def about():
        return render_template("about.html")
    @app.route("/products")
    def products():
        search_query = request.args.get("q", "").lower().strip()
        data = get_products()
        if search_query:
            # Filter products whose title contains the search keyword
            data = [p for p in data if search_query in p["title"].lower()]
        return render_template("products.html", products=data, search_query=search_query)

    # ---------------- Product Detail ----------------
    @app.route("/product/<int:id>")
    def product_detail(id):
        product = get_single_product(id)
        if not product:
            return "Product not found", 404
        return render_template("product_detail.html", product=product)

    # ---------------- Add to Cart ----------------
    @app.route("/add_to_cart/<int:id>")
    def add_to_cart(id):
        cart = session.get("cart", [])  # list of product IDs
        cart.append(id)
        session["cart"] = cart
        return redirect(url_for("cart"))

    # ---------------- Remove from Cart ----------------
    @app.route("/remove_from_cart/<int:id>")
    def remove_from_cart(id):
        cart = session.get("cart", [])
        # remove all instances of this product from cart
        cart = [pid for pid in cart if pid != id]
        session["cart"] = cart
        return redirect(url_for("cart"))

    # ---------------- Cart Page ----------------
    @app.route("/cart")
    def cart():
        cart_ids = session.get("cart", [])
        items_dict = {}
        total = 0

        # Count quantities for each product
        for pid in cart_ids:
            items_dict[pid] = items_dict.get(pid, 0) + 1

        items = []
        for pid, qty in items_dict.items():
            product = get_single_product(pid)
            if product:
                product['quantity'] = qty
                product['subtotal'] = product['price'] * qty
                total += product['subtotal']
                items.append(product)

        return render_template("cart.html", items=items, total=total,hide_footer=True)
    @app.get('/contact')
    def contact():
        return render_template('contact.html')

    @app.post('/contact/submit')
    def contact_submit():
        form = request.form
        name = form.get('name')
        email = form.get('email')
        subject = form.get('subject')
        phone = form.get('phone')
        message = form.get('message')

        if not name or not email or not message:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('contact'))

        telegram_message = f"""
        🔔 <b>New Contact Form Submission</b>
    
        👤 <b>Name:</b> {name}
        📧 <b>Email:</b> {email}
        📞 <b>Phone:</b> {phone or 'Not provided'}
        💡 <b>Subject:</b> {subject or 'Not provided'}
        💬 <b>Message:</b>
        {message}
        """

        result = sendMessage(token, telegram_message)

        if '"ok":true' in result:
            flash('Thank you! Your message has been sent successfully.', 'success')
        else:
            flash('Sorry, there was an error sending your message. Please try again.', 'error')

        return redirect(url_for('contact'))
