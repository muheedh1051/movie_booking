from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

# App config
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",         # your MySQL username
    password="",         # leave blank if no password
    database="movie_booking"
)
cursor = db.cursor()

# ---------------- Routes ---------------- #

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match"

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
            return redirect(url_for('index'))
        except:
            return "Username already exists or error occurred"
    
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    if user:
        session['user_id'] = user[0]
        return redirect(url_for('home'))
    else:
        return redirect(url_for('index'))

@app.route('/home')
def home():
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    return render_template('home.html', movies=movies)

@app.route('/booking/<int:movie_id>')
def booking(movie_id):
    cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
    movie = cursor.fetchone()
    return render_template('booking.html', movie=movie)

@app.route('/confirm', methods=['POST'])
def confirm():
    user_id = session.get('user_id')
    movie_id = request.form.get('movie_id')
    show_time = request.form.get('show_time')
    seats = request.form.getlist('seats')

    if not show_time or not seats:
        return "Please select a show time and at least one seat."

    if len(seats) > 6:
        return "You can only book up to 6 seats."

    seat_str = ','.join(seats)
    cursor.execute(
        "INSERT INTO bookings (user_id, movie_id, show_time, seats) VALUES (%s, %s, %s, %s)",
        (user_id, movie_id, show_time, seat_str)
    )
    db.commit()

    

    cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
    movie = cursor.fetchone()

    return render_template('confirmation.html', show_time=show_time, seats=seats, movie=movie)

@app.route('/my_bookings')
def my_bookings():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))

    query = """
        SELECT m.title, b.show_time, b.seats
        FROM bookings b
        JOIN movies m ON b.movie_id = m.id
        WHERE b.user_id = %s
        ORDER BY b.id DESC
    """
    cursor.execute(query, (user_id,))
    bookings = cursor.fetchall()

    return render_template('my_bookings.html', bookings=bookings)

@app.route('/logout')
def logout():
    session.clear()  # Clears both user_id and admin session
    return redirect(url_for('index'))  # Redirects to login page


@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Simple admin check (you can make it secure later)
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid admin credentials"

    return render_template('admin_login.html')

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    # Only allow admin to access this page
    if not session.get('admin'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form['title']
        poster = request.form['poster']
        description = request.form['description']

        cursor.execute("INSERT INTO movies (title, poster, description) VALUES (%s, %s, %s)",
                       (title, poster, description))
        db.commit()
        return redirect(url_for('admin_dashboard'))

    return render_template('add_movie.html')


@app.route('/view_bookings')
def view_bookings():
    if not session.get('admin'):
        return redirect(url_for('index'))

    query = """
        SELECT u.username, m.title, b.show_time, b.seats
        FROM bookings b
        JOIN users u ON b.user_id = u.id
        JOIN movies m ON b.movie_id = m.id
        ORDER BY b.id DESC
    """
    cursor.execute(query)
    bookings = cursor.fetchall()

    return render_template('view_bookings.html', bookings=bookings)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
