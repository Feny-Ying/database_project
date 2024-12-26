from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector
import hashlib

# Flask App Initialization
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database Configuration
db_config = {
    'host': '35.201.204.93',  # Change this to your MySQL host
    'user': 'user',  # Change this to your MySQL username
    'password': '1234',  # Change this to your MySQL password
    'database': 'Final',  # Change this to your MySQL database name
}

# Database Connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Main
@app.route("/", methods=["GET", "POST"])
def main():
    if 'username' in session:
        session.pop('username', None)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == "POST":
        
        # Collect search and filter parameters from the form
        search = request.form.get('search', '').strip()
        price_min = request.form.get('price-min')
        price_max = request.form.get('price-max')
        area = request.form.get('area')
        stars = request.form.get('stars')
        room_type = request.form.get('roomtype')

        # Build the query dynamically based on the filters
        query = "SELECT * FROM listings WHERE 1=1"
        params = []

        if search:
            query += " AND host_name LIKE %s"
            params.append(f"%{search}%")
        if price_min:
            query += " AND price >= %s"
            params.append(price_min)
        if price_max:
            query += " AND price <= %s"
            params.append(price_max)
        if area:
            query += " AND region = %s"
            params.append(area)
        if stars and stars != "0":
            query += " AND rating >= %s"
            params.append(stars)
        if room_type:
            query += " AND room_type = %s"
            params.append(room_type)

        # Execute the query
        cursor.execute(query, params)
        results = cursor.fetchall()

        # Close the connection
        cursor.close()
        conn.close()

        # Redirect to the search route with query parameters
        query_params = {
            'search': search,
            'price-min': price_min,
            'price-max': price_max,
            'area': area,
            'stars': stars,
            'roomtype': room_type
        }
        
        query_params = {k: v for k, v in query_params.items() if v}
        
        query_string = '&'.join(f'{key}={value}' for key, value in query_params.items())
        return redirect(f'/search?{query_string}')
    
    return render_template("main.html")

#Main_User
@app.route("/main_user", methods=["GET", "POST"])
def main_user():
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == "POST":
        
        # Collect search and filter parameters from the form
        search = request.form.get('search', '').strip()
        price_min = request.form.get('price-min')
        price_max = request.form.get('price-max')
        area = request.form.get('area')
        stars = request.form.get('stars')
        room_type = request.form.get('roomtype')

        # Build the query dynamically based on the filters
        query = "SELECT * FROM listings WHERE 1=1"
        params = []

        if search:
            query += " AND host_name LIKE %s"
            params.append(f"%{search}%")
        if price_min:
            query += " AND price >= %s"
            params.append(price_min)
        if price_max:
            query += " AND price <= %s"
            params.append(price_max)
        if area:
            query += " AND region = %s"
            params.append(area)
        if stars and stars != "0":
            query += " AND rating >= %s"
            params.append(stars)
        if room_type:
            query += " AND room_type = %s"
            params.append(room_type)

        # Execute the query
        cursor.execute(query, params)
        results = cursor.fetchall()

        # Close the connection
        cursor.close()
        conn.close()

        # Redirect to the search route with query parameters
        query_params = {
            'search': search,
            'price-min': price_min,
            'price-max': price_max,
            'area': area,
            'stars': stars,
            'roomtype': room_type
        }
        query_string = '&'.join(f'{key}={value}' for key, value in query_params.items())
        return redirect(f'/search?{query_string}')
    
    return render_template("main_user.html", results=[], filters={})

