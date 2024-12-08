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
    page = request.args.get('page', 1)  # Default to page 1 if not provided

    # Add your search logic here to get results...

    # Render the search template and pass the page number
    return render_template("search.html", page=int(page), keyword=search_query, total_pages=5, results=[])

# List
@app.route("/list", methods=["GET", "POST"])
def list():
    # Extract page number, default to 1 if not provided
    page = request.args.get('page', 1)

    # Add your logic to fetch the list data here...
    
    return render_template("list.html", page=int(page), total_pages=5, results=[])

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
