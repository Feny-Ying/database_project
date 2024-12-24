from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector
import hashlib

# Flask App Initialization
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database Configuration
db_config = {
    'host': 'localhost',  # Change this to your MySQL host
    'user': 'root',  # Change this to your MySQL username
    'password': '24280143',  # Change this to your MySQL password
    'database': 'db_project',  # Change this to your MySQL database name
}

# Database Connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Main
@app.route("/", methods=["GET", "POST"])
def main():
    if 'username' in session:
        session.pop('username', None)
    
    if request.method == "POST":
        search = request.form['search']
        
        return redirect("/search")
        
    return render_template("main.html")

#Main_User
@app.route("/main_user", methods=["GET", "POST"])
def main_user():
    if request.method == "POST":
        search = request.form['search']
        
        return redirect("/search")
        
    return render_template("main_user.html")

# Search
@app.route("/search", methods=["GET", "POST"])
def search():
    # Extract search term and page number
    search_query = request.args.get('search', '')
    page = int(request.args.get('page', 1))  # Default to page 1 if not provided
    per_page = 10
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Search query to get matching hotel names
        query_search = """
        SELECT hotel_id, hotel_name, description
        FROM hotels
        WHERE hotel_name LIKE %s
        LIMIT %s OFFSET %s
        """
        cursor.execute(query_search, (f"%{search_query}%", per_page, offset))
        results = cursor.fetchall()

        # Get the total count of matching results
        query_count = """
        SELECT COUNT(*)
        FROM hotels
        WHERE hotel_name LIKE %s
        """
        cursor.execute(query_count, (f"%{search_query}%",))
        total_count = cursor.fetchone()[0]
        total_pages = (total_count + per_page - 1) // per_page

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        results = []
        total_pages = 1

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

    # Render the search template and pass the results and pagination information
    return render_template("search.html", page=page, keyword=search_query, total_pages=total_pages, results=results)

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
            return redirect("/")
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "danger")
        finally:
            cursor.close()
            conn.close()
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
