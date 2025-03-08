from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL database connection configuration
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sac148*+S",
    database="os2"
)

# Function to create a new cursor connected to the database
def get_database_cursor():
    return db_connection.cursor()

@app.route('/')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def register():
    try:
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        
        # Create a new cursor
        db_cursor = get_database_cursor()
        
        # Insert user data into the database
        sql = "INSERT INTO users (fullname, email, password) VALUES (%s, %s, %s)"
        values = (fullname, email, password)
        db_cursor.execute(sql, values)
        db_connection.commit()
        
        # Insert user data into the login table
        login_sql = "INSERT INTO login (fullname, email, password) VALUES (%s, %s, %s)"
        login_values = (fullname, email, password)
        db_cursor.execute(login_sql, login_values)
        db_connection.commit()

        return "User registered successfully!"  # Message for successful registration
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            
            # Create a new cursor
            db_cursor = get_database_cursor()
            
            # Check if the user exists in the database
            sql = "SELECT * FROM users WHERE email = %s AND password = %s"
            values = (email, password)
            db_cursor.execute(sql, values)
            user = db_cursor.fetchone()
            
            if user:
                return redirect(url_for('index'))  # Redirect to the home page upon successful sign-in
            else:
                return "Invalid email or password. Please try again."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return render_template('signin.html')

# Function to add item to wishlist in database
@app.route('/wishlist', methods=['POST'])
def add_to_wishlist():
    try:
        data = request.get_json()
        item = data.get('item')
        
        # Create a new cursor
        db_cursor = get_database_cursor()
        
        if item:
            query = "INSERT INTO wishlist (item_name) VALUES (%s)"
            db_cursor.execute(query, (item,))
            db_connection.commit()
            return jsonify({'message': 'Item added to wishlist successfully'}), 200
        else:
            return jsonify({'message': 'Item not provided in request'}), 400
    except Exception as e:
        return jsonify({'message': 'Failed to add item to wishlist', 'error': str(e)}), 500

@app.route('/wishlist', methods=['GET'])
def get_wishlist():
    try:
        # Create a new cursor
        db_cursor = get_database_cursor()
        
        db_cursor.execute("SELECT item_name FROM wishlist")
        wishlist_items = [row[0] for row in db_cursor.fetchall()]
        return jsonify({'wishlist_items': wishlist_items}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to fetch wishlist items', 'error': str(e)}), 500

@app.route('/checkout', methods=['POST'])
def checkout():
    try:
        user_id = request.form['user_id']  # Assuming you have user authentication and you know the user's ID
        item_name = request.form['item_name']
        
        # Create a new cursor
        db_cursor = get_database_cursor()
        
        # Insert checkout details into the database
        sql = "INSERT INTO checkout (user_id, item_name) VALUES (%s, %s)"
        values = (user_id, item_name)
        db_cursor.execute(sql, values)
        db_connection.commit()
        
        return "Checkout successful!"  # Message for successful checkout
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/index')
def index():
    return render_template('index1.html')

@app.route('/clothes')
def clothes():
    try:
        # Fetch clothing products from the database
        db_cursor = get_database_cursor()
        db_cursor.execute("SELECT * FROM clothing_products")
        clothing_products = db_cursor.fetchall()
        
        return render_template('clothes.html', clothing_products=clothing_products)
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/health')
def health():
    try:
        # Fetch health products from the database
        db_cursor = get_database_cursor()
        db_cursor.execute("SELECT * FROM health_products")
        health_products = db_cursor.fetchall()
        
        return render_template('health.html', health_products=health_products)
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
if __name__ == '__main__':
    app.run(debug=True)
