# 🎬 Movie Magic 🎟️  
An elegant online movie ticket booking system built with Flask and MySQL.

---

## 📌 Project Description

**Movie Magic** is a web-based movie ticket booking application where users can explore current movies, register/login, book tickets, and view their bookings. Admins can manage movies and view all bookings through a dedicated admin panel.

This project showcases full-stack development skills with Flask (Python), MySQL, and frontend technologies like HTML/CSS.

---

## 🌟 Features

### 👤 User Side:
- 🔐 User Registration and Login
- 🎥 Browse all available movies
- 🎫 Book tickets for movies
- 📂 View personal bookings and confirmations

### 🔒 Admin Side:
- 🔑 Admin Login
- ➕ Add new movies
- 📊 View all user bookings

### 💅 UI/UX:
- Simple and clean interface
- Responsive design for better user experience
- Visuals of popular movies via poster images

---

## 🛠️ Tech Stack

| Layer       | Technology            |
|-------------|------------------------|
| Frontend    | HTML, CSS              |
| Backend     | Flask (Python)         |
| Database    | MySQL (via XAMPP)      |
| Tools       | VS Code, Git, GitHub   |

---

## 🗂️ Project Structure
movie_booking/
├── static/
│ └── assets/ # Movie posters
│ └── css/ # Style files
├── templates/ # HTML pages
│ ├── home.html
│ ├── login.html
│ ├── register.html
│ ├── booking.html
│ ├── confirmation.html
│ ├── my_bookings.html
│ └── admin_login.html, add_movie.html, view_bookings.html
├── app.py # Flask application
└── README.md # Project description (you’re reading it!)


---

## 🚀 How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/muheedh1051/MovieMagic.git
   cd MovieMagic

2.Start MySQL using XAMPP, and create a movie_booking database.

3.Import the SQL tables:
   users
   movies
   bookings

4.Run the Flask app:
    python app.py
    
Visit:
http://localhost:5000 🎉

✨🎬 "Building Movie Magic has been a magical journey filled with creativity 🧠, learning 📚, and code 💻. 
       I hope this project inspires you 💡 as much as it inspired me while building it. 🚀"

— 💖 Muheedh 🎉