@app.route("/search", methods=["GET", "POST"])
def search():
    # Extract search term and filters from the request
    search_query = request.args.get('search', '')
    price_min = request.args.get('price-min')
    price_max = request.args.get('price-max')
    area = request.args.get('area')
    stars = request.args.get('stars')
    room_type = request.args.get('roomtype')
    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Build query dynamically
        query = "SELECT * FROM listings WHERE 1=1"
        params = []

        if search_query:
            query += " AND host_name LIKE %s"
            params.append(f"%{search_query}%")
        if price_min:
            query += " AND price >= %s"
            params.append(price_min)
        if price_max:
            query += " AND price <= %s"
            params.append(price_max)
        if area:
            query += " AND region = %s"
            params.append(area)
        if stars and stars != "0":
            query += " AND rating >= %s"
            params.append(stars)
        if room_type:
            query += " AND room_type = %s"
            params.append(room_type)

        query += " LIMIT %s OFFSET %s"
        params.extend([per_page, offset])

        # Execute query
        cursor.execute(query, params)
        results = cursor.fetchall()

        # Get total count for pagination
        count_query = "SELECT COUNT(*) FROM listings WHERE 1=1"
        count_params = params[:-2]  # Exclude LIMIT and OFFSET
        cursor.execute(count_query, count_params)
        total_count = cursor.fetchone()[0]
        total_pages = (total_count + per_page - 1) // per_page

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        results = []
        total_pages = 1

    finally:
        cursor.close()
        conn.close()
        
    conn = get_db_connection()
    cursor = conn.cursor()
        
    if request.method == "POST":
        
        # Collect search and filter parameters from the form
        search = request.form.get('search', '').strip()
        price_min = request.form.get('price-min')
        price_max = request.form.get('price-max')
        area = request.form.get('area')
        stars = request.form.get('stars')
        room_type = request.form.get('roomtype')

        # Build the query dynamically based on the filters
        query = "SELECT * FROM listings WHERE 1=1"
        params = []

        if search:
            query += " AND host_name LIKE %s"
            params.append(f"%{search}%")
        if price_min:
            query += " AND price >= %s"
            params.append(price_min)
        if price_max:
            query += " AND price <= %s"
            params.append(price_max)
        if area:
            query += " AND region = %s"
            params.append(area)
        if stars and stars != "0":
            query += " AND rating >= %s"
            params.append(stars)
        if room_type:
            query += " AND room_type = %s"
            params.append(room_type)

        # Execute the query
        cursor.execute(query, params)
        results = cursor.fetchall()

        # Close the connection
        cursor.close()
        conn.close()

        # Redirect to the search route with query parameters
        query_params = {
            'search': search,
            'price-min': price_min,
            'price-max': price_max,
            'area': area,
            'stars': stars,
            'roomtype': room_type
        }
        query_string = '&'.join(f'{key}={value}' for key, value in query_params.items())
        return redirect(f'/search?{query_string}')

    return render_template("search.html", page=page, keyword=search_query, total_pages=total_pages, results=results, filters=request.args)

# List
@app.route("/list", methods=["GET", "POST"])
def list():
    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page
    
    conn = get_db_connection()
    cursor = conn.cursor()

    query_id = "SELECT id FROM users WHERE username = %s"
    username = session['username']
    cursor.execute(query_id, (username,))

    result = cursor.fetchone()
        
    user_id = result[0]
    
    print(user_id)
    
    try:
        query_list = """
        SELECT l.list_id, l.name, l.description
        FROM user_list ul
        JOIN list l ON ul.list_id = l.list_id
        WHERE ul.user_id = %s
        LIMIT %s OFFSET %s
        """
        cursor.execute(query_list, (user_id, per_page, offset))
        
        user_list = cursor.fetchall()
        
        # Get the total count of favorites
        query_count = """
        SELECT COUNT(*)
        FROM user_list ul
        JOIN list l ON ul.list_id = l.list_id
        WHERE ul.user_id = %s
        """
        cursor.execute(query_count, (user_id,))
        total_count = cursor.fetchone()[0]
        total_pages = (total_count + per_page - 1) // per_page

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        user_list = []
        total_pages = 1
        
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
    return render_template("list.html", page=page, total_pages=total_pages, results=user_list)

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the user exists in the database and whether the password is correct
        # Query to check the user
        try:
            query = "SELECT password FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            if result:
                stored_password = result[0]
                if stored_password == hashed_password:
                    session['username'] = username
                    return redirect("/main_user")
                else:
                    flash("Incorrect password.", "danger")
            else:
                flash("Username does not exist.", "danger")
        except mysql.connector.Error as err:
            flash(f"Database error: {err}", "danger")
        finally:
            cursor.close()
            conn.close()
        
    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/")

# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # TODO # 4: Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()


        # Add the query to insert a new user into the database
        try:
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, hashed_password))
            conn.commit()
            flash("Account created successfully! Please log in.", "success")
            return redirect("/login")
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "danger")
        finally:
            cursor.close()
            conn.close()
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
