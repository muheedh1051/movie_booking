# Movie Magic - Flask + AWS-based Movie Booking Platform
# Complete project setup code (like your AWS Stocker app)

import os
import boto3
import hashlib
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import webbrowser
import threading
import time
from boto3.dynamodb.conditions import Key

app = Flask(__name__)
app.secret_key = 'moviemagic_secret_key_2024'

# AWS Configuration
AWS_REGION = 'us-east-1'
USERS_TABLE = 'movie_users'
MOVIES_TABLE = 'movie_movies'
BOOKINGS_TABLE = 'movie_bookings'
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:xxxx:movie_magic_alerts'

# Initialize AWS services
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
sns_client = boto3.client('sns', region_name=AWS_REGION)

# DynamoDB tables
users_table = dynamodb.Table(USERS_TABLE)
movies_table = dynamodb.Table(MOVIES_TABLE)
bookings_table = dynamodb.Table(BOOKINGS_TABLE)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def send_sns_message(subject, message, email=None):
    try:
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject=subject
        )
    except Exception as e:
        print(f"SNS Error: {e}")

@app.route('/')
def index():
    response = movies_table.scan()
    movies = response.get('Items', [])
    return render_template('index.html', movies=movies)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = hash_password(request.form['password'])
        role = request.form['role']  # Viewer or Admin

        response = users_table.get_item(Key={'email': email})
        if 'Item' in response:
            flash('Email already registered!', 'error')
            return redirect(url_for('signup'))

        users_table.put_item(Item={
            'email': email,
            'username': username,
            'password': password,
            'role': role,
            'created_at': datetime.now().isoformat()
        })

        send_sns_message('🎬 Welcome to Movie Magic!', f"Thanks {username} for signing up as {role} 🎉")
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hash_password(request.form['password'])
        role = request.form['role']

        response = users_table.get_item(Key={'email': email})
        user = response.get('Item')
        if user and user['password'] == password and user['role'] == role:
            session['user_email'] = email
            session['username'] = user['username']
            session['role'] = role
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard' if role == 'Admin' else 'movies'))
        flash('Invalid credentials!', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/movies')
def movies():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    response = movies_table.scan()
    return render_template('movies.html', movies=response.get('Items', []))

@app.route('/book/<movie_id>', methods=['GET', 'POST'])
def book(movie_id):
    if 'user_email' not in session:
        return redirect(url_for('login'))
    movie = movies_table.get_item(Key={'id': movie_id}).get('Item')
    if request.method == 'POST':
        seats = int(request.form['seats'])
        booking_id = str(uuid.uuid4())
        bookings_table.put_item(Item={
            'id': booking_id,
            'user_email': session['user_email'],
            'movie_id': movie_id,
            'movie_title': movie['title'],
            'seats': seats,
            'timestamp': datetime.now().isoformat()
        })
        send_sns_message('🎟️ Booking Confirmed!', f"You booked {seats} seats for {movie['title']} 🍿")
        flash('Booking successful!', 'success')
        return redirect(url_for('my_bookings'))
    return render_template('book.html', movie=movie)

@app.route('/my_bookings')
def my_bookings():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    response = bookings_table.scan(FilterExpression=Key('user_email').eq(session['user_email']))
    return render_template('my_bookings.html', bookings=response['Items'])

@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('role') != 'Admin':
        return redirect(url_for('login'))
    users = users_table.scan().get('Items', [])
    bookings = bookings_table.scan().get('Items', [])
    return render_template('admin_dashboard.html', users=users, bookings=bookings)

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if session.get('role') != 'Admin':
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        description = request.form['description']
        movie_id = str(uuid.uuid4())
        movies_table.put_item(Item={
            'id': movie_id,
            'title': title,
            'genre': genre,
            'description': description,
            'added_at': datetime.now().isoformat()
        })
        flash('Movie added!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_movie.html')

@app.route('/about')
def about():
    return render_template('about.html')

def open_browser():
    time.sleep(1.5)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    if not os.environ.get('WERKZEUG_RUN_MAIN'):
        threading.Thread(target=open_browser).start()
    app.run(debug=True, host='0.0.0.0', port=5000)
